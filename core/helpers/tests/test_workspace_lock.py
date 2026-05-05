"""
Testes unitarios do workspace_lock.

Cobre:
- Acquire e release basicos
- Idempotencia de release (FileNotFoundError ignorado)
- Timestamp-based orphan detection (cap 60s configuravel via param)
- O_CREAT | O_EXCL atomic creation (corrida de 2 processos)
- Timeout (max_wait_s)
- MD5 do path (forward slash normalization Windows)
- Erro estruturado em stderr no timeout
"""
import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from workspace_lock import acquire_lock, release_lock, lock_path_for


def test_acquire_creates_lock_file(tmp_workspace, tmp_home):
    acquire_lock(tmp_workspace)
    lock = lock_path_for(tmp_workspace)
    assert lock.exists()
    content = lock.read_text(encoding="utf-8").splitlines()
    assert int(content[0]) == os.getpid()
    assert int(content[1]) > 1700000000000  # epoch ms recente


def test_release_removes_lock(tmp_workspace, tmp_home):
    acquire_lock(tmp_workspace)
    release_lock(tmp_workspace)
    assert not lock_path_for(tmp_workspace).exists()


def test_release_idempotent_when_lock_missing(tmp_workspace, tmp_home):
    # nao deve raise mesmo se o lock nao existir
    release_lock(tmp_workspace)


def test_lock_path_normalizes_windows_separators(tmp_home, monkeypatch):
    # Normalizacao backslash -> forward slash antes de MD5
    fake_path = Path("C:\\some\\workspace")
    expected_md5 = hashlib.md5(b"C:/some/workspace").hexdigest()
    lock = lock_path_for(fake_path)
    assert expected_md5 in str(lock)


def test_orphan_detection_by_timestamp(tmp_workspace, tmp_home):
    # Forjar lock com timestamp 70s no passado
    lock = lock_path_for(tmp_workspace)
    lock.parent.mkdir(parents=True, exist_ok=True)
    old_ms = int(time.time() * 1000) - 70_000
    lock.write_text(f"999999\n{old_ms}\n", encoding="utf-8")

    # Acquire deve detectar orfao, apagar e seguir
    acquire_lock(tmp_workspace, max_wait_s=5, orphan_age_s=60)
    content = lock.read_text(encoding="utf-8").splitlines()
    assert int(content[0]) == os.getpid()  # nosso PID, nao 999999
    release_lock(tmp_workspace)


def test_active_lock_blocks_until_timeout(tmp_workspace, tmp_home):
    # Forjar lock recente com PID falso ainda dentro do cap
    lock = lock_path_for(tmp_workspace)
    lock.parent.mkdir(parents=True, exist_ok=True)
    recent_ms = int(time.time() * 1000)  # agora
    lock.write_text(f"999999\n{recent_ms}\n", encoding="utf-8")

    # Esperar por 2s (max_wait), depois deve sair com SystemExit(2)
    start = time.time()
    with pytest.raises(SystemExit) as exc:
        acquire_lock(tmp_workspace, max_wait_s=2, orphan_age_s=60)
    elapsed = time.time() - start
    assert exc.value.code == 2
    assert 1.5 <= elapsed <= 4.0  # margem pra polling 1s


def test_timeout_emits_structured_stderr(tmp_workspace, tmp_home, capsys):
    lock = lock_path_for(tmp_workspace)
    lock.parent.mkdir(parents=True, exist_ok=True)
    recent_ms = int(time.time() * 1000)
    lock.write_text(f"999999\n{recent_ms}\n", encoding="utf-8")

    with pytest.raises(SystemExit):
        acquire_lock(tmp_workspace, max_wait_s=2, orphan_age_s=60)

    captured = capsys.readouterr()
    assert "LOCK_TIMEOUT" in captured.err
    assert "pid=999999" in captured.err


def test_o_creat_excl_race_resolves_atomically(tmp_workspace, tmp_home):
    """
    Spawn 2 processos Python que tentam acquire ao mesmo tempo.
    Exatamente 1 vence, outro entra em polling e timeout.
    """
    helper = Path(__file__).resolve().parent.parent / "workspace_lock.py"
    cmd = [sys.executable, str(helper), "acquire", str(tmp_workspace)]
    release_cmd = [sys.executable, str(helper), "release", str(tmp_workspace)]
    env = {**os.environ, "USERPROFILE": str(tmp_home), "HOME": str(tmp_home)}

    # Lancar 2 processos quase simultaneamente
    p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    p2 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)

    # Aguardar o primeiro a terminar (qualquer um pode vencer no scheduler do SO)
    # poll() em loop pra nao bloquear no processo errado
    winner, loser = None, None
    deadline = time.time() + 10
    while time.time() < deadline:
        if p1.poll() is not None and winner is None:
            winner, loser = p1, p2
            break
        if p2.poll() is not None and winner is None:
            winner, loser = p2, p1
            break
        time.sleep(0.1)

    assert winner is not None, "Nenhum processo terminou em 10s"
    assert winner.returncode == 0  # vencedor adquiriu o lock

    # Release pra desbloquear o perdedor
    subprocess.run(release_cmd, env=env)
    rc_loser = loser.wait(timeout=35)
    # Perdedor deve ter conseguido depois do release OU timeout (rc 2)
    assert rc_loser in (0, 2)
