#!/usr/bin/env python3
"""
Helper de estado do onboarding do Sistema Maestro.

Markers de turno gravados em <projeto>/memorias/onboarding/state-{slug}.md.
Hook PreToolUse `onboarding-orquestra.py` lê este state pra validar dispatches.

API:
  init_state(state_dir, slug, fluxo) -> Path
  mark(state_dir, slug, marker)
  has_marker(state_dir, slug, marker) -> bool
  archive(state_dir, slug)
  cleanup_orphans(state_dir, max_age_hours=24)
  normalize_slug(workspace_name, projeto_name) -> str
"""
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Permite import quando rodado como script (não como pacote)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _slug import slugify  # noqa: E402


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def normalize_slug(workspace_name: str, projeto_name: str) -> str:
    return f"{slugify(workspace_name)}-{slugify(projeto_name)}"


def _state_path(state_dir: Path, slug: str) -> Path:
    return state_dir / f"state-{slug}.md"


def init_state(state_dir: Path, slug: str, fluxo: str) -> Path:
    state_dir.mkdir(parents=True, exist_ok=True)
    path = _state_path(state_dir, slug)
    content = (
        f"---\n"
        f"slug: {slug}\n"
        f"fluxo: {fluxo}\n"
        f"inicio: {_now_iso()}\n"
        f"---\n\n"
        f"## Markers\n\n"
    )
    path.write_text(content, encoding="utf-8")
    return path


def mark(state_dir: Path, slug: str, marker: str) -> None:
    path = _state_path(state_dir, slug)
    if not path.exists():
        raise FileNotFoundError(f"state file not found for slug={slug}")
    content = path.read_text(encoding="utf-8")
    if f"- {marker}: " in content:
        return  # idempotente
    line = f"- {marker}: {_now_iso()}\n"
    if not content.endswith("\n"):
        content += "\n"
    content += line
    path.write_text(content, encoding="utf-8")


def has_marker(state_dir: Path, slug: str, marker: str) -> bool:
    path = _state_path(state_dir, slug)
    if not path.exists():
        return False
    return f"- {marker}: " in path.read_text(encoding="utf-8")


def archive(state_dir: Path, slug: str) -> Path:
    src = _state_path(state_dir, slug)
    if not src.exists():
        raise FileNotFoundError(f"state file not found for slug={slug}")
    concluidos = state_dir / "concluidos"
    concluidos.mkdir(exist_ok=True)
    dst = concluidos / src.name
    src.rename(dst)
    return dst


def cleanup_orphans(state_dir: Path, max_age_hours: int = 24) -> int:
    if not state_dir.exists():
        return 0
    cutoff = datetime.now(timezone.utc).timestamp() - (max_age_hours * 3600)
    removed = 0
    for path in state_dir.glob("state-*.md"):
        if path.stat().st_mtime < cutoff:
            path.unlink()
            removed += 1
    return removed


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("usage: onboarding_state.py <init|mark|has|archive|cleanup|slug> ...", file=sys.stderr)
        return 2
    cmd = args[0]
    if cmd == "init" and len(args) == 4:
        init_state(Path(args[1]), args[2], args[3])
        return 0
    if cmd == "mark" and len(args) == 4:
        mark(Path(args[1]), args[2], args[3])
        return 0
    if cmd == "has" and len(args) == 4:
        return 0 if has_marker(Path(args[1]), args[2], args[3]) else 1
    if cmd == "archive" and len(args) == 3:
        archive(Path(args[1]), args[2])
        return 0
    if cmd == "cleanup" and len(args) >= 2:
        max_age = int(args[2]) if len(args) >= 3 else 24
        removed = cleanup_orphans(Path(args[1]), max_age_hours=max_age)
        print(f"removed={removed}")
        return 0
    if cmd == "slug" and len(args) == 3:
        print(normalize_slug(args[1], args[2]))
        return 0
    print(f"invalid command or args: {args}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
