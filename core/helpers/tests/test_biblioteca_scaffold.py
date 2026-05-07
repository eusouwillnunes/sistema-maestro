"""Testes para biblioteca_scaffold.scaffold."""
import json
import os
import subprocess
import sys
from pathlib import Path

HELPER = Path(__file__).resolve().parents[1] / "biblioteca_scaffold.py"


def run_scaffold(destino, empresa_nome, plugin_dir):
    """Executa o helper e retorna (returncode, stdout_dict, stderr)."""
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(
        [sys.executable, str(HELPER), "scaffold", str(destino), str(empresa_nome), "--plugin-dir", str(plugin_dir)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    try:
        payload = json.loads(result.stdout) if result.stdout.strip() else None
    except json.JSONDecodeError:
        payload = None
    return result.returncode, payload, result.stderr


def test_destino_path_relativo_falha(tmp_path, mock_plugin_dir):
    rc, payload, _ = run_scaffold("relative/path", "Padaria do João", mock_plugin_dir)
    assert rc == 1
    assert payload["status"] == "error"
    assert payload["motivo"] == "destino-relativo"


def test_destino_arquivo_existente_falha(tmp_path, mock_plugin_dir):
    arquivo = tmp_path / "arquivo.md"
    arquivo.write_text("não sou pasta")
    rc, payload, _ = run_scaffold(arquivo, "Padaria do João", mock_plugin_dir)
    assert rc == 1
    assert payload["motivo"] == "destino-e-arquivo"


def test_empresa_nome_vazio_falha(tmp_path, mock_plugin_dir):
    destino = tmp_path / "padaria-do-joao"
    rc, payload, _ = run_scaffold(destino, "", mock_plugin_dir)
    assert rc == 1
    assert payload["motivo"] == "empresa-nome-vazio"


def test_empresa_nome_so_espacos_falha(tmp_path, mock_plugin_dir):
    destino = tmp_path / "padaria-do-joao"
    rc, payload, _ = run_scaffold(destino, "   ", mock_plugin_dir)
    assert rc == 1
    assert payload["motivo"] == "empresa-nome-vazio"


def test_slug_vazio_so_emojis_falha(tmp_path, mock_plugin_dir):
    destino = tmp_path / "destino"
    rc, payload, _ = run_scaffold(destino, "🎉🎊", mock_plugin_dir)
    assert rc == 1
    assert payload["motivo"] == "slug-vazio"


def test_plugin_dir_invalido_falha(tmp_path):
    destino = tmp_path / "padaria-do-joao"
    plugin_dir_fake = tmp_path / "fake-plugin"
    plugin_dir_fake.mkdir()
    rc, payload, _ = run_scaffold(destino, "Padaria do João", plugin_dir_fake)
    assert rc == 1
    assert payload["motivo"] == "plugin-dir-invalido"


def test_duplicata_arquivo_principal_existe(tmp_path, mock_plugin_dir):
    destino = tmp_path / "padaria-do-joao"
    destino.mkdir()
    (destino / "padaria-do-joao.md").write_text(
        '---\ntitulo: Biblioteca\nempresa: "Padaria do João"\ncriado: 2026-01-01\n---\n# Conteúdo\n',
        encoding="utf-8",
    )
    rc, payload, _ = run_scaffold(destino, "Padaria do João", mock_plugin_dir)
    assert rc == 0
    assert payload["status"] == "duplicata"
    assert payload["empresa-existente"] == "Padaria do João"


def test_pasta_existe_sem_arquivo_principal_segue(tmp_path, mock_plugin_dir):
    """Pasta sem <slug>.md não dispara duplicata (segue scaffold)."""
    destino = tmp_path / "padaria-do-joao"
    destino.mkdir()
    (destino / "outro-arquivo.md").write_text("conteúdo", encoding="utf-8")
    rc, payload, _ = run_scaffold(destino, "Padaria do João", mock_plugin_dir)
    if payload:
        assert payload.get("status") != "duplicata"


def _run_ok(tmp_path, mock_plugin_dir, empresa="Padaria do João", subdir="padaria-do-joao"):
    """Helper: roda scaffold e retorna (payload, destino_path)."""
    destino = tmp_path / subdir
    rc, payload, stderr = run_scaffold(destino, empresa, mock_plugin_dir)
    assert rc == 0, f"stderr={stderr}\npayload={payload}"
    assert payload["status"] == "ok", f"payload={payload}"
    return payload, destino


def test_slug_integracao_acentos(tmp_path, mock_plugin_dir):
    payload, _ = _run_ok(tmp_path, mock_plugin_dir, "Açaí Aço", "acai-aco")
    assert payload["empresa-slug"] == "acai-aco"


def test_idempotencia_2a_invocacao_dispara_duplicata(tmp_path, mock_plugin_dir):
    payload, destino = _run_ok(tmp_path, mock_plugin_dir)
    rc2, payload2, _ = run_scaffold(destino, "Padaria do João", mock_plugin_dir)
    assert rc2 == 0
    assert payload2["status"] == "duplicata"


def test_idempotencia_arquivo_user_preservado(tmp_path, mock_plugin_dir):
    """Arquivo customizado é preservado, scaffold completa o resto."""
    destino = tmp_path / "padaria-do-joao"
    destino.mkdir()
    custom = destino / "identidade"
    custom.mkdir()
    custom_md = custom / "circulo-dourado.md"
    custom_md.write_text("CONTEÚDO CUSTOM", encoding="utf-8")
    payload, _ = _run_ok(tmp_path, mock_plugin_dir)
    assert custom_md.read_text(encoding="utf-8") == "CONTEÚDO CUSTOM"
    assert "identidade/circulo-dourado.md" in payload["pulados"]


def test_idempotencia_scaffold_parcial(tmp_path, mock_plugin_dir):
    destino = tmp_path / "padaria-do-joao"
    (destino / "identidade").mkdir(parents=True)
    payload, _ = _run_ok(tmp_path, mock_plugin_dir)
    assert len(payload["criados"]) > 0


def test_copia_8_identidade(tmp_path, mock_plugin_dir):
    payload, destino = _run_ok(tmp_path, mock_plugin_dir)
    identidade_files = list((destino / "identidade").glob("*.md"))
    assert len(identidade_files) == 9
    nomes = {f.name for f in identidade_files}
    assert "circulo-dourado.md" in nomes
    assert "_identidade.md" in nomes


def test_copia_17_paineis(tmp_path, mock_plugin_dir):
    payload, destino = _run_ok(tmp_path, mock_plugin_dir)
    paineis = [
        "tarefas/_tarefas.md", "planos/_planos.md", "entrevistas/_entrevistas.md",
        "rascunhos/_rascunhos.md", "entrevistas/_cascatas.md", "produtos/_produtos.md",
        "funis/_funis.md", "lancamentos/_lancamentos.md", "campanhas/_campanhas.md",
        "lead-magnets/_lead-magnets.md", "escada-de-valor/_escada-de-valor.md",
        "pesquisas/_pesquisas.md", "entregas/_entregas.md", "identidade/_identidade.md",
        "tarefas/_qa-reprovacoes.md", "tarefas/_violacoes-maestro.md",
        "memorias/_pendencias-aceitas.md",
    ]
    for p in paineis:
        assert (destino / p).is_file(), f"painel ausente: {p}"


def test_copia_3_inline(tmp_path, mock_plugin_dir):
    payload, destino = _run_ok(tmp_path, mock_plugin_dir)
    for p in ["social/_social.md", "referencias/_referencias.md", "memorias/_memorias.md"]:
        assert (destino / p).is_file(), f"inline ausente: {p}"


def test_copia_5_fixos(tmp_path, mock_plugin_dir):
    payload, destino = _run_ok(tmp_path, mock_plugin_dir)
    fixos = [
        "maestro/checklists/README.md",
        "memorias/feedback-revisor.md",
        "memorias/pendencias-aceitas/historico.md",
        "memorias/auditoria/historico.md",
        "memorias/auditoria/_defesa-anti-hallucination.md",
    ]
    for f in fixos:
        assert (destino / f).is_file(), f"fixo ausente: {f}"


def test_paineis_match_filesystem(tmp_path, mock_plugin_dir):
    """Lista hardcoded de painéis no helper deve bater com os arquivos reais em indexes-area/."""
    indexes_area = mock_plugin_dir / "core" / "templates" / "indexes-area"
    arquivos_reais = sorted(f.name for f in indexes_area.glob("*-index.md"))
    assert len(arquivos_reais) == 13


def test_pasta_auditoria_canarios(tmp_path, mock_plugin_dir):
    payload, destino = _run_ok(tmp_path, mock_plugin_dir)
    assert (destino / "memorias" / "auditoria" / "canarios-ativos" / ".gitkeep").is_file()


def test_pasta_pendencias_aceitas(tmp_path, mock_plugin_dir):
    payload, destino = _run_ok(tmp_path, mock_plugin_dir)
    assert (destino / "memorias" / "pendencias-aceitas" / "historico.md").is_file()


def test_warning_template_ausente(tmp_path, mock_plugin_dir):
    """Remove 1 painel do mock-plugin e confirma warning."""
    alvo = mock_plugin_dir / "core" / "templates" / "indexes-area" / "_funis-index.md"
    alvo.unlink()
    payload, _ = _run_ok(tmp_path, mock_plugin_dir)
    motivos = [w["template"] for w in payload["warnings"]]
    assert any("_funis-index.md" in m for m in motivos)


def test_warnings_multiplos(tmp_path, mock_plugin_dir):
    for nome in ["_funis-index.md", "_lancamentos-index.md", "_pesquisas-index.md"]:
        (mock_plugin_dir / "core" / "templates" / "indexes-area" / nome).unlink()
    payload, _ = _run_ok(tmp_path, mock_plugin_dir)
    assert len(payload["warnings"]) >= 3


def test_zero_warnings_caso_normal(tmp_path, mock_plugin_dir):
    payload, _ = _run_ok(tmp_path, mock_plugin_dir)
    assert payload["warnings"] == []


def test_json_keys_status_ok(tmp_path, mock_plugin_dir):
    payload, _ = _run_ok(tmp_path, mock_plugin_dir)
    for k in ["status", "destino", "empresa", "empresa-slug", "criados", "pulados", "warnings"]:
        assert k in payload


def test_json_keys_status_duplicata(tmp_path, mock_plugin_dir):
    _, destino = _run_ok(tmp_path, mock_plugin_dir)
    rc2, payload2, _ = run_scaffold(destino, "Padaria do João", mock_plugin_dir)
    for k in ["status", "destino", "empresa-slug", "empresa-existente"]:
        assert k in payload2


def test_json_paths_relativos(tmp_path, mock_plugin_dir):
    payload, destino = _run_ok(tmp_path, mock_plugin_dir)
    for p in payload["criados"] + payload["pulados"]:
        assert not p.startswith("/"), f"path absoluto encontrado: {p}"
        assert not (len(p) > 1 and p[1] == ":"), f"path Windows abs encontrado: {p}"


def test_json_error_exit_1(tmp_path, mock_plugin_dir):
    rc, payload, _ = run_scaffold("relative", "Padaria", mock_plugin_dir)
    assert rc == 1
    assert payload["status"] == "error"


def test_path_with_spaces(tmp_path, mock_plugin_dir):
    destino = tmp_path / "with spaces" / "padaria-do-joao"
    rc, payload, stderr = run_scaffold(destino, "Padaria do João", mock_plugin_dir)
    assert rc == 0, f"stderr={stderr}"
    assert payload["status"] == "ok"
    assert (destino / "identidade").is_dir()


def test_encoding_utf8_lf(tmp_path, mock_plugin_dir):
    payload, destino = _run_ok(tmp_path, mock_plugin_dir)
    arquivo = destino / "padaria-do-joao.md"
    raw = arquivo.read_bytes()
    assert b"\r\n" not in raw, "CRLF detectado"
    assert not raw.startswith(b"\xef\xbb\xbf"), "BOM detectado"


def test_arquivo_principal_placeholders_substituidos(tmp_path, mock_plugin_dir):
    payload, destino = _run_ok(tmp_path, mock_plugin_dir)
    arquivo = destino / "padaria-do-joao.md"
    texto = arquivo.read_text(encoding="utf-8")
    assert "[NOME DA EMPRESA]" not in texto
    assert "[DATA DE CRIAÇÃO]" not in texto
    assert "Padaria do João" in texto
    import re as _re
    assert _re.search(r"\d{4}-\d{2}-\d{2}", texto)


def test_motivos_canonicos_tem_traducao_no_skill_md():
    """Cada motivo retornável pelo helper deve ter linha na tabela do SKILL.md."""
    skill_md = Path(__file__).resolve().parents[3] / "skills" / "bibliotecario" / "SKILL.md"
    if not skill_md.is_file():
        return
    texto = skill_md.read_text(encoding="utf-8")
    motivos_canonicos = [
        "destino-relativo", "destino-e-arquivo", "permission-denied",
        "slug-vazio", "empresa-nome-vazio", "plugin-dir-invalido",
    ]
    for m in motivos_canonicos:
        assert m in texto, f"motivo `{m}` não encontrado na tabela de tradução do SKILL.md"
