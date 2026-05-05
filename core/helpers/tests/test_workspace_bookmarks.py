"""
Testes unitarios do workspace_bookmarks.
"""
import json
import os
import sys
import time
from pathlib import Path

import pytest

from workspace_bookmarks import (
    atomic_write_json,
    load_bookmarks,
    has_path_anywhere,
    has_group_at_root,
    add_painel_workspace,
    add_projeto_subgrupo,
    inject_callout_index,
    add_library_to_projeto,
)


# ---------- atomic_write_json ----------

def test_atomic_write_creates_file(tmp_path):
    target = tmp_path / "bm.json"
    atomic_write_json(target, {"items": [{"x": 1}]})
    assert json.loads(target.read_text(encoding="utf-8"))["items"][0]["x"] == 1


def test_atomic_write_overwrites_existing(tmp_path):
    target = tmp_path / "bm.json"
    target.write_text('{"items": [{"old": true}]}', encoding="utf-8")
    atomic_write_json(target, {"items": [{"new": True}]})
    assert json.loads(target.read_text(encoding="utf-8"))["items"][0]["new"] is True


def test_atomic_write_indent_2_ensure_ascii_false(tmp_path):
    target = tmp_path / "bm.json"
    atomic_write_json(target, {"items": [{"emoji": "📊"}]})
    content = target.read_text(encoding="utf-8")
    assert "📊" in content  # nao escapa unicode
    assert content.count("\n") > 1  # indentado


# ---------- load_bookmarks ----------

def test_load_bookmarks_existing(tmp_workspace):
    data = load_bookmarks(tmp_workspace)
    assert data == {"items": []}


def test_load_bookmarks_missing_returns_empty(tmp_workspace):
    (tmp_workspace / ".obsidian" / "bookmarks.json").unlink()
    data = load_bookmarks(tmp_workspace)
    assert data == {"items": []}


def test_load_bookmarks_corrupted_creates_bak(tmp_workspace):
    bm = tmp_workspace / ".obsidian" / "bookmarks.json"
    bm.write_text("{not json", encoding="utf-8")
    data = load_bookmarks(tmp_workspace)
    assert data == {"items": []}
    assert (tmp_workspace / ".obsidian" / "bookmarks.json.bak").exists()


# ---------- has_path_anywhere ----------

def test_has_path_anywhere_finds_nested(tmp_workspace):
    data = {
        "items": [
            {"type": "group", "title": "X", "items": [
                {"type": "file", "path": "deep/nested/file.md"}
            ]}
        ]
    }
    assert has_path_anywhere(data, "deep/nested/file.md") is True
    assert has_path_anywhere(data, "missing.md") is False


# ---------- merge idempotente ----------

def test_add_painel_workspace_idempotent(tmp_workspace):
    add_painel_workspace(tmp_workspace)
    data1 = load_bookmarks(tmp_workspace)
    add_painel_workspace(tmp_workspace)
    data2 = load_bookmarks(tmp_workspace)
    assert data1 == data2  # 2a chamada nao duplica


def test_add_painel_workspace_creates_3_items(tmp_workspace):
    add_painel_workspace(tmp_workspace)
    data = load_bookmarks(tmp_workspace)
    grupo = next((g for g in data["items"] if g.get("title", "").startswith("📊")), None)
    assert grupo is not None
    paths = [i.get("path") for i in grupo["items"]]
    assert "_painel/index.md" in paths
    assert "_painel/tarefas.md" in paths
    assert "_painel/grafo.md" in paths


def test_add_projeto_subgrupo_idempotent(tmp_workspace):
    add_projeto_subgrupo(tmp_workspace, "cliente-a")
    data1 = load_bookmarks(tmp_workspace)
    add_projeto_subgrupo(tmp_workspace, "cliente-a")
    data2 = load_bookmarks(tmp_workspace)
    assert data1 == data2


