#!/usr/bin/env python3
"""
Hook PreToolUse do Sistema Maestro.
Bloqueia Edit/Write/MultiEdit/NotebookEdit do Maestro hub
em paths de vault Maestro fora da whitelist Fase 1.

Etapa 0 (F-Status): valida schema do frontmatter pra todos
(hub + subagent), bloqueando mutilacao de campos canonicos
e status fora do enum do catalogo.
"""
import sys
import json
import re
from pathlib import Path

# Permite importar helper de catalogo
sys.path.insert(0, str(Path(__file__).parent.parent / "core" / "helpers"))

WHITELIST_FASE_1 = {"rascunhos", "memorias", "maestro", ".obsidian", ".claude"}
ERROR_LOG = Path.home() / ".maestro" / "hook-errors.log"
MAX_DEPTH_ALPHA = 20  # limite de profundidade na escalada de parents


# Templates obrigatorios por tipo (campos canonicos que NAO podem sumir)
TEMPLATES_OBRIGATORIOS = {
    "tarefa": {"tipo", "status", "titulo", "agente", "categoria"},
    "plano": {"tipo", "status", "titulo"},
    "identidade": {"tipo", "camada", "status"},
    "produto": {"tipo", "camada", "status"},
    "pesquisa": {"tipo", "status", "titulo"},
    "rascunho": {"tipo", "status"},
    "entrevista": {"tipo", "status", "titulo"},
    "campanha": {"tipo", "status", "titulo"},
    "funil": {"tipo", "status", "titulo"},
    "lancamento": {"tipo", "status", "titulo"},
    "lead-magnet": {"tipo", "status", "titulo"},
    "escada-de-valor": {"tipo", "status", "titulo"},
    "analise-performance": {"tipo", "status", "titulo"},
    "entrega-generica": {"tipo", "status", "titulo"},
}

MENSAGENS_NATURAIS = {
    "status-fora-do-enum": "Peguei aqui — apliquei status fora do vocabulario canonico ('{valor}'). Vou refazer usando o caminho oficial.",
    "campo-canonico-removido": "Peguei aqui — removi campo canonico '{campo}' do frontmatter por engano. Vou refazer preservando a estrutura.",
}

# Cache do catalogo (1x por processo)
_CATALOG = None


def get_catalog():
    """Carrega catalogo 1x por processo."""
    global _CATALOG
    if _CATALOG is None:
        from patch_frontmatter import load_catalog
        catalog_path = Path(__file__).parent.parent / "core" / "protocolos" / "catalogo-status.md"
        _CATALOG = load_catalog(catalog_path)
    return _CATALOG


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


FRONTMATTER_BLOCK = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def parse_fm(text: str):
    """Extrai frontmatter como dict de strings. Retorna None se ausente."""
    m = FRONTMATTER_BLOCK.match(text)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def infer_tipo(fm, path: Path):
    """Tipo do frontmatter, ou inferencia pela pasta."""
    if fm and fm.get("tipo"):
        return fm["tipo"], True  # (tipo, declarado_explicitamente)
    mapping = {
        "tarefas": "tarefa", "planos": "plano", "pesquisas": "pesquisa",
        "rascunhos": "rascunho", "entrevistas": "entrevista",
        "identidade": "identidade", "produto": "produto",
        "campanhas": "campanha", "funis": "funil", "lancamentos": "lancamento",
        "lead-magnets": "lead-magnet",
    }
    tipo = mapping.get(path.parent.name)
    return (tipo, False) if tipo else (None, False)


def simulate_edit(current: str, old: str, new: str) -> str:
    """Aplica Edit em memoria."""
    return current.replace(old, new, 1) if old in current else current


