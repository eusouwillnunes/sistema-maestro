"""
Helper deterministico do /importar-projeto.

Cobre: deteccao de estado, validacao, extracao atomica, conflitos,
wikilinks orfaos, log de proveniencia.

NAO edita conteudo dos arquivos importados (so move).
Tmp fora do vault (D13). status: concluido obrigatorio (D11).
"""
import argparse
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
STATUS_LINE_RE = re.compile(r"^status\s*:\s*(.+)$", re.MULTILINE)
WIKILINK_RE = re.compile(r"\[\[([^\]\|]+)(\|[^\]]+)?\]\]")

TEMPLATES_IDENTIDADE_ESPERADOS = {
    "circulo-dourado.md", "historia-fundadores.md", "identidade-visual.md",
    "manifesto.md", "perfil-publico.md", "personalidade-marca.md",
    "posicionamento.md", "tom-de-voz.md",
}
TEMPLATES_PRODUTO_ESPERADOS = {
    "analise-mercado.md", "big-idea-hook.md", "desejos-massa.md",
    "dossie.md", "oferta.md", "perfil-prospect.md",
    "prova-social.md", "swipe-file.md",
}

DECISOES_VALIDAS = {"sobrescrever", "manter", "pular"}

# Alias de normalização de nomes de pasta no source (singular → plural canônico).
# Nome alinhado com biblioteca_scaffold.py (D102, evita drift).
_ALIAS_NORMALIZACAO = {
    "produto": "produtos",
}


def detect_state(path: str) -> dict:
    p = Path(path).resolve()
    if not p.exists():
        return {"estado": 0, "hints": {"path_inexistente": True}}

    marker_workspace = p / ".maestro-workspace"
    config_projeto = p / "maestro" / "config.md"
    hints = {}

    # Estado 1: vault zerado
    if not marker_workspace.exists() and not config_projeto.exists():
        # Pasta vazia ou so com .obsidian/
        conteudo = [x for x in p.iterdir() if x.name != ".obsidian"]
        if not conteudo:
            return {"estado": 1, "hints": hints}
        # Tem outras coisas mas sem markers — ainda trata como 1
        return {"estado": 1, "hints": hints}

    # Estado 2: workspace, CWD na raiz
    if marker_workspace.exists() and not config_projeto.exists():
        projetos = [
            d for d in p.iterdir()
            if d.is_dir() and (d / "maestro" / "config.md").exists()
        ]
        if not projetos:
            hints["workspace_orfao"] = True
        elif len(projetos) > 1:
            hints["cwd_ambiguo"] = True
            hints["projetos_disponiveis"] = [d.name for d in projetos]
        return {"estado": 2, "hints": hints}

    # Estados 3-5: dentro de projeto (D102 — top-level, sem wrapper)
    if config_projeto.exists():
        # Validar config
        try:
            txt = config_projeto.read_text(encoding="utf-8")
            if "---" not in txt or "tipo:" not in txt:
                hints["config_invalida"] = True
        except Exception:
            hints["config_invalida"] = True

        identidade = p / "identidade"
        produtos = p / "produtos"
        identidade_tem = identidade.exists() and any(identidade.glob("*.md"))
        produtos_tem = produtos.exists() and any(produtos.glob("*/*.md"))

        if not identidade_tem and not produtos_tem:
            hints["cascas_vazias"] = True
            return {"estado": 4, "hints": hints}

        if identidade_tem and produtos_tem:
            return {"estado": 5, "hints": hints}

        return {"estado": 4, "hints": hints}

    return {"estado": 0, "hints": {"indefinido": True}}


