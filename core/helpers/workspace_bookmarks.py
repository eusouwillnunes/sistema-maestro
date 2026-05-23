#!/usr/bin/env python3
"""
Helper de bookmarks da workspace.

Manipula <workspace>/.obsidian/bookmarks.json com merge idempotente por
path interno (aprendizado #19). Atomic write com retry-on-WinError-5
(backoff [0.2, 0.5, 1.0, 2.0]s — Obsidian indexing pode segurar handle
200-500ms; Fase 0 F4 Teste A confirmou os.replace atomico em NTFS).

CLI:
    python workspace_bookmarks.py scaffold <ws> <projeto-slug>
    python workspace_bookmarks.py regenerate <ws>
    python workspace_bookmarks.py inject-callout <ws>
    python workspace_bookmarks.py library <ws> <projeto-slug> <items-json>

Exit codes:
    0 — sucesso
    2 — write falhou apos retries (stderr: WRITE_FAILED|...)
    3 — JSON corrompido (logado mas continua, exit 0)
    1 — erro nao previsto
"""
import errno
import json
import os
import sys
import time
from pathlib import Path

BACKOFFS = [0.2, 0.5, 1.0, 2.0]
CALLOUT_MARKER = "<!-- MAESTRO_CALLOUT_COLISAO -->"
# Marker fica DENTRO do blockquote (prefixo `> `) pra ficar invisivel no
# Reading View do Obsidian. Fora de blockquote/code, Obsidian renderiza
# HTML comment como texto literal (B-F4-VAL-3, Sessao 72).
CALLOUT_TEXT = """> [!info] Nomes iguais entre projetos
>
> Você tem múltiplos projetos nessa Área de Trabalho. Se dois projetos tiverem
> um arquivo com o mesmo nome (ex: `funil-webinar`), o Obsidian abre o do
> projeto onde você está agora.
>
> Pra abrir o de outro projeto, use a busca rápida (`Ctrl+O` ou `Cmd+O`) e
> digite o nome da pasta antes — ex: `cliente-b/funil-webinar`.
>
> <!-- MAESTRO_CALLOUT_COLISAO -->
"""


def _now_ms() -> int:
    return int(time.time() * 1000)


def atomic_write_json(target: Path, data: dict) -> None:
    """tmp + os.replace + retry [0.2, 0.5, 1.0, 2.0]s em WinError 5."""
    tmp = target.with_suffix(target.suffix + ".tmp")
    last_err = None
    for delay in [0] + BACKOFFS:
        if delay > 0:
            time.sleep(delay)
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(str(tmp), str(target))
            return
        except OSError as e:
            if getattr(e, "winerror", None) != 5 and e.errno != errno.EACCES:
                raise
            last_err = e
    sys.stderr.write(
        f"WRITE_FAILED|target={target}|attempts={len(BACKOFFS)+1}|last_err={last_err}\n"
    )
    sys.exit(2)


