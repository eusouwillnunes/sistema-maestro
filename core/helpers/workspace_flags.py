#!/usr/bin/env python3
"""
Helper de flags da workspace.

Gerencia <workspace>/.maestro-flags.md com frontmatter idempotente +
atomic write com retry. Backup .bak se corrompido.

CLI:
    python workspace_flags.py init <ws>
    python workspace_flags.py get <ws> <flag-name>
    python workspace_flags.py set <ws> <flag-name> <flag-value>
"""
import errno
import os
import re
import sys
import time
from pathlib import Path

FLAGS_FILENAME = ".maestro-flags.md"
BACKOFFS = [0.2, 0.5, 1.0, 2.0]

TEMPLATE = """---
tipo: maestro-flags-workspace
versao-template: 1
aviso-colisao-wikilink-mostrado: false
---

> [!warning] Não edite manualmente
> Este arquivo guarda flags persistentes da Área de Trabalho. O Maestro atualiza
> automaticamente via Bibliotecário. Editar manualmente pode dessincronizar o
> estado e fazer mensagens repetirem ou sumirem indevidamente.

# Flags da Área de Trabalho

| Flag | Significado |
|---|---|
| `aviso-colisao-wikilink-mostrado` | True se o callout sobre nomes iguais entre projetos já foi mostrado nesta workspace |
"""


def _atomic_write_text(target: Path, content: str) -> None:
    tmp = target.with_suffix(target.suffix + ".tmp")
    last_err = None
    for delay in [0] + BACKOFFS:
        if delay > 0:
            time.sleep(delay)
        try:
            tmp.write_text(content, encoding="utf-8")
            os.replace(str(tmp), str(target))
            return
        except OSError as e:
            if getattr(e, "winerror", None) != 5 and e.errno != errno.EACCES:
                raise
            last_err = e
    sys.stderr.write(f"WRITE_FAILED|target={target}|attempts={len(BACKOFFS)+1}|last_err={last_err}\n")
    sys.exit(2)


def _flags_path(workspace: Path) -> Path:
    return workspace / FLAGS_FILENAME


def _parse_frontmatter(content: str) -> dict[str, str] | None:
    """
    Retorna dict do frontmatter ou None se invalido.
    Parse simples — assume schema controlado pelo template.
    """
    if not content.startswith("---\n"):
        return None
    try:
        end = content.index("\n---\n", 4)
    except ValueError:
        return None
    fm_text = content[4:end]
    result = {}
    for line in fm_text.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            result[k.strip()] = v.strip()
    if "tipo" not in result:
        return None
    return result


def init_flags(workspace: Path) -> None:
    """Cria .maestro-flags.md do template se nao existir."""
    target = _flags_path(workspace)
    if target.exists():
        return
    _atomic_write_text(target, TEMPLATE)


def get_flag(workspace: Path, flag_name: str) -> str | None:
    target = _flags_path(workspace)
    if not target.exists():
        return None
    content = target.read_text(encoding="utf-8")
    fm = _parse_frontmatter(content)
    if fm is None:
        return None
    return fm.get(flag_name)


def set_flag(workspace: Path, flag_name: str, flag_value: str) -> bool:
    """
    Atualiza flag no frontmatter. Retorna True se houve mudanca, False se idempotente.
    Se .maestro-flags.md corrompido, faz backup e recria do template.
    """
    target = _flags_path(workspace)
    if not target.exists():
        init_flags(workspace)

    content = target.read_text(encoding="utf-8")
    fm = _parse_frontmatter(content)

    if fm is None:
        # Corrompido — backup + recriar
        bak = target.with_suffix(".md.bak")
        try:
            target.replace(bak)
        except Exception:
            pass
        sys.stderr.write(f"FLAGS_CORRUPTED|backup={bak}\n")
        _atomic_write_text(target, TEMPLATE)
        content = TEMPLATE
        fm = _parse_frontmatter(content) or {}

    if fm.get(flag_name) == flag_value:
        return False  # idempotente

    # Substituir linha do flag (ou adicionar se nao existir)
    pattern = re.compile(rf"^{re.escape(flag_name)}:\s*.*$", re.MULTILINE)
    new_line = f"{flag_name}: {flag_value}"
    if pattern.search(content):
        new_content = pattern.sub(new_line, content, count=1)
    else:
        # Inserir antes do --- de fechamento do frontmatter
        end_marker = "\n---\n"
        idx = content.index(end_marker, 4)
        new_content = content[:idx] + "\n" + new_line + content[idx:]

    _atomic_write_text(target, new_content)
    return True


def main() -> int:
    if len(sys.argv) < 3:
        sys.stderr.write("Uso: workspace_flags.py init|get|set <ws> [flag-name] [flag-value]\n")
        return 1

    action = sys.argv[1]
    workspace = Path(sys.argv[2]).resolve()

    if action == "init":
        init_flags(workspace)
        return 0

    elif action == "get":
        if len(sys.argv) < 4:
            sys.stderr.write("get requer flag-name\n")
            return 1
        value = get_flag(workspace, sys.argv[3])
        if value is None:
            return 1
        print(value)
        return 0

    elif action == "set":
        if len(sys.argv) < 5:
            sys.stderr.write("set requer flag-name e flag-value\n")
            return 1
        changed = set_flag(workspace, sys.argv[3], sys.argv[4])
        print(f"flag-atualizada={'true' if changed else 'false'}")
        return 0

    else:
        sys.stderr.write(f"Acao desconhecida: {action}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