def scan_input(path: str) -> dict:
    p = Path(path).resolve()
    if not p.exists():
        return {"modo": "vazio", "items": []}

    zips = sorted([f.name for f in p.glob("*.zip") if f.is_file()])

    # Detectar bare ANTES de normalizar (aceita 'produto/' OU 'produtos/')
    bare_identidade = (p / "identidade").is_dir() and any((p / "identidade").glob("*.md"))
    bare_produto_singular = (p / "produto").is_dir() and any((p / "produto").glob("*/*.md"))
    bare_produtos_plural = (p / "produtos").is_dir() and any((p / "produtos").glob("*/*.md"))
    bare_produtos = bare_produto_singular or bare_produtos_plural

    tem_zip = bool(zips)
    tem_bare = bare_identidade or bare_produtos

    if tem_zip and tem_bare:
        # Não normaliza no mix — só após user escolher modo bare
        bare_items = []
        if bare_identidade:
            bare_items.append("identidade")
        if bare_produtos:
            bare_items.append("produtos")  # normalizado pra plural
        return {"modo": "mix", "items": {"zips": zips, "pastas": bare_items}}

    if tem_zip:
        return {"modo": "zip", "items": zips}

    if tem_bare:
        # Normalização in-place (D102): renomeia 'produto/' → 'produtos/' fisicamente
        norm = _normalizar_aliases_no_tmp(p)
        if norm["erros"]:
            # Colisão produto/ E produtos/ — passa erro pra cima
            return {
                "modo": "bare-erro",
                "items": [],
                "erros": norm["erros"],
            }
        bare_items = []
        if bare_identidade:
            bare_items.append("identidade")
        if bare_produtos:
            bare_items.append("produtos")
        result = {"modo": "bare", "items": bare_items}
        if norm["renames"]:
            result["renames"] = norm["renames"]
        return result

    return {"modo": "vazio", "items": []}


def inspect_zip(zip_path: str) -> dict:
    zp = Path(zip_path).resolve()
    if not zp.exists():
        raise ValueError(f"ZIP nao existe: {zip_path}")
    if not zipfile.is_zipfile(zp):
        raise ValueError(f"Arquivo nao eh ZIP valido: {zip_path}")

    folders = set()
    files = []
    total_size = 0
    with zipfile.ZipFile(zp, "r") as zf:
        for info in zf.infolist():
            if info.is_dir():
                folders.add(info.filename.rstrip("/"))
            else:
                files.append(info.filename)
                total_size += info.file_size
                # Adicionar pastas-pai
                parts = info.filename.split("/")
                for i in range(1, len(parts)):
                    folders.add("/".join(parts[:i]))
    return {
        "folders": sorted(folders),
        "files": sorted(files),
        "total_size": total_size,
    }


def _ler_status(arquivo: Path) -> tuple:
    """Retorna (status, motivo_se_invalido). Status None se quebrado."""
    try:
        txt = arquivo.read_text(encoding="utf-8")
    except Exception as e:
        return None, f"leitura falhou: {e}"
    m = FRONTMATTER_RE.match(txt)
    if not m:
        return None, "frontmatter ausente"
    fm = m.group(1)
    sm = STATUS_LINE_RE.search(fm)
    if not sm:
        return None, "status ausente"
    valor = sm.group(1).strip()
    if not valor or ":" in valor or valor.startswith(("'", '"')):
        # Heuristica simples de frontmatter quebrado
        if ":" in valor:
            return None, "frontmatter quebrado"
    return valor, None


def _normalizar_aliases_no_tmp(tmp_path) -> dict:
    """
    Renomeia pastas singulares pra plural canônico no tmp.

    Pra cada alias em _ALIAS_NORMALIZACAO:
    - Se tmp/<alias> existe e tmp/<plural> NÃO existe → rename
    - Se ambos existem → erro estruturado (sem merge silencioso)
    - Se nada existe → no-op

    Retorna {"renames": [(from, to), ...], "erros": [...]}.
    """
    tmp = Path(tmp_path)
    renames = []
    erros = []
    for singular, plural in _ALIAS_NORMALIZACAO.items():
        src = tmp / singular
        dst = tmp / plural
        if src.exists() and dst.exists():
            erros.append({
                "erro": "alias-collision",
                "tipo": "alias-collision",
                "detalhes": f"tmp contém tanto '{singular}/' quanto '{plural}/'",
                "mensagem-natural": (
                    f"Seu arquivo .zip tem duas pastas com nomes parecidos "
                    f"(`{singular}/` e `{plural}/`). Deixa só uma das duas e tenta de novo."
                ),
            })
            continue
        if src.exists() and not dst.exists():
            try:
                src.rename(dst)
                renames.append((singular, plural))
            except OSError as e:
                erros.append({
                    "erro": "rename-failed",
                    "tipo": "io-error",
                    "detalhes": f"falhou rename de '{singular}/' pra '{plural}/': {e}",
                    "mensagem-natural": (
                        f"Não consegui renomear a pasta `{singular}/` pra `{plural}/` no tmp. "
                        "Pode ser que algum programa esteja com a pasta aberta — fecha e tenta de novo."
                    ),
                })
    return {"renames": renames, "erros": erros}


