"""
Testes unitarios do workspace_flags.
"""
import pytest

from workspace_flags import init_flags, get_flag, set_flag, FLAGS_FILENAME


def test_init_creates_file_with_template(tmp_workspace):
    init_flags(tmp_workspace)
    flags = tmp_workspace / FLAGS_FILENAME
    assert flags.exists()
    content = flags.read_text(encoding="utf-8")
    assert "tipo: maestro-flags-workspace" in content
    assert "aviso-colisao-wikilink-mostrado: false" in content
    assert "[!warning] Não edite manualmente" in content


def test_init_idempotent(tmp_workspace):
    init_flags(tmp_workspace)
    flags = tmp_workspace / FLAGS_FILENAME
    flags.write_text(flags.read_text(encoding="utf-8") + "\n# user comment\n", encoding="utf-8")
    init_flags(tmp_workspace)  # nao deve sobrescrever
    assert "# user comment" in flags.read_text(encoding="utf-8")


def test_get_flag_returns_value(tmp_workspace):
    init_flags(tmp_workspace)
    assert get_flag(tmp_workspace, "aviso-colisao-wikilink-mostrado") == "false"


def test_set_flag_updates_frontmatter(tmp_workspace):
    init_flags(tmp_workspace)
    set_flag(tmp_workspace, "aviso-colisao-wikilink-mostrado", "true")
    assert get_flag(tmp_workspace, "aviso-colisao-wikilink-mostrado") == "true"


def test_set_flag_idempotent(tmp_workspace):
    init_flags(tmp_workspace)
    set_flag(tmp_workspace, "aviso-colisao-wikilink-mostrado", "true")
    content_1 = (tmp_workspace / FLAGS_FILENAME).read_text(encoding="utf-8")
    set_flag(tmp_workspace, "aviso-colisao-wikilink-mostrado", "true")
    content_2 = (tmp_workspace / FLAGS_FILENAME).read_text(encoding="utf-8")
    # Conteudo igual (sem rewrite quando valor ja eh o pedido)
    assert content_1 == content_2


def test_set_flag_corrupted_creates_bak(tmp_workspace):
    flags = tmp_workspace / FLAGS_FILENAME
    flags.write_text("not a valid frontmatter at all", encoding="utf-8")
    set_flag(tmp_workspace, "aviso-colisao-wikilink-mostrado", "true")
    assert (tmp_workspace.parent / "test-workspace" / ".maestro-flags.md.bak").exists()
    # Recriou com template + valor pedido
    new_content = flags.read_text(encoding="utf-8")
    assert "aviso-colisao-wikilink-mostrado: true" in new_content
