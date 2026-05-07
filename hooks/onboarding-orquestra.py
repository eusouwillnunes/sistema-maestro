#!/usr/bin/env python3
"""
Hook PreToolUse de auditoria do onboarding.

Bloqueia dispatch Skill/Agent do hub do Maestro quando marker
correspondente está ausente no state file ativo.

Markers críticos validados:
- t-consentimento (gate pra SCAFFOLD WORKSPACE)
- t-auq-biblioteca (gate pra Bibliotecário CRIAR)
- t-auq-pesquisa (gate pra Pesquisador)

Subagent calls são liberados incondicionalmente (aprendizado #21).
Sem state file ativo → libera tudo (hook não interfere fora do onboarding).
"""
import json
import re
import sys
from pathlib import Path

# Mapeamento (tool_name, subagent_type, fluxo) -> marker required.
# fluxo é parseado de tool_input["prompt"] procurando "FLUXO: <X>".
# fluxo None = qualquer fluxo (Pesquisador não usa marcador FLUXO).
PROTECTED_DISPATCHES = {
    ("Agent", "maestro:bibliotecario", "CRIAR"): "t-auq-biblioteca",
    ("Skill", "maestro:bibliotecario", "CRIAR"): "t-auq-biblioteca",
    ("Agent", "maestro:bibliotecario", "SCAFFOLD WORKSPACE"): "t-consentimento",
    ("Skill", "maestro:bibliotecario", "SCAFFOLD WORKSPACE"): "t-consentimento",
    ("Agent", "maestro:pesquisador", None): "t-auq-pesquisa",
    ("Skill", "maestro:pesquisador", None): "t-auq-pesquisa",
}


def emit(decision: str, reason: str = "") -> None:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
        }
    }
    if reason:
        output["hookSpecificOutput"]["permissionDecisionReason"] = reason
    print(json.dumps(output))
    sys.exit(0)


def is_subagent(payload: dict) -> bool:
    """Detecta se chamada vem de subagent (libera tudo). Aprendizado #21."""
    return bool(payload.get("agent_id") or payload.get("agent_type"))


def parse_fluxo(prompt: str) -> str:
    """Extrai 'FLUXO: X' do prompt do dispatch. String vazia se não achar."""
    # `[A-Z ]*` cobre fluxos como "CRIAR" e "SCAFFOLD WORKSPACE" sem cruzar
    # linhas (evita capturar "CRIAR\nCONTEXTO" quando prompt continua).
    m = re.search(r"FLUXO:[ \t]*([A-Z][A-Z ]*)", prompt or "", re.IGNORECASE)
    if m:
        return m.group(1).strip().upper()
    return ""


def find_active_state(cwd: Path):
    """Retorna Path do state file ativo (sem t-conclusao) ou None."""
    onboarding_dir = cwd / "memorias" / "onboarding"
    if not onboarding_dir.exists():
        return None
    for state in onboarding_dir.glob("state-*.md"):
        try:
            content = state.read_text(encoding="utf-8")
        except Exception:
            continue
        if "- t-conclusao: " not in content:
            return state
    return None


def has_marker_in_state(state_path: Path, marker: str) -> bool:
    try:
        content = state_path.read_text(encoding="utf-8")
    except Exception:
        return False
    return f"- {marker}: " in content


def has_any_state_evidence(cwd: Path) -> bool:
    """True se existe algum state file (ativo ou arquivado) — evidência de que
    Camadas 3+4 chegaram a ser ativadas em algum momento desta workspace."""
    onboarding_dir = cwd / "memorias" / "onboarding"
    if not onboarding_dir.exists():
        return False
    if any(onboarding_dir.glob("state-*.md")):
        return True
    concluidos = onboarding_dir / "concluidos"
    if concluidos.exists() and any(concluidos.glob("state-*.md")):
        return True
    return False


def is_completion_write(tool_name: str, tool_input: dict) -> bool:
    """Detecta tentativa de gravar `onboarding-completo: true` em config.md
    via Bash (sed/echo) ou via Edit/Write. Tripwire B-OnbUX-2A-9 medida (c)."""
    if tool_name == "Bash":
        cmd = tool_input.get("command", "") or ""
        if "config.md" in cmd and "onboarding-completo" in cmd and "true" in cmd:
            return True
        return False
    if tool_name in ("Edit", "Write", "MultiEdit"):
        path = tool_input.get("file_path", "") or ""
        if not path.endswith("config.md"):
            return False
        haystack = ""
        if tool_name == "Write":
            haystack = tool_input.get("content", "") or ""
        elif tool_name == "Edit":
            haystack = tool_input.get("new_string", "") or ""
        else:  # MultiEdit
            edits = tool_input.get("edits", []) or []
            haystack = " ".join(e.get("new_string", "") or "" for e in edits)
        return "onboarding-completo: true" in haystack
    return False


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        emit("allow")  # input inválido — não interfere

    if is_subagent(payload):
        emit("allow")

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})
    cwd = Path(payload.get("cwd", ".")).resolve()

    # Tripwire B-OnbUX-2A-9 medida (c): bloqueia gravar onboarding-completo: true
    # quando Camadas 3+4 nunca foram ativadas (nenhum state file ativo nem arquivado).
    if is_completion_write(tool_name, tool_input) and not has_any_state_evidence(cwd):
        tripwire_reason = {
            "reason": "audit-trail-ausente",
            "tool-bloqueado": tool_name,
            "hint": (
                "Tentou marcar onboarding-completo: true mas nenhum state file "
                "de auditoria existe em memorias/onboarding/. As Camadas 3+4 "
                "do onboarding nunca foram ativadas — provavelmente o Bash de "
                "init do T3 (Primeira Vez) ou T0/T1B (Novo Projeto) foi pulado. "
                "Re-execute esse Bash antes de finalizar o onboarding. Não "
                "silenciar este bloqueio."
            ),
            "mensagem-pro-user": (
                "Faltou um passo de auditoria do onboarding aqui. "
                "Vou voltar e ativar antes de fechar — um instante."
            ),
        }
        emit("deny", json.dumps(tripwire_reason, ensure_ascii=False))

    target = tool_input.get("subagent_type") or tool_input.get("skill") or ""
    prompt_text = tool_input.get("prompt", "")
    fluxo = parse_fluxo(prompt_text)

    key_with_fluxo = (tool_name, target, fluxo)
    key_no_fluxo = (tool_name, target, None)
    if key_with_fluxo in PROTECTED_DISPATCHES:
        marker_required = PROTECTED_DISPATCHES[key_with_fluxo]
    elif key_no_fluxo in PROTECTED_DISPATCHES:
        marker_required = PROTECTED_DISPATCHES[key_no_fluxo]
    else:
        emit("allow")

    state = find_active_state(cwd)
    if state is None:
        emit("allow")  # sem onboarding ativo

    if has_marker_in_state(state, marker_required):
        emit("allow")

    reason_obj = {
        "reason": "marker-ausente",
        "marker-esperado": marker_required,
        "agent-bloqueado": target,
        "hint": (
            f"AUQ correspondente a {marker_required} não foi emitida antes "
            f"deste dispatch. Emita a AUQ, registre o marker via helper "
            f"onboarding_state.py, e re-tente."
        ),
        "mensagem-pro-user": (
            "Peguei aqui — preciso te perguntar uma coisa antes de seguir. "
            "Um instante."
        ),
    }
    emit("deny", json.dumps(reason_obj, ensure_ascii=False))


if __name__ == "__main__":
    main()
