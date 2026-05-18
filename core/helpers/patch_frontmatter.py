#!/usr/bin/env python3
"""Helper de escrita controlada do frontmatter.

Lê catálogo central de status, valida enum, escreve atomicamente.
Modos: --file (single) ou --batch (stdin JSON array).
"""
import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path


# Cache do catálogo em memória (carregado 1x por processo)
_CATALOG_CACHE = None


def load_catalog(path: Path) -> dict:
    """Parse o catálogo Markdown para dict.

    Retorna: {"canonicos-universais": [...], "tipos": {tipo: {...}}}
    """
    global _CATALOG_CACHE
    if _CATALOG_CACHE is not None and _CATALOG_CACHE.get("_path") == str(path):
        return _CATALOG_CACHE

    text = path.read_text(encoding="utf-8")
    result = {"canonicos-universais": [], "tipos": {}}

    # Status canônicos universais — bullets sob "## Status canônicos universais"
    canon_section = re.search(
        r"## Status canônicos universais\s*\n(.*?)(?=\n##|\Z)",
        text, re.DOTALL,
    )
    if canon_section:
        for line in canon_section.group(1).splitlines():
            m = re.match(r"^- `([a-z-]+)`", line.strip())
            if m:
                result["canonicos-universais"].append(m.group(1))

    # Blocos `### tipo: X` (ou `### tipo: X, Y, Z` para schema compartilhado)
    type_blocks = re.findall(
        r"### tipo:\s*([a-z-, ]+?)\n(.*?)(?=\n### |\n## |\Z)",
        text, re.DOTALL,
    )
    for types_str, body in type_blocks:
        types = [t.strip() for t in types_str.split(",") if t.strip()]
        block = _parse_type_block(body)
        for t in types:
            result["tipos"][t] = block

    result["_path"] = str(path)
    _CATALOG_CACHE = result
    return result


