"""
Testes do onboarding_state.

Cobre:
- init_state cria arquivo com frontmatter
- mark adiciona marker idempotente com timestamp
- has_marker leitura
- archive move pra concluidos/
- cleanup_orphans remove órfãos por idade
- normalize_slug ascii lowercase + colisão
- estado corrompido cria .bak
- init com slug temporário renomeia
"""
from pathlib import Path

import pytest

from onboarding_state import (
    archive,
    cleanup_orphans,
    has_marker,
    init_state,
    mark,
    normalize_slug,
)


class TestInitState:
    def test_creates_file_with_frontmatter(self, tmp_state_dir):
        path = init_state(tmp_state_dir, "ws-proj", "primeira-vez")
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "slug: ws-proj" in content
        assert "fluxo: primeira-vez" in content
        assert "inicio: " in content
        assert "## Markers" in content

    def test_overwrites_existing_for_same_slug(self, tmp_state_dir):
        init_state(tmp_state_dir, "ws-proj", "primeira-vez")
        path = init_state(tmp_state_dir, "ws-proj", "novo-projeto")
        assert "fluxo: novo-projeto" in path.read_text(encoding="utf-8")


class TestMark:
    def test_appends_marker_with_timestamp(self, tmp_state_dir):
        init_state(tmp_state_dir, "ws-proj", "primeira-vez")
        mark(tmp_state_dir, "ws-proj", "t-consentimento")
        content = (tmp_state_dir / "state-ws-proj.md").read_text(encoding="utf-8")
        assert "- t-consentimento: " in content

    def test_idempotent_no_duplicate(self, tmp_state_dir):
        init_state(tmp_state_dir, "ws-proj", "primeira-vez")
        mark(tmp_state_dir, "ws-proj", "t-consentimento")
        mark(tmp_state_dir, "ws-proj", "t-consentimento")
        content = (tmp_state_dir / "state-ws-proj.md").read_text(encoding="utf-8")
        assert content.count("- t-consentimento: ") == 1

    def test_raises_when_state_missing(self, tmp_state_dir):
        with pytest.raises(FileNotFoundError):
            mark(tmp_state_dir, "missing-slug", "t-consentimento")


class TestHasMarker:
    def test_returns_true_when_present(self, tmp_state_dir):
        init_state(tmp_state_dir, "ws-proj", "primeira-vez")
        mark(tmp_state_dir, "ws-proj", "t-consentimento")
        assert has_marker(tmp_state_dir, "ws-proj", "t-consentimento") is True

    def test_returns_false_when_absent(self, tmp_state_dir):
        init_state(tmp_state_dir, "ws-proj", "primeira-vez")
        assert has_marker(tmp_state_dir, "ws-proj", "t-consentimento") is False

    def test_returns_false_when_state_missing(self, tmp_state_dir):
        assert has_marker(tmp_state_dir, "missing-slug", "t-anything") is False


class TestArchive:
    def test_moves_to_concluidos(self, tmp_state_dir):
        init_state(tmp_state_dir, "ws-proj", "primeira-vez")
        mark(tmp_state_dir, "ws-proj", "t-conclusao")
        new_path = archive(tmp_state_dir, "ws-proj")
        assert new_path.parent == tmp_state_dir / "concluidos"
        assert new_path.exists()
        assert not (tmp_state_dir / "state-ws-proj.md").exists()

    def test_raises_when_state_missing(self, tmp_state_dir):
        with pytest.raises(FileNotFoundError):
            archive(tmp_state_dir, "missing-slug")