def load_bookmarks(workspace: Path) -> dict:
    """Le bookmarks.json. Fallback {'items': []}. Backup .bak se corrompido."""
    bm = workspace / ".obsidian" / "bookmarks.json"
    if not bm.exists():
        return {"items": []}
    try:
        return json.loads(bm.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        bak = bm.with_suffix(".json.bak")
        try:
            bm.replace(bak)
        except Exception:
            pass
        sys.stderr.write(f"JSON_CORRUPTED|backup={bak}\n")
        return {"items": []}


def save_bookmarks(workspace: Path, data: dict) -> None:
    bm = workspace / ".obsidian" / "bookmarks.json"
    bm.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(bm, data)


def has_path_anywhere(data: dict, target_path: str) -> bool:
    """Busca recursiva por item com path == target_path."""
    def walk(node):
        if isinstance(node, dict):
            if node.get("path") == target_path:
                return True
            for v in node.values():
                if walk(v):
                    return True
        elif isinstance(node, list):
            for item in node:
                if walk(item):
                    return True
        return False
    return walk(data)


def has_group_at_root(data: dict, title: str) -> bool:
    return any(
        i.get("type") == "group" and i.get("title") == title
        for i in data.get("items", [])
    )


def find_group_at_root(data: dict, title: str) -> dict | None:
    for i in data.get("items", []):
        if i.get("type") == "group" and i.get("title") == title:
            return i
    return None


def add_painel_workspace(workspace: Path) -> None:
    """Adiciona grupo '📊 Painel da Área de Trabalho' (idempotente por path _painel/index.md)."""
    data = load_bookmarks(workspace)
    if has_path_anywhere(data, "_painel/index.md"):
        return  # ja existe

    ctime = _now_ms()
    grupo = {
        "type": "group",
        "title": "📊 Painel da Área de Trabalho",
        "description": "Visão agregada de todos os projetos e tarefas",
        "ctime": ctime,
        "items": [
            {"type": "file", "path": "_painel/index.md",   "title": "🏠 Visão geral",
             "description": "Lista de projetos da workspace", "ctime": ctime},
            {"type": "file", "path": "_painel/tarefas.md", "title": "✅ Tarefas em todos",
             "description": "Tarefas em aberto cross-project", "ctime": ctime},
            {"type": "file", "path": "_painel/grafo.md",   "title": "🕸️ Grafo cross-project",
             "description": "Tags compartilhadas entre projetos", "ctime": ctime},
        ],
    }
    data.setdefault("items", []).insert(0, grupo)
    save_bookmarks(workspace, data)


def add_projeto_subgrupo(workspace: Path, slug: str) -> None:
    """Adiciona/garante subgrupo do projeto dentro de '📁 Projetos' (idempotente)."""
    data = load_bookmarks(workspace)

    # Garantir grupo '📁 Projetos'
    projetos = find_group_at_root(data, "📁 Projetos")
    if projetos is None:
        ctime = _now_ms()
        projetos = {
            "type": "group",
            "title": "📁 Projetos",
            "description": "Navegação rápida pra cada projeto da workspace",
            "ctime": ctime,
            "items": [],
        }
        data.setdefault("items", []).append(projetos)

    # Idempotencia por path do painel do projeto
    target_path = f"{slug}/{slug}.md"
    if has_path_anywhere(data, target_path):
        save_bookmarks(workspace, data)
        return

    ctime = _now_ms()
    sub = {
        "type": "group",
        "title": slug,
        "ctime": ctime,
        "items": [
            {"type": "file",   "path": f"{slug}/{slug}.md", "title": "📊 Painel do projeto",
             "description": "Index principal do projeto", "ctime": ctime},
            {"type": "folder", "path": slug,                "title": "📂 Pasta",
             "description": "Pasta inteira do projeto no File Explorer", "ctime": ctime},
            {"type": "group",  "title": "📚 Biblioteca",
             "description": "Biblioteca de Marketing", "ctime": ctime, "items": []},
        ],
    }
    projetos["items"].append(sub)
    save_bookmarks(workspace, data)


def add_library_to_projeto(workspace: Path, slug: str, items: list[dict]) -> None:
    """
    Aninha items da biblioteca-de-marketing dentro de
    Projetos > <slug> > 📚 Biblioteca.

    Idempotente por path interno de cada item.
    """
    data = load_bookmarks(workspace)

    projetos = find_group_at_root(data, "📁 Projetos")
    if projetos is None:
        # Vault legado sem workspace — fallback: appendar no raiz como antes
        for item in items:
            if not has_path_anywhere(data, item.get("path", "")):
                data.setdefault("items", []).append(item)
        save_bookmarks(workspace, data)
        return

    sub = next(
        (g for g in projetos["items"] if g.get("type") == "group" and g.get("title") == slug),
        None,
    )
    if sub is None:
        # subgrupo do projeto nao existe ainda — criar
        add_projeto_subgrupo(workspace, slug)
        data = load_bookmarks(workspace)
        projetos = find_group_at_root(data, "📁 Projetos")
        sub = next(g for g in projetos["items"] if g.get("title") == slug)

    biblioteca = next(
        (g for g in sub["items"] if g.get("type") == "group" and g.get("title") == "📚 Biblioteca"),
        None,
    )
    if biblioteca is None:
        biblioteca = {"type": "group", "title": "📚 Biblioteca", "ctime": _now_ms(), "items": []}
        sub["items"].append(biblioteca)

    existing_paths = {i.get("path") for i in biblioteca["items"]}
    for item in items:
        if item.get("path") not in existing_paths:
            biblioteca["items"].append(item)

    save_bookmarks(workspace, data)


def add_auditoria_grupo(workspace: Path, slug: str) -> None:
    """
    Adiciona grupo '🔒 Auditoria' dentro de Projetos > <slug>, irmão de
    📚 Biblioteca. Idempotente por path interno.

    No-op silencioso se:
      - '📁 Projetos' não existe no bookmarks (workspace pré-F4)
      - subgrupo <slug> não existe dentro de '📁 Projetos'

    Defesa estrutural visível da Decisão 109 — materializa pra user leigo
    com vocabulário sem jargão técnico (Decisão 110).
    """
    data = load_bookmarks(workspace)

    projetos = find_group_at_root(data, "📁 Projetos")
    if projetos is None:
        return  # workspace pré-F4 — no-op

    sub = next(
        (g for g in projetos.get("items", [])
         if g.get("type") == "group" and g.get("title") == slug),
        None,
    )
    if sub is None:
        return  # subgrupo do projeto não existe — no-op

    # Idempotência por path do primeiro item
    bloqueios_path = f"{slug}/memorias/auditoria/_bloqueios-hook-index.md"
    if has_path_anywhere(data, bloqueios_path):
        return  # já existe

    ctime = _now_ms()
    grupo = {
        "type": "group",
        "title": "🔒 Auditoria",
        "description": "Acompanhe o que o Maestro bloqueou ou auditou enquanto trabalha",
        "ctime": ctime,
        "items": [
            {"type": "file",
             "path": bloqueios_path,
             "title": "📊 Bloqueios automáticos",
             "description": "Painel dos despachos que o sistema barrou antes de rodar",
             "ctime": ctime},
            {"type": "file",
             "path": f"{slug}/memorias/auditoria/_defesa-anti-hallucination.md",
             "title": "📊 Verificações de leitura",
             "description": "Painel das vezes que o sistema conferiu se o agente leu o arquivo certo",
             "ctime": ctime},
            {"type": "file",
             "path": f"{slug}/memorias/auditoria/historico.md",
             "title": "📊 Linha do tempo",
             "description": "Histórico cronológico geral da auditoria do projeto",
             "ctime": ctime},
        ],
    }
    sub.setdefault("items", []).append(grupo)
    save_bookmarks(workspace, data)


def inject_callout_index(workspace: Path) -> None:
    """Injeta callout no _painel/index.md (idempotente por marker)."""
    index = workspace / "_painel" / "index.md"
    if not index.exists():
        return  # F2 cria o painel; F4 nao cria

    content = index.read_text(encoding="utf-8")
    if CALLOUT_MARKER in content:
        return  # ja injetado

    # Inserir callout apos frontmatter (--- ... ---) e antes do primeiro
    # bloco markdown
    if content.startswith("---"):
        # Achar fim do frontmatter
        try:
            end_fm = content.index("\n---\n", 3) + len("\n---\n")
        except ValueError:
            end_fm = 0
        new_content = content[:end_fm] + "\n" + CALLOUT_TEXT + "\n" + content[end_fm:]
    else:
        new_content = CALLOUT_TEXT + "\n" + content

    # Atomic write Markdown (mesmo padrao do JSON, write text)
    tmp = index.with_suffix(".md.tmp")
    last_err = None
    for delay in [0] + BACKOFFS:
        if delay > 0:
            time.sleep(delay)
        try:
            tmp.write_text(new_content, encoding="utf-8")
            os.replace(str(tmp), str(index))
            return
        except OSError as e:
            if getattr(e, "winerror", None) != 5 and e.errno != errno.EACCES:
                raise
            last_err = e
    sys.stderr.write(f"WRITE_FAILED|target={index}|attempts={len(BACKOFFS)+1}|last_err={last_err}\n")
    sys.exit(2)


def list_active_projetos(workspace: Path) -> list[str]:
    """Glob workspace/*/maestro/config.md e filtrar por maestro-ativo: true."""
    slugs = []
    for config in sorted(workspace.glob("*/maestro/config.md")):
        try:
            content = config.read_text(encoding="utf-8")
            # Parse simples: linha "maestro-ativo: true"
            ativo = False
            for line in content.splitlines():
                if line.strip().startswith("maestro-ativo:"):
                    ativo = "true" in line.lower()
                    break
            if ativo:
                slugs.append(config.parent.parent.name)
        except Exception:
            continue
    return slugs


def regenerate(workspace: Path) -> dict:
    """
    Garante grupo Painel da Area de Trabalho + subgrupo de cada projeto ativo.
    Detecta 2+ projetos pela 1a vez.

    B-F4-VAL-7: chama add_painel_workspace tambem (idempotente). Antes so
    chamava add_projeto_subgrupo, entao apos corrupcao + recriacao do
    bookmarks.json o grupo Painel sumia.

    Retorna:
        {"projetos": [...], "aviso_colisao_pendente": bool}
    """
    add_painel_workspace(workspace)
    slugs = list_active_projetos(workspace)
    for slug in slugs:
        add_projeto_subgrupo(workspace, slug)
        add_auditoria_grupo(workspace, slug)  # S101 — Decisão 110 (cobertura uniforme)

    # Detecao de 2+ projetos
    aviso_pendente = False
    flags_path = workspace / ".maestro-flags.md"
    if len(slugs) >= 2 and flags_path.exists():
        flags_content = flags_path.read_text(encoding="utf-8")
        # Parse simples
        if "aviso-colisao-wikilink-mostrado: false" in flags_content:
            inject_callout_index(workspace)
            aviso_pendente = True

    return {"projetos": slugs, "aviso_colisao_pendente": aviso_pendente}


# ---------- CLI ----------

def main() -> int:
    if len(sys.argv) < 3:
        sys.stderr.write("Uso: workspace_bookmarks.py scaffold|regenerate|inject-callout|library <ws> [args]\n")
        return 1

    action = sys.argv[1]
    workspace = Path(sys.argv[2]).resolve()

    if action == "scaffold":
        if len(sys.argv) < 4:
            sys.stderr.write("scaffold requer projeto-slug\n")
            return 1
        slug = sys.argv[3]
        add_painel_workspace(workspace)
        add_projeto_subgrupo(workspace, slug)
        add_auditoria_grupo(workspace, slug)  # S101 — Decisão 110
        return 0

    elif action == "regenerate":
        result = regenerate(workspace)
        # Imprimir saida estruturada pro Bibliotecario passar pro report
        print(f"projetos={','.join(result['projetos'])}")
        print(f"aviso-colisao-pendente={'true' if result['aviso_colisao_pendente'] else 'false'}")
        return 0

    elif action == "inject-callout":
        inject_callout_index(workspace)
        return 0

    elif action == "library":
        if len(sys.argv) < 5:
            sys.stderr.write("library requer projeto-slug e items-json\n")
            return 1
        slug = sys.argv[3]
        items = json.loads(sys.argv[4])
        add_library_to_projeto(workspace, slug, items)
        return 0

    else:
        sys.stderr.write(f"Acao desconhecida: {action}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