def _parse_type_block(body: str) -> dict:
    """Parse de bloco de tipo. Retorna dict com chaves do schema."""
    block = {
        "status-canonicos": [],
        "extensoes": [],
        "campos-auxiliares": [],
        "categoria-criativa-vai-pra-entregue": False,
    }
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        m = re.match(r"^- ([a-z-]+):\s*(.+?)(?:\s*#.*)?$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if key in ("status-canonicos", "extensoes", "campos-auxiliares"):
            if value in ("(nenhuma)", "(nenhum)"):
                block[key] = []
            else:
                block[key] = [v.strip() for v in value.split(",") if v.strip()]
        elif key == "categoria-criativa-vai-pra-entregue":
            block[key] = value.lower() == "true"
    return block


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def split_frontmatter(text: str) -> tuple[dict, str, list[str]]:
    """Separa frontmatter do corpo. Retorna (dict_fm, body, key_order)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text, []
    fm_text, body = m.group(1), m.group(2)
    fm = {}
    order = []
    for line in fm_text.splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        k, _, v = line.partition(":")
        k = k.strip()
        fm[k] = v.strip()
        order.append(k)
    return fm, body, order


def dump_frontmatter(fm: dict, order: list[str], body: str) -> str:
    """Reconstrói o arquivo preservando ordem de chaves."""
    lines = ["---"]
    seen = set()
    for k in order:
        if k in fm:
            lines.append(f"{k}: {fm[k]}")
            seen.add(k)
    # chaves novas (não estavam na ordem original) vão pro fim
    for k, v in fm.items():
        if k not in seen:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n" + body


def infer_tipo_by_folder(path: Path) -> str | None:
    """Infere tipo pelo nome da pasta pai."""
    parent = path.parent.name
    mapping = {
        "tarefas": "tarefa",
        "planos": "plano",
        "pesquisas": "pesquisa",
        "rascunhos": "rascunho",
        "entrevistas": "entrevista",
        "identidade": "identidade",
        "produto": "produto",
        "campanhas": "campanha",
        "funis": "funil",
        "lancamentos": "lancamento",
        "lead-magnets": "lead-magnet",
    }
    return mapping.get(parent)


def atomic_write(target: Path, content: str) -> None:
    """Escrita atômica usando tempfile no mesmo diretório (cross-platform)."""
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False,
            dir=target.parent, suffix=".tmp",
        ) as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)
        os.replace(tmp_path, target)
    except Exception:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        raise


def apply_patch(path: Path, sets: dict, unsets: list, catalog: dict, tipo_override: str | None = None) -> tuple:
    """Aplica patch. Retorna (sucesso, mensagem)."""
    text = path.read_text(encoding="utf-8")
    fm, body, order = split_frontmatter(text)
    if not fm:
        return False, f"arquivo sem frontmatter: {path}"

    tipo = tipo_override or fm.get("tipo") or infer_tipo_by_folder(path)
    if not tipo:
        return False, f"tipo indeterminado para {path}; use --tipo X"
    if tipo not in catalog["tipos"]:
        return False, f"tipo '{tipo}' nao esta no catalogo"

    type_block = catalog["tipos"][tipo]
    valid_statuses = set(type_block["status-canonicos"]) | set(type_block["extensoes"])
    known_aux = set(type_block.get("campos-auxiliares", []))
    sistema_keys = {"tipo", "status", "data-criacao", "data-inicio", "data-conclusao",
                    "data-cancelamento", "data-entregue", "data-aprovacao",
                    "titulo", "agente", "categoria", "solicitante", "parte-de",
                    "resultado", "tags", "camada", "depende-de", "concluido-por",
                    "aprovada-por", "_ultima-correcao-por", "voltas-em-revisao",
                    "corrige", "correcoes", "adicionada-em", "criado-em",
                    "tarefa-relacionada", "agente-solicitante", "regera",
                    "agente-decompositor", "modo-execucao", "total-tarefas",
                    "tarefas-concluidas"}

    # Aplica sets
    for k, v in sets.items():
        if k == "status":
            if v not in valid_statuses:
                return False, (
                    f"status '{v}' fora do enum para tipo '{tipo}'. "
                    f"Validos: {sorted(valid_statuses)}"
                )
        elif k not in known_aux and k not in sistema_keys:
            print(
                f"aviso: campo '{k}' nao declarado no catalogo do tipo '{tipo}'; aplicando assim mesmo",
                file=sys.stderr,
            )
        fm[k] = v
        if k not in order:
            order.append(k)

    # Aplica unsets
    for k in unsets:
        fm.pop(k, None)

    new_text = dump_frontmatter(fm, order, body)
    atomic_write(path, new_text)
    return True, "OK " + " ".join(f"{k}={v}" for k, v in sets.items())


def main():
    parser = argparse.ArgumentParser(description="Patch frontmatter com validacao de enum.")
    parser.add_argument("--file", type=Path)
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--set", action="append", default=[], dest="sets")
    parser.add_argument("--unset", action="append", default=[], dest="unsets")
    parser.add_argument("--tipo")
    args = parser.parse_args()

    catalog_path = Path(__file__).parent.parent / "protocolos" / "catalogo-status.md"
    catalog = load_catalog(catalog_path)

    if args.batch:
        return main_batch(catalog)

    if not args.file:
        print("uso: --file <path> --set k=v [--set k=v ...] | --batch < json", file=sys.stderr)
        return 1

    sets = {}
    for s in args.sets:
        if "=" not in s:
            print(f"--set invalido: {s}", file=sys.stderr)
            return 1
        k, _, v = s.partition("=")
        sets[k] = v

    ok, msg = apply_patch(args.file, sets, args.unsets, catalog, args.tipo)
    if ok:
        print(msg)
    else:
        print(msg, file=sys.stderr)
    return 0 if ok else 1


def main_batch(catalog: dict) -> int:
    """Modo --batch: le JSON array do stdin."""
    try:
        items = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"JSON invalido no stdin: {e}", file=sys.stderr)
        return 1

    failed = 0
    for item in items:
        path = Path(item["file"])
        sets = item.get("sets", {})
        unsets = item.get("unsets", [])
        tipo = item.get("tipo")
        ok, msg = apply_patch(path, sets, unsets, catalog, tipo)
        if ok:
            print(f"OK {path}")
        else:
            print(f"FAIL {path}: {msg}", file=sys.stderr)
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
