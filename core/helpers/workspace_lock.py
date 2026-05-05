#!/usr/bin/env python3
"""
Helper de lock pra serializar dispatches concorrentes do Bibliotecario na
mesma workspace (SCAFFOLD WORKSPACE / REGENERATE PAINEL / UPDATE_FLAG /
CRIAR BOOKMARKS DE NAVEGACAO).

Detecao de orfao por timestamp (cap 60s) — substitui os.kill(pid, 0) que
nao funciona cross-platform (Sessao 71, Fase 0 F4 Teste B).

CLI:
    python workspace_lock.py acquire <workspace_path>
    python workspace_lock.py release <workspace_path>

Exit codes:
    0 — sucesso
    2 — timeout aguardando lock (stderr: LOCK_TIMEOUT|pid=X|age_s=Y|path=Z)
    1 — erro nao previsto
"""
import hashlib
import os
import sys
import time
from pathlib import Path

LOCK_TIMEOUT_S = 30
ORPHAN_AGE_S = 60
POLL_INTERVAL_S = 1.0


def lock_path_for(workspace_path: Path) -> Path:
    """MD5 do path absoluto (forward-slash normalizado) — mesmo path em qualquer SO produz mesmo hash dentro do SO."""
    md5 = hashlib.md5(str(workspace_path).replace("\\", "/").encode("utf-8")).hexdigest()
    return Path.home() / ".maestro" / f"scaffold-workspace-{md5}.lock"


def acquire_lock(workspace_path: Path, max_wait_s: int = LOCK_TIMEOUT_S, orphan_age_s: int = ORPHAN_AGE_S) -> None:
    """
    Adquire o lock. Retorna None em sucesso. SystemExit(2) em timeout.
    """
    lock = lock_path_for(workspace_path)
    lock.parent.mkdir(parents=True, exist_ok=True)

    start = time.time()
    while True:
        try:
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"{os.getpid()}\n{int(time.time() * 1000)}\n".encode("utf-8"))
            os.close(fd)
            return
        except FileExistsError:
            pass

        # Lock existe — checar idade
        try:
            content = lock.read_text(encoding="utf-8").splitlines()
            created_ms = int(content[1]) if len(content) >= 2 else 0
        except Exception:
            content = []
            created_ms = 0

        age_s = (time.time() * 1000 - created_ms) / 1000
        if age_s > orphan_age_s:
            try:
                lock.unlink()
            except FileNotFoundError:
                pass
            continue

        if time.time() - start > max_wait_s:
            pid_str = content[0] if content else "?"
            sys.stderr.write(
                f"LOCK_TIMEOUT|pid={pid_str}|age_s={age_s:.0f}|path={lock}\n"
            )
            sys.exit(2)

        time.sleep(POLL_INTERVAL_S)


def release_lock(workspace_path: Path) -> None:
    lock = lock_path_for(workspace_path)
    try:
        lock.unlink()
    except FileNotFoundError:
        pass


def main() -> int:
    if len(sys.argv) < 3:
        sys.stderr.write("Uso: workspace_lock.py acquire|release <workspace_path>\n")
        return 1

    action = sys.argv[1]
    workspace = Path(sys.argv[2]).resolve()

    if action == "acquire":
        acquire_lock(workspace)
        return 0
    elif action == "release":
        release_lock(workspace)
        return 0
    else:
        sys.stderr.write(f"Acao desconhecida: {action}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
