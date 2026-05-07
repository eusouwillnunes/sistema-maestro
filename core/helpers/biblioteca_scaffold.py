#!/usr/bin/env python3
"""
Helper de scaffold da Biblioteca de Marketing pro Sistema Maestro.

Cria estrutura completa de pastas e templates dentro de <destino>:
- ~21 pastas
- 8 templates de identidade
- 17 painéis Dataview (com rename `_X-index.md` → `_X.md`)
- 3 indexes inline (social, referencias, memorias)
- 5 fixos (readmes + auditoria + pendências)
- Arquivo principal `<empresa-slug>.md` com placeholders substituídos

Uso:
  python biblioteca_scaffold.py scaffold <destino-abs> "<empresa-nome>" --plugin-dir <plugin-abs>

Saída: JSON em stdout. Exit 0 ok/duplicata, 1 erro fatal.
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

# Import de _slug compartilhado
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _slug import slugify  # noqa: E402


# Códigos canônicos de motivo (alinhados com a tabela de tradução do SKILL.md)
MOTIVO_DESTINO_RELATIVO = "destino-relativo"
MOTIVO_DESTINO_E_ARQUIVO = "destino-e-arquivo"
MOTIVO_PLUGIN_DIR_INVALIDO = "plugin-dir-invalido"
MOTIVO_EMPRESA_NOME_VAZIO = "empresa-nome-vazio"
MOTIVO_SLUG_VAZIO = "slug-vazio"
MOTIVO_PERMISSION_DENIED = "permission-denied"
MOTIVO_IO_ERROR = "io-error"


def emit_error(motivo: str, detalhes: str = "") -> None:
    """Imprime JSON de erro em stdout e sai com exit 1."""
    payload = {"status": "error", "motivo": motivo}
    if detalhes:
        payload["detalhes"] = detalhes
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(1)


def check_duplicata(destino: Path, empresa_slug: str) -> str | None:
    """
    Retorna o valor do campo `empresa:` no frontmatter de <destino>/<empresa-slug>.md
    se o arquivo existe e tem esse campo. Senão retorna None.
    """
    arquivo = destino / f"{empresa_slug}.md"
    if not arquivo.is_file():
        return None
    try:
        conteudo = arquivo.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not conteudo.startswith("---"):
        return None
    try:
        end_idx = conteudo.index("\n---", 3)
    except ValueError:
        return None
    frontmatter = conteudo[3:end_idx]
    for linha in frontmatter.splitlines():
        linha = linha.strip()
        if linha.startswith("empresa:"):
            valor = linha[len("empresa:"):].strip().strip('"').strip("'")
            return valor or None
    return None


def main() -> None:
    parser = argparse.ArgumentParser(prog="biblioteca_scaffold")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scaffold = sub.add_parser("scaffold", help="Cria scaffold da biblioteca")
    p_scaffold.add_argument("destino", help="Path absoluto da pasta destino")
    p_scaffold.add_argument("empresa_nome", help="Nome legível da empresa")
    p_scaffold.add_argument("--plugin-dir", required=True, help="Path absoluto do plugin instalado")

    args = parser.parse_args()

    if args.cmd == "scaffold":
        scaffold(args.destino, args.empresa_nome, args.plugin_dir)


def scaffold(destino_arg: str, empresa_nome: str, plugin_dir_arg: str) -> None:
    # 1. Validar argumentos
    destino = Path(destino_arg)
    if not destino.is_absolute():
        emit_error(MOTIVO_DESTINO_RELATIVO, f"recebido: {destino_arg}")

    if destino.exists() and not destino.is_dir():
        emit_error(MOTIVO_DESTINO_E_ARQUIVO, f"path existe e é arquivo: {destino_arg}")

    if not empresa_nome or not empresa_nome.strip():
        emit_error(MOTIVO_EMPRESA_NOME_VAZIO)

    plugin_dir = Path(plugin_dir_arg)
    biblioteca_templates = plugin_dir / "core" / "templates" / "biblioteca-de-marketing"
    if not biblioteca_templates.is_dir():
        emit_error(MOTIVO_PLUGIN_DIR_INVALIDO, f"esperado: {biblioteca_templates}")

    # 2. Calcular slug
    empresa_slug = slugify(empresa_nome.strip())
    if not empresa_slug:
        emit_error(MOTIVO_SLUG_VAZIO, f"nome contém só símbolos/emojis: {empresa_nome!r}")

    # 3. Pre-check duplicata
    duplicata = check_duplicata(destino, empresa_slug)
    if duplicata:
        payload = {
            "status": "duplicata",
            "destino": str(destino),
            "empresa-slug": empresa_slug,
            "empresa-existente": duplicata,
        }
        print(json.dumps(payload, ensure_ascii=False))
        sys.exit(0)

    # 4. Coletar resultado
    criados: list[str] = []
    pulados: list[str] = []
    warnings: list[dict] = []

    # 5. Criar pasta destino
    try:
        destino.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        emit_error(MOTIVO_PERMISSION_DENIED, str(e))
    except OSError as e:
        emit_error(MOTIVO_IO_ERROR, str(e))

    # 6. Criar árvore de pastas
    pastas = [
        "identidade", "produtos", "escada-de-valor", "lead-magnets",
        "funis", "lancamentos", "campanhas", "social", "referencias",
        "pesquisas", "entregas", "tarefas", "planos", "entrevistas",
        "rascunhos",
        "memorias",
        "memorias/auditoria",
        "memorias/auditoria/canarios-ativos",
        "memorias/pendencias-aceitas",
        "maestro",
        "maestro/checklists",
    ]
    for p in pastas:
        (destino / p).mkdir(parents=True, exist_ok=True)

    # 7. Copiar 8 templates de identidade
    identidade_src = plugin_dir / "core" / "templates" / "biblioteca-de-marketing" / "preenchimento" / "identidade"
    if identidade_src.is_dir():
        for tpl in identidade_src.glob("*.md"):
            dst = destino / "identidade" / tpl.name
            _copy_idempotent(tpl, dst, destino, criados, pulados, warnings)
    else:
        warnings.append({"template": str(identidade_src), "motivo": "ausente"})

    # 8. Copiar 17 painéis Dataview (com rename _X-index.md → _X.md)
    paineis = [
        ("_tarefas-index.md", "tarefas/_tarefas.md"),
        ("_planos-index.md", "planos/_planos.md"),
        ("_entrevistas-index.md", "entrevistas/_entrevistas.md"),
        ("_rascunhos-index.md", "rascunhos/_rascunhos.md"),
        ("indexes-area/_cascatas-index.md", "entrevistas/_cascatas.md"),
        ("indexes-area/_produtos-index.md", "produtos/_produtos.md"),
        ("indexes-area/_funis-index.md", "funis/_funis.md"),
        ("indexes-area/_lancamentos-index.md", "lancamentos/_lancamentos.md"),
        ("indexes-area/_campanhas-index.md", "campanhas/_campanhas.md"),
        ("indexes-area/_lead-magnets-index.md", "lead-magnets/_lead-magnets.md"),
        ("indexes-area/_escada-de-valor-index.md", "escada-de-valor/_escada-de-valor.md"),
        ("indexes-area/_pesquisas-index.md", "pesquisas/_pesquisas.md"),
        ("indexes-area/_entregas-index.md", "entregas/_entregas.md"),
        ("indexes-area/_identidade-index.md", "identidade/_identidade.md"),
        ("indexes-area/_qa-reprovacoes-index.md", "tarefas/_qa-reprovacoes.md"),
        ("indexes-area/_violacoes-maestro-index.md", "tarefas/_violacoes-maestro.md"),
        ("indexes-area/_pendencias-aceitas-index.md", "memorias/_pendencias-aceitas.md"),
    ]
    templates_root = plugin_dir / "core" / "templates"
    for src_rel, dst_rel in paineis:
        src = templates_root / src_rel
        dst = destino / dst_rel
        _copy_idempotent(src, dst, destino, criados, pulados, warnings)

    # 9. Copiar 3 indexes inline novos
    inline_root = biblioteca_templates / "inline"
    for fname, dst_rel in [
        ("_social.md", "social/_social.md"),
        ("_referencias.md", "referencias/_referencias.md"),
        ("_memorias.md", "memorias/_memorias.md"),
    ]:
        _copy_idempotent(inline_root / fname, destino / dst_rel, destino, criados, pulados, warnings)

    # 10. Copiar arquivos fixos (5)
    fixos = [
        (templates_root / "_readme-checklists-projeto.md", "maestro/checklists/README.md"),
        (templates_root / "_feedback-revisor-template.md", "memorias/feedback-revisor.md"),
        (templates_root / "_pendencias-aceitas-historico-template.md", "memorias/pendencias-aceitas/historico.md"),
        (biblioteca_templates / "auditoria" / "_historico.md", "memorias/auditoria/historico.md"),
        (biblioteca_templates / "auditoria" / "_defesa-anti-hallucination.md", "memorias/auditoria/_defesa-anti-hallucination.md"),
    ]
    for src, dst_rel in fixos:
        _copy_idempotent(src, destino / dst_rel, destino, criados, pulados, warnings)

    # 11. .gitkeep em canarios-ativos/
    gitkeep = destino / "memorias" / "auditoria" / "canarios-ativos" / ".gitkeep"
    rel_gitkeep = str(gitkeep.relative_to(destino)).replace("\\", "/")
    if gitkeep.exists():
        pulados.append(rel_gitkeep)
    else:
        gitkeep.write_text("", encoding="utf-8", newline="\n")
        criados.append(rel_gitkeep)

    # 12. Escrever arquivo principal <empresa-slug>.md com placeholders substituídos
    principal_src = biblioteca_templates / "_index-biblioteca.md"
    principal_dst = destino / f"{empresa_slug}.md"
    if principal_dst.exists():
        pulados.append(f"{empresa_slug}.md")
    elif principal_src.is_file():
        try:
            template_text = principal_src.read_text(encoding="utf-8")
        except OSError as e:
            emit_error(MOTIVO_IO_ERROR, str(e))
        rendered = template_text.replace("[NOME DA EMPRESA]", empresa_nome.strip())
        rendered = rendered.replace("[DATA DE CRIAÇÃO]", date.today().isoformat())
        principal_dst.write_text(rendered, encoding="utf-8", newline="\n")
        criados.append(f"{empresa_slug}.md")
    else:
        warnings.append({"template": str(principal_src), "motivo": "ausente"})

    # 13. Saída final
    payload = {
        "status": "ok",
        "destino": str(destino),
        "empresa": empresa_nome.strip(),
        "empresa-slug": empresa_slug,
        "criados": sorted(criados),
        "pulados": sorted(pulados),
        "warnings": warnings,
    }
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(0)


def _copy_idempotent(
    src: Path, dst: Path, base: Path,
    criados: list[str], pulados: list[str], warnings: list[dict],
) -> None:
    """Copia src→dst preservando UTF-8 LF. Pula se dst existe. Anota warning se src ausente."""
    rel = str(dst.relative_to(base)).replace("\\", "/")
    if dst.exists():
        pulados.append(rel)
        return
    if not src.is_file():
        warnings.append({"template": str(src), "motivo": "ausente"})
        return
    try:
        text = src.read_text(encoding="utf-8", errors="replace")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8", newline="\n")
        criados.append(rel)
    except PermissionError as e:
        emit_error(MOTIVO_PERMISSION_DENIED, str(e))
    except OSError as e:
        emit_error(MOTIVO_IO_ERROR, str(e))


if __name__ == "__main__":
    main()