def validate_pre_requisitos(layout: list) -> dict:
    invalidos = []
    for p in layout:
        arquivo = Path(p)
        if not arquivo.exists():
            invalidos.append({"path": p, "motivo": "arquivo nao existe"})
            continue
        status, motivo = _ler_status(arquivo)
        if motivo:
            invalidos.append({"path": p, "motivo": motivo})
        elif status != "concluido":
            invalidos.append({"path": p, "motivo": f"status: {status}"})
    return {"ok": len(invalidos) == 0, "arquivos_invalidos": invalidos}


def validate_integrity(layout: dict) -> dict:
    avisos = []
    bloqueios = []

    identidade = layout.get("identidade", [])
    produtos = layout.get("produtos", {})
    produtos_existe = layout.get("_produtos_existe", False) or bool(produtos)

    if not identidade and not produtos:
        bloqueios.append("nem identidade nem produtos encontrados")
        return {"verdict": "bloqueio", "avisos": avisos, "bloqueios": bloqueios}

    if produtos_existe and not produtos:
        bloqueios.append("pasta produtos/ presente mas sem slug")
        return {"verdict": "bloqueio", "avisos": avisos, "bloqueios": bloqueios}

    if identidade:
        identidade_set = set(identidade)
        faltam = TEMPLATES_IDENTIDADE_ESPERADOS - identidade_set
        extras = identidade_set - TEMPLATES_IDENTIDADE_ESPERADOS
        if faltam:
            avisos.append(f"identidade/: faltam {sorted(faltam)}")
        if extras:
            avisos.append(f"identidade/: arquivos inesperados {sorted(extras)}")

    for slug, arquivos in produtos.items():
        arquivos_set = set(arquivos)
        faltam = TEMPLATES_PRODUTO_ESPERADOS - arquivos_set
        extras = arquivos_set - TEMPLATES_PRODUTO_ESPERADOS
        if faltam:
            avisos.append(f"produtos/{slug}/: faltam {sorted(faltam)}")
        if extras:
            avisos.append(f"produtos/{slug}/: arquivos inesperados {sorted(extras)}")

    return {"verdict": "ok", "avisos": avisos, "bloqueios": bloqueios}


def extract_atomic(zip_path: str, tmp_externo: str) -> dict:
    zp = Path(zip_path).resolve()
    tmp = Path(tmp_externo).resolve()

    if not zp.exists():
        return {"ok": False, "erro": f"ZIP nao existe: {zip_path}"}
    if not zipfile.is_zipfile(zp):
        return {"ok": False, "erro": "ZIP corrompido ou invalido"}

    tmp.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(zp, "r") as zf:
            # Validar path traversal antes de extrair
            for info in zf.infolist():
                destino = (tmp / info.filename).resolve()
                if not str(destino).startswith(str(tmp)):
                    shutil.rmtree(tmp, ignore_errors=True)
                    return {
                        "ok": False,
                        "erro": f"path traversal detectado em '{info.filename}' — extracao fora do tmp",
                    }
            zf.extractall(tmp)
        # D102 — normaliza singular→plural após extração
        norm = _normalizar_aliases_no_tmp(tmp)
        if norm["erros"]:
            # Colisão alias (produto/ E produtos/) — propaga erro estruturado
            erro = norm["erros"][0]
            shutil.rmtree(tmp, ignore_errors=True)
            return {"ok": False, **erro}
        result = {"ok": True, "extracted_to": str(tmp)}
        if norm["renames"]:
            result["renames"] = norm["renames"]
        return result
    except OSError as e:
        shutil.rmtree(tmp, ignore_errors=True)
        if "No space" in str(e) or "ENOSPC" in str(e):
            return {"ok": False, "erro": "NO_SPACE: disco cheio"}
        return {"ok": False, "erro": f"IO error: {e}"}
    except Exception as e:
        shutil.rmtree(tmp, ignore_errors=True)
        return {"ok": False, "erro": str(e)}