def test_add_projeto_subgrupo_creates_painel_pasta_biblioteca(tmp_workspace):
    add_projeto_subgrupo(tmp_workspace, "cliente-a")
    data = load_bookmarks(tmp_workspace)
    projetos = next(g for g in data["items"] if g.get("title") == "📁 Projetos")
    sub = next(g for g in projetos["items"] if g.get("title") == "cliente-a")
    titles = [i.get("title") for i in sub["items"]]
    assert "📊 Painel do projeto" in titles
    assert "📂 Pasta" in titles
    assert "📚 Biblioteca" in titles


# ---------- inject_callout_index ----------

def test_inject_callout_idempotent(tmp_workspace):
    painel = tmp_workspace / "_painel"
    painel.mkdir(exist_ok=True)
    index = painel / "index.md"
    index.write_text("---\ntipo: painel-workspace\n---\n\n# Index\n\n```dataview\nTABLE x\n```\n",
                     encoding="utf-8")

    inject_callout_index(tmp_workspace)
    content_1 = index.read_text(encoding="utf-8")
    inject_callout_index(tmp_workspace)
    content_2 = index.read_text(encoding="utf-8")

    assert content_1 == content_2  # idempotente
    assert "<!-- MAESTRO_CALLOUT_COLISAO -->" in content_1
    assert "Nomes iguais entre projetos" in content_1


# ---------- add_library_to_projeto ----------

def test_add_library_aninhado_em_projetos(tmp_workspace):
    add_painel_workspace(tmp_workspace)
    add_projeto_subgrupo(tmp_workspace, "cliente-a")

    biblioteca_items = [
        {"type": "file", "path": "cliente-a/identidade/_identidade.md", "title": "Identidade"}
    ]
    add_library_to_projeto(tmp_workspace, "cliente-a", biblioteca_items)

    data = load_bookmarks(tmp_workspace)
    projetos = next(g for g in data["items"] if g.get("title") == "📁 Projetos")
    sub = next(g for g in projetos["items"] if g.get("title") == "cliente-a")
    biblioteca = next(g for g in sub["items"] if g.get("title") == "📚 Biblioteca")
    assert any(i.get("path") == "cliente-a/identidade/_identidade.md" for i in biblioteca["items"])


def test_add_library_idempotente_por_path(tmp_workspace):
    add_painel_workspace(tmp_workspace)
    add_projeto_subgrupo(tmp_workspace, "cliente-a")

    item = {"type": "file", "path": "cliente-a/identidade/_identidade.md", "title": "Identidade"}
    add_library_to_projeto(tmp_workspace, "cliente-a", [item])
    add_library_to_projeto(tmp_workspace, "cliente-a", [item])

    data = load_bookmarks(tmp_workspace)
    projetos = next(g for g in data["items"] if g.get("title") == "📁 Projetos")
    sub = next(g for g in projetos["items"] if g.get("title") == "cliente-a")
    biblioteca = next(g for g in sub["items"] if g.get("title") == "📚 Biblioteca")
    paths = [i.get("path") for i in biblioteca["items"]]
    assert paths.count("cliente-a/identidade/_identidade.md") == 1


# ---------- regenerate ----------

def test_regenerate_recria_painel_workspace_apos_recriacao(tmp_workspace, add_projeto):
    """B-F4-VAL-7: regenerate deve garantir grupo Painel da Area de Trabalho
    mesmo quando bookmarks.json foi recriado do zero (apos corrupcao)."""
    from workspace_bookmarks import regenerate

    # bookmarks.json começa vazio (simula recém-recriado pós-corrupção)
    assert load_bookmarks(tmp_workspace) == {"items": []}

    # adiciona 2 projetos pra exercitar fluxo
    add_projeto("cliente-b")

    regenerate(tmp_workspace)
    data = load_bookmarks(tmp_workspace)

    # Deve ter ambos: Painel da Área de Trabalho + Projetos
    titulos = [i.get("title", "") for i in data["items"]]
    assert any("Painel da Área de Trabalho" in t for t in titulos), f"Painel ausente: {titulos}"
    assert any("Projetos" in t for t in titulos), f"Projetos ausente: {titulos}"
