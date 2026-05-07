"""
Fixtures pytest pra testes dos helpers da F4.
"""
import os
import shutil
import sys
from pathlib import Path

import pytest

# Permitir import dos helpers sem instalar pacote
HELPERS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HELPERS_DIR))


@pytest.fixture
def tmp_workspace(tmp_path: Path) -> Path:
    """
    Cria workspace sintetica com:
      - .maestro-workspace marker
      - .obsidian/ com bookmarks.json vazio
      - 1 projeto (cliente-a) com maestro/config.md
    """
    ws = tmp_path / "test-workspace"
    ws.mkdir()
    (ws / ".maestro-workspace").write_text(
        "# Marker do Sistema Maestro — workspace.\n", encoding="utf-8"
    )
    (ws / ".obsidian").mkdir()
    (ws / ".obsidian" / "bookmarks.json").write_text(
        '{"items": []}', encoding="utf-8"
    )
    projeto = ws / "cliente-a"
    (projeto / "maestro").mkdir(parents=True)
    (projeto / "maestro" / "config.md").write_text(
        "---\nempresa: cliente-a\nmaestro-ativo: true\nslug: cliente-a\n---\n",
        encoding="utf-8",
    )
    return ws


@pytest.fixture
def tmp_home(tmp_path: Path, monkeypatch) -> Path:
    """
    Sobrescreve Path.home() pra apontar pra tmp_path/.maestro-home/.
    Helpers usam Path.home() / .maestro / scaffold-*.lock.
    """
    home = tmp_path / ".maestro-home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))  # Windows
    monkeypatch.setattr(Path, "home", lambda: home)
    return home


@pytest.fixture
def add_projeto(tmp_workspace):
    """Helper pra adicionar projetos extras na workspace sintetica."""
    def _add(slug: str, ativo: bool = True):
        p = tmp_workspace / slug
        (p / "maestro").mkdir(parents=True, exist_ok=True)
        (p / "maestro" / "config.md").write_text(
            f"---\nempresa: {slug}\nmaestro-ativo: {str(ativo).lower()}\nslug: {slug}\n---\n",
            encoding="utf-8",
        )
        return p
    return _add


@pytest.fixture
def tmp_state_dir(tmp_path: Path) -> Path:
    """
    Cria diretório sintético pra testes de onboarding_state.
    Estrutura:
      <tmp>/projeto-x/memorias/onboarding/
    """
    state_dir = tmp_path / "projeto-x" / "memorias" / "onboarding"
    state_dir.mkdir(parents=True)
    (state_dir / "concluidos").mkdir()
    return state_dir


@pytest.fixture
def mock_plugin_dir(tmp_path: Path) -> Path:
    """
    Cria cópia parcial dos templates do plugin pra teste isolado do biblioteca_scaffold.
    Estrutura: <tmp>/mock-plugin/core/templates/...
    """
    plugin_root = Path(__file__).resolve().parents[3]
    src_templates = plugin_root / "core" / "templates"
    dst_plugin = tmp_path / "mock-plugin"
    dst_templates = dst_plugin / "core" / "templates"
    dst_templates.mkdir(parents=True)

    # Copia diretórios completos que o helper precisa
    shutil.copytree(src_templates / "biblioteca-de-marketing", dst_templates / "biblioteca-de-marketing")
    shutil.copytree(src_templates / "indexes-area", dst_templates / "indexes-area")

    # Copia arquivos de raiz necessários
    for fname in [
        "_tarefas-index.md",
        "_planos-index.md",
        "_entrevistas-index.md",
        "_rascunhos-index.md",
        "_readme-checklists-projeto.md",
        "_feedback-revisor-template.md",
        "_pendencias-aceitas-historico-template.md",
    ]:
        src = src_templates / fname
        if src.exists():
            shutil.copy(src, dst_templates / fname)

    return dst_plugin