def detect_conflicts(target: str, source: str) -> dict:
    target_path = Path(target)
    source_path = Path(source)
    conflitos = []

    src_ident = source_path / "identidade"
    if src_ident.is_dir():
        tgt_ident = target_path / "identidade"
        choques = []
        if tgt_ident.is_dir():
            for arquivo in src_ident.glob("*.md"):
                if (tgt_ident / arquivo.name).exists():
                    choques.append(arquivo.name)
        if choques:
            conflitos.append({"grupo": "identidade", "arquivos": sorted(choques)})

    # D102 — source já normalizado pra plural (extract_atomic ou scan_input)
    src_prod = source_path / "produtos"
    if src_prod.is_dir():
        for slug_dir in src_prod.iterdir():
            if not slug_dir.is_dir():
                continue
            slug = slug_dir.name
            tgt_slug = target_path / "produtos" / slug
            choques = []
            if tgt_slug.is_dir():
                for arquivo in slug_dir.glob("*.md"):
                    if (tgt_slug / arquivo.name).exists():
                        choques.append(arquivo.name)
            if choques:
                conflitos.append({
                    "grupo": f"produtos/{slug}",
                    "arquivos": sorted(choques),
                })

    return {"conflitos": conflitos}


def apply_resolution(target: str, source: str, decisions: dict) -> dict:
    target_path = Path(target)
    source_path = Path(source)
    target_path.mkdir(parents=True, exist_ok=True)

    arquivos_importados = []
    removidos = []
    erros = []

    # Validar decisoes
    for grupo, decisao in decisions.items():
        if decisao not in DECISOES_VALIDAS:
            erros.append(f"decisao invalida pra grupo '{grupo}': '{decisao}'")
    if erros:
        return {"arquivos_importados": [], "removidos": [], "erros": erros}

    src_ident = source_path / "identidade"
    if src_ident.is_dir():
        decisao = decisions.get("identidade", "sobrescrever")
        if decisao != "pular":
            tgt = target_path / "identidade"
            tgt.mkdir(parents=True, exist_ok=True)
            for arquivo in src_ident.glob("*.md"):
                destino = tgt / arquivo.name
                if destino.exists() and decisao == "manter":
                    continue
                shutil.move(str(arquivo), str(destino))
                arquivos_importados.append(str(destino.relative_to(target_path)))

    # D102 — source ja normalizado pra plural
    src_prod = source_path / "produtos"
    if src_prod.is_dir():
        for slug_dir in src_prod.iterdir():
            if not slug_dir.is_dir():
                continue
            grupo = f"produtos/{slug_dir.name}"
            decisao = decisions.get(grupo, "sobrescrever")
            if decisao == "pular":
                continue
            tgt_slug = target_path / "produtos" / slug_dir.name
            tgt_slug.mkdir(parents=True, exist_ok=True)
            for arquivo in slug_dir.glob("*.md"):
                destino = tgt_slug / arquivo.name
                if destino.exists() and decisao == "manter":
                    continue
                shutil.move(str(arquivo), str(destino))
                arquivos_importados.append(str(destino.relative_to(target_path)))

    # Cleanup source vazio
    try:
        shutil.rmtree(source_path)
    except OSError:
        pass

    return {
        "arquivos_importados": sorted(arquivos_importados),
        "removidos": removidos,
        "erros": erros,
    }