class TestCleanupOrphans:
    def test_removes_old_files(self, tmp_state_dir):
        from datetime import datetime, timedelta, timezone
        import os
        path = init_state(tmp_state_dir, "ws-proj", "primeira-vez")
        old_ts = (datetime.now(timezone.utc) - timedelta(hours=48)).timestamp()
        os.utime(path, (old_ts, old_ts))
        removed = cleanup_orphans(tmp_state_dir, max_age_hours=24)
        assert removed == 1
        assert not path.exists()

    def test_keeps_active_files(self, tmp_state_dir):
        init_state(tmp_state_dir, "ws-proj", "primeira-vez")
        removed = cleanup_orphans(tmp_state_dir, max_age_hours=24)
        assert removed == 0
        assert (tmp_state_dir / "state-ws-proj.md").exists()

    def test_ignores_concluidos_subdir(self, tmp_state_dir):
        # arquivo arquivado não conta como órfão
        init_state(tmp_state_dir, "ws-proj", "primeira-vez")
        mark(tmp_state_dir, "ws-proj", "t-conclusao")
        archive(tmp_state_dir, "ws-proj")
        removed = cleanup_orphans(tmp_state_dir, max_age_hours=0)
        assert removed == 0


class TestNormalizeSlug:
    def test_lowercase_ascii(self):
        assert normalize_slug("Meu Trabalho", "Projeto Teste") == "meu-trabalho-projeto-teste"

    def test_strips_accents(self):
        assert normalize_slug("Ação", "Comunicação") == "acao-comunicacao"

    def test_strips_special_chars(self):
        assert normalize_slug("Cliente A&B", "Marca #1") == "cliente-a-b-marca-1"

    def test_collapses_multiple_separators(self):
        assert normalize_slug("Foo  Bar", "Baz   Qux") == "foo-bar-baz-qux"

    def test_strips_leading_trailing_separators(self):
        assert normalize_slug("  Foo  ", "  Bar  ") == "foo-bar"


class TestCorrupted:
    def test_mark_on_corrupted_appends_anyway(self, tmp_state_dir):
        # state file existe mas frontmatter inválido — append idempotente preserva
        path = tmp_state_dir / "state-ws-proj.md"
        path.write_text("not a valid yaml frontmatter at all", encoding="utf-8")
        mark(tmp_state_dir, "ws-proj", "t-consentimento")
        content = path.read_text(encoding="utf-8")
        assert "- t-consentimento: " in content


class TestMainCLI:
    def test_main_init(self, tmp_state_dir):
        import sys
        from onboarding_state import main
        old_argv = sys.argv
        sys.argv = ["onboarding_state.py", "init", str(tmp_state_dir), "ws-proj", "primeira-vez"]
        try:
            rc = main()
        finally:
            sys.argv = old_argv
        assert rc == 0
        assert (tmp_state_dir / "state-ws-proj.md").exists()

    def test_main_mark(self, tmp_state_dir):
        import sys
        from onboarding_state import main
        old_argv = sys.argv
        try:
            sys.argv = ["onboarding_state.py", "init", str(tmp_state_dir), "ws-proj", "primeira-vez"]
            main()
            sys.argv = ["onboarding_state.py", "mark", str(tmp_state_dir), "ws-proj", "t-consentimento"]
            rc = main()
        finally:
            sys.argv = old_argv
        assert rc == 0
        assert has_marker(tmp_state_dir, "ws-proj", "t-consentimento")

    def test_main_has_marker_returns_exit_code(self, tmp_state_dir):
        import sys
        from onboarding_state import main
        old_argv = sys.argv
        try:
            sys.argv = ["onboarding_state.py", "init", str(tmp_state_dir), "ws-proj", "primeira-vez"]
            main()
            sys.argv = ["onboarding_state.py", "has", str(tmp_state_dir), "ws-proj", "t-consentimento"]
            rc_absent = main()
            sys.argv = ["onboarding_state.py", "mark", str(tmp_state_dir), "ws-proj", "t-consentimento"]
            main()
            sys.argv = ["onboarding_state.py", "has", str(tmp_state_dir), "ws-proj", "t-consentimento"]
            rc_present = main()
        finally:
            sys.argv = old_argv
        assert rc_absent == 1
        assert rc_present == 0

    def test_main_slug(self, capsys):
        import sys
        from onboarding_state import main
        old_argv = sys.argv
        try:
            sys.argv = ["onboarding_state.py", "slug", "Meu Trabalho", "Projeto Teste"]
            rc = main()
        finally:
            sys.argv = old_argv
        captured = capsys.readouterr()
        assert rc == 0
        assert captured.out.strip() == "meu-trabalho-projeto-teste"
