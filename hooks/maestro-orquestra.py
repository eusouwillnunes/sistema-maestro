#!/usr/bin/env python3
"""
Hook PreToolUse do Sistema Maestro.
Bloqueia Edit/Write/MultiEdit/NotebookEdit do Maestro hub
em paths de vault Maestro fora da whitelist Fase 1.
"""
import sys
import json
from pathlib import Path

WHITELIST_FASE_1 = {"rascunhos", "memorias", "maestro", ".obsidian", ".claude"}
ERROR_LOG = Path.home() / ".maestro" / "hook-errors.log"
MAX_DEPTH_ALPHA = 20  # limite de profundidade na escalada de parents


def log_error(msg: str) -> None:
    try:
        ERROR_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(ERROR_LOG, "a", encoding="utf-8") as f:
            f.write(f"{msg}\n")
    except Exception:
        pass


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


def detect_vault_alpha(fp: Path):
    candidate = fp.resolve().parent
    depth = 0
    while candidate != candidate.parent:
        if depth >= MAX_DEPTH_ALPHA:
            return None
        if (candidate / "maestro" / "config.md").exists():
            return candidate
        candidate = candidate.parent
        depth += 1
    return None


MESSAGE_TEMPLATE = """ESCRITA BLOQUEADA: {path}

Você é o Maestro orquestrador. Maestro não escreve no vault de projeto — só especialistas escrevem. Pra prosseguir:

1. CORREÇÃO DE CONTEÚDO CRIATIVO (copy, posicionamento, identidade, marca):
   → Despachar via Agent(<especialista>) — ex: Agent(maestro:marca), Agent(maestro:copywriter)
   → O especialista escreve na sessão de subagente, hook libera automaticamente.

2. CRIAR/ATUALIZAR TAREFA, PLANO, ENTREGA:
   → Despachar Agent(maestro:gerente) com FLUXO apropriado (criar-tarefa, criar-revisao, concluir-tarefa).

3. SCAFFOLD/INDEX/ESTRUTURA DO VAULT:
   → Despachar Agent(maestro:bibliotecario).

4. RASCUNHO EXPLORATÓRIO (notas, lista, exploração de ideia):
   → Escrita permitida em rascunhos/<slug>.md. Use /rascunho.
   → ATENÇÃO: rascunho NÃO é substituto de especialista. Conteúdo final criativo (copy de marca, posicionamento, headline, página, manifesto, círculo dourado) SEMPRE via especialista — mesmo se for "só um teste".

5. CONFIGURAÇÃO DO PROJETO (maestro/, .obsidian/, .claude/):
   → Permitido — re-tente se a tentativa foi numa dessas pastas.

NUNCA aplique correção alegando "agindo como agente X" — isso é o bug B-S55-54.
NUNCA use Bash com redirect (`>`, `>>`, `cat << EOF`) pra contornar este bloqueio — é o mesmo bug B-S55-54, só mudando de ferramenta.
Se você não tem certeza qual especialista despachar, abra AskUserQuestion pro usuário.

Antes de re-tentar, traduza o bloqueio pro usuário em linguagem natural — ele não vê esta mensagem. Padrão: "Peguei aqui — eu tinha começado a editar direto. Vou despachar [especialista] pra fazer corretamente." Se hook bloqueou 2x seguidas no mesmo path, parar e abrir AskUserQuestion ao invés de re-tentar."""


def main():
    try:
        payload = json.loads(sys.stdin.read())

        # Etapa 1 — subagente?
        if payload.get("agent_id") or payload.get("agent_type"):
            return emit("allow")

        # Etapa 2 — extrair file_path
        tool_input = payload.get("tool_input") or {}
        file_path = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not file_path:
            return emit("allow")

        fp = Path(file_path).resolve()

        # Etapa 3 — vault Maestro?
        vault_root = detect_vault_alpha(fp)
        if vault_root is None:
            return emit("allow")

        # Etapa 4 — whitelist
        if vault_root != fp.parent and vault_root not in fp.parents:
            log_error(
                f"[hook-warning] vault_root={vault_root} not ancestor of fp={fp}; fail-open"
            )
            return emit("allow")

        rel = fp.relative_to(vault_root)
        first_segment = rel.parts[0] if rel.parts else ""
        if first_segment in WHITELIST_FASE_1:
            return emit("allow")

        # Etapa 5 — bloqueia
        return emit("deny", MESSAGE_TEMPLATE.format(path=str(fp)))

    except Exception as e:
        log_error(f"[hook-error] {type(e).__name__}: {e}")
        return emit("allow")


if __name__ == "__main__":
    main()