def validate_frontmatter_schema(tool_name: str, tool_input: dict):
    """Valida schema do frontmatter.

    Retorna dict com deny_reason se violacao, None caso contrario (OK ou fora do
    escopo). NUNCA retorna "allow" — schema valido apenas significa "segue pras
    proximas etapas (whitelist de path)".
    """
    file_path = tool_input.get("file_path")
    if not file_path:
        return None

    path = Path(file_path)
    current_fm = None

    # Estado simulado pos-operacao
    if tool_name == "Write":
        new_content = tool_input.get("content", "")
        if path.exists():
            try:
                current_fm = parse_fm(path.read_text(encoding="utf-8"))
            except Exception:
                current_fm = None
    elif tool_name in ("Edit", "MultiEdit"):
        if not path.exists():
            return None
        try:
            current = path.read_text(encoding="utf-8")
        except Exception:
            return None
        current_fm = parse_fm(current)
        if tool_name == "Edit":
            new_content = simulate_edit(
                current,
                tool_input.get("old_string", ""),
                tool_input.get("new_string", ""),
            )
        else:
            new_content = current
            for edit in tool_input.get("edits", []):
                new_content = simulate_edit(
                    new_content,
                    edit.get("old_string", ""),
                    edit.get("new_string", ""),
                )
    else:
        return None

    new_fm = parse_fm(new_content)
    if new_fm is None:
        return None  # sem frontmatter, fora do escopo

    tipo, tipo_declarado = infer_tipo(new_fm, path)
    if not tipo:
        return None  # tipo indeterminado, fail-open

    # Se o arquivo original declarava tipo: e o novo removeu, e' mutilacao.
    if current_fm and current_fm.get("tipo") and not new_fm.get("tipo"):
        return {
            "code": "frontmatter-schema-violation",
            "tipo": current_fm["tipo"],
            "violacao": "campo-canonico-removido",
            "campo-faltando": "tipo",
            "hint": "Use python plugin/core/helpers/patch_frontmatter.py para mudar campos sem mutilar o frontmatter.",
            "mensagem-natural": MENSAGENS_NATURAIS["campo-canonico-removido"].format(campo="tipo"),
        }

    try:
        catalog = get_catalog()
    except Exception as e:
        log_error(f"[hook-schema-error] falha ao carregar catalogo: {e}")
        return None

    if tipo not in catalog.get("tipos", {}):
        log_error(f"[hook-schema-warning] tipo '{tipo}' nao esta no catalogo; fail-open")
        return None

    obrigatorios = TEMPLATES_OBRIGATORIOS.get(tipo, {"tipo", "status"})
    # Quando tipo foi INFERIDO pela pasta (nao declarado no fm), nao exigir "tipo"
    # como campo obrigatorio — scaffold inicial pode estar montando a casca.
    if not tipo_declarado:
        obrigatorios = obrigatorios - {"tipo"}

    faltando = obrigatorios - set(new_fm.keys())
    if faltando:
        campo = sorted(faltando)[0]
        return {
            "code": "frontmatter-schema-violation",
            "tipo": tipo,
            "violacao": "campo-canonico-removido",
            "campo-faltando": campo,
            "hint": "Use python plugin/core/helpers/patch_frontmatter.py para mudar campos sem mutilar o frontmatter.",
            "mensagem-natural": MENSAGENS_NATURAIS["campo-canonico-removido"].format(campo=campo),
        }

    status = new_fm.get("status")
    if status:
        type_block = catalog["tipos"][tipo]
        validos = set(type_block.get("status-canonicos", [])) | set(type_block.get("extensoes", []))
        if validos and status not in validos:
            return {
                "code": "frontmatter-schema-violation",
                "tipo": tipo,
                "violacao": "status-fora-do-enum",
                "valor-rejeitado": status,
                "enum-valido": sorted(validos),
                "hint": f"Use python plugin/core/helpers/patch_frontmatter.py --file {file_path} --set status=<valor>",
                "mensagem-natural": MENSAGENS_NATURAIS["status-fora-do-enum"].format(valor=status),
            }

    # Schema OK — segue pras proximas etapas (whitelist de paths).
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
        tool_name = payload.get("tool_name", "")
        tool_input = payload.get("tool_input") or {}

        # Etapa 0 — validacao semantica de schema (aplica a TODOS, inclusive subagent).
        # Se schema invalido, deny imediato. Se OK ou fora do escopo, CONTINUA
        # pras etapas seguintes (NAO sobrepoe a whitelist de paths — B-S55-54).
        if tool_name in ("Edit", "Write", "MultiEdit"):
            deny_reason = validate_frontmatter_schema(tool_name, tool_input)
            if deny_reason is not None:
                return emit("deny", json.dumps(deny_reason, ensure_ascii=False))

        # Etapa 1 — subagente? (libera apos schema validado)
        if payload.get("agent_id") or payload.get("agent_type"):
            return emit("allow")

        # Etapa 2 — extrair file_path
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