def scan_orphan_wikilinks(paths: list, target: str = None) -> dict:
    """
    Procura wikilinks em paths e retorna os que apontam pra arquivos inexistentes
    dentro do target.
    """
    if target is None:
        # paths[0] vai ate o pai do target
        target = str(Path(paths[0]).parent.parent.parent)
    target_path = Path(target)
    orfaos = []
    total_arquivos = 0

    for path_grupo in paths:
        pg = Path(path_grupo)
        if not pg.is_dir():
            continue
        for arquivo in pg.rglob("*.md"):
            total_arquivos += 1
            try:
                txt = arquivo.read_text(encoding="utf-8")
            except Exception:
                continue
            for match in WIKILINK_RE.finditer(txt):
                link = match.group(1).strip()
                # Resolver: link relativo a algum lugar do vault
                destinos_possiveis = [
                    target_path / f"{link}.md",
                    target_path / link / f"{Path(link).name}.md",
                ]
                if not any(d.exists() for d in destinos_possiveis):
                    orfaos.append({
                        "arquivo": str(arquivo.relative_to(target_path)),
                        "link": link,
                        "destino_esperado": f"{link}.md",
                    })

    return {"orfaos": orfaos, "total_arquivos_processados": total_arquivos}


def _slug_safe(nome: str) -> str:
    nome = re.sub(r"[^\w\-.]+", "-", nome.lower())
    return re.sub(r"-+", "-", nome).strip("-")


def write_provenance(target: str, source_name: str, summary: dict) -> dict:
    target_path = Path(target)
    pasta_log = target_path / "memorias" / "importacoes"
    pasta_log.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    slug_fonte = _slug_safe(source_name)
    arquivo = pasta_log / f"{timestamp}-{slug_fonte}.md"

    arquivos_importados = summary.get("arquivos_importados", [])
    avisos = summary.get("avisos", [])
    orfaos = summary.get("wikilinks_orfaos", [])

    # B-Imp-cand-5: aceita int (contagem direta) ou list (itera). Rejeita outros tipos.
    arquivos_count, arquivos_lista = _normalizar_campo_summary(
        arquivos_importados, "arquivos_importados"
    )
    avisos_count, avisos_lista = _normalizar_campo_summary(avisos, "avisos")
    orfaos_count, orfaos_lista = _normalizar_campo_summary(orfaos, "wikilinks_orfaos")

    conteudo = f"""---
tipo: log-importacao
status: concluido
timestamp: {datetime.now().isoformat(timespec='seconds')}
fonte: {source_name}
projeto-destino: {summary.get('projeto_destino', '')}
arquivos-importados: {arquivos_count}
avisos: {avisos_count}
wikilinks-orfaos: {orfaos_count}
---

# Importacao de {timestamp.replace('T', ' ')}

## Arquivos importados ({arquivos_count})

"""
    for a in arquivos_lista:
        conteudo += f"- `{a}`\n"
    conteudo += f"\n## Avisos ({avisos_count})\n\n"
    for a in avisos_lista:
        conteudo += f"- {a}\n"
    conteudo += f"\n## Ligacoes orfas ({orfaos_count})\n\n"
    for o in orfaos_lista:
        if isinstance(o, dict):
            conteudo += f"- `[[{o['link']}]]` em `{o['arquivo']}`\n"
        else:
            conteudo += f"- {o}\n"

    arquivo.write_text(conteudo, encoding="utf-8")

    # Append no _log.md agregador
    log_agg = pasta_log / "_log.md"
    if not log_agg.exists():
        log_agg.write_text(
            "# Log de Importacoes\n\n| Timestamp | Resultado | Arquivos | Erro |\n|---|---|---|---|\n",
            encoding="utf-8",
        )
    with open(log_agg, "a", encoding="utf-8") as f:
        f.write(f"| {timestamp} | ok | {arquivos_count} | {source_name} | - |\n")

    return {"arquivo_log": str(arquivo)}


def _normalizar_campo_summary(valor, nome_campo: str):
    """B-Imp-cand-5: aceita list ou int em campos do summary; rejeita outros tipos.

    Retorna (count, lista_iteravel). Se valor era int, lista volta vazia.
    Se valor era list, count = len(lista).
    Outros tipos: erro estruturado pra stderr.
    """
    if isinstance(valor, list):
        return len(valor), valor
    if isinstance(valor, int):
        return valor, []
    _emit_arg_error(
        "write_provenance",
        f"summary.{nome_campo}",
        "wrong-type",
        f"esperava list ou int, recebeu {type(valor).__name__}",
    )


def cleanup_tmp_externo(tmp_path: str) -> dict:
    tmp = Path(tmp_path)
    if tmp.exists():
        shutil.rmtree(tmp, ignore_errors=True)
    return {"ok": True}


def _emit_arg_error(funcao: str, arg_name: str, tipo: str, detalhe: str) -> None:
    """Emite erro estruturado de validacao de arg e sai com codigo 2."""
    payload = {
        "erro": f"--{arg_name} {detalhe} (funcao: {funcao})",
        "tipo": tipo,
        "funcao": funcao,
        "arg": arg_name,
    }
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
    sys.exit(2)


def _parse_json_arg(arg_value, arg_name: str, funcao: str, expected_type=None):
    """Parse JSON arg do CLI com erro amigavel.

    - None -> tipo: missing-arg
    - JSON invalido -> tipo: invalid-json (B-Imp-cand-17)
    - Tipo errado -> tipo: wrong-type
    """
    if arg_value is None:
        _emit_arg_error(funcao, arg_name, "missing-arg", "obrigatorio mas ausente")
    try:
        parsed = json.loads(arg_value)
    except json.JSONDecodeError as e:
        _emit_arg_error(
            funcao,
            arg_name,
            "invalid-json",
            f"JSON invalido: {e.msg} (linha {e.lineno}, coluna {e.colno}). "
            f"Dica: paths Windows com backslash precisam de escape duplo no JSON (C:\\\\tmp\\\\foo).",
        )
    if expected_type is not None and not isinstance(parsed, expected_type):
        _emit_arg_error(
            funcao,
            arg_name,
            "wrong-type",
            f"esperava {expected_type.__name__}, recebeu {type(parsed).__name__}",
        )
    return parsed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("funcao", choices=[
        "detect_state", "scan_input", "inspect_zip",
        "validate_pre_requisitos", "validate_integrity",
        "extract_atomic", "detect_conflicts", "apply_resolution",
        "scan_orphan_wikilinks", "write_provenance", "cleanup_tmp_externo",
    ])
    parser.add_argument("--target", help="Path absoluto da pasta-alvo")
    parser.add_argument("--zip", help="Path absoluto do ZIP")
    parser.add_argument("--tmp", help="Path absoluto do tmp externo")
    parser.add_argument("--source", help="Path do source (tmp ou BARE)")
    parser.add_argument("--decisions", help="JSON com decisoes de conflito")
    parser.add_argument("--paths", help="JSON com lista de paths pra scan")
    parser.add_argument("--source-name", help="Nome amigavel da fonte")
    parser.add_argument("--summary", help="JSON com sumario pro provenance")
    args = parser.parse_args()

    try:
        if args.funcao == "detect_state":
            resultado = detect_state(args.target)
        elif args.funcao == "scan_input":
            resultado = scan_input(args.target)
        elif args.funcao == "inspect_zip":
            resultado = inspect_zip(args.zip)
        elif args.funcao == "validate_pre_requisitos":
            layout = _parse_json_arg(args.paths, "paths", args.funcao, expected_type=list)
            resultado = validate_pre_requisitos(layout)
        elif args.funcao == "validate_integrity":
            layout = _parse_json_arg(args.paths, "paths", args.funcao, expected_type=dict)
            resultado = validate_integrity(layout)
        elif args.funcao == "extract_atomic":
            resultado = extract_atomic(args.zip, args.tmp)
        elif args.funcao == "detect_conflicts":
            resultado = detect_conflicts(args.target, args.source)
        elif args.funcao == "apply_resolution":
            decisions = _parse_json_arg(args.decisions, "decisions", args.funcao, expected_type=dict)
            resultado = apply_resolution(args.target, args.source, decisions)
        elif args.funcao == "scan_orphan_wikilinks":
            paths = _parse_json_arg(args.paths, "paths", args.funcao, expected_type=list)
            resultado = scan_orphan_wikilinks(paths, args.target)
        elif args.funcao == "write_provenance":
            summary = _parse_json_arg(args.summary, "summary", args.funcao, expected_type=dict)
            resultado = write_provenance(args.target, args.source_name, summary)
        elif args.funcao == "cleanup_tmp_externo":
            resultado = cleanup_tmp_externo(args.tmp)

        print(json.dumps(resultado, ensure_ascii=False))
        sys.exit(0)
    except Exception as exc:
        print(json.dumps({"erro": str(exc)}), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
