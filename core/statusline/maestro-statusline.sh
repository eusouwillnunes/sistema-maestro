#!/usr/bin/env bash
# maestro-statusline.sh — Status line do Sistema Maestro
# Recebe JSON via stdin do Claude Code, renderiza barra de status formatada.
# Gerado pelo Sistema Maestro. Nao edite manualmente — use /maestro-statusline configurar.

set -u

# --- Configuracao (preenchida pela skill ao gerar) ---
ITEMS="contexto,limite-5h,limite-7d,modelo"
ESTILO_CONTEXTO="barra"
ESTILO_LIMITE_5H="numero"
ESTILO_LIMITE_7D="numero"
ESTILO_MODELO="texto"
ESTILO_CUSTO="numero"
FAIXAS_CONTEXTO="40,60,70"

# --- Cores ANSI ---
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
ORANGE=$'\033[38;5;208m'
RED=$'\033[31m'
RESET=$'\033[0m'
DIM=$'\033[2m'
SEP=" ${DIM}|${RESET} "

# --- Ler JSON do stdin ---
JSON=$(cat)

# --- Extracao: jq quando disponivel, senao sed regex puro (sem Python) ---
if command -v jq >/dev/null 2>&1; then
  PARSED=$(printf '%s' "$JSON" | jq -r '
    [
      (.context_window.used_percentage // 0),
      (.rate_limits.five_hour.used_percentage // 0),
      (.rate_limits.seven_day.used_percentage // 0),
      (.model.display_name // "?"),
      (.cost.total_cost_usd // 0)
    ] | @tsv
  ' 2>/dev/null)
  IFS=$'\t' read -r CTX_PCT LIMIT_5H_PCT LIMIT_7D_PCT MODEL_NAME COST_USD <<< "$PARSED"
else
  # JSON do Claude Code pode vir formatado (multi-linha com indentacao) E ter objetos
  # nested dentro do parent que queremos (ex: current_usage dentro de context_window vem
  # ANTES de used_percentage). awk slurpa tudo via getline e faz brace counting manual
  # pra delimitar o bloco do parent corretamente — depois extrai o campo de dentro.
  PARSED=$(printf '%s' "$JSON" | awk '
    function extract_block(buf, parent,    start, brace_start, depth, i, c) {
      start = index(buf, "\"" parent "\"")
      if (!start) return ""
      buf = substr(buf, start)
      brace_start = index(buf, "{")
      if (!brace_start) return ""
      depth = 1; i = brace_start + 1
      while (i <= length(buf) && depth > 0) {
        c = substr(buf, i, 1)
        if (c == "{") depth++
        else if (c == "}") depth--
        if (depth == 0) return substr(buf, brace_start, i - brace_start + 1)
        i++
      }
      return ""
    }
    function extract_num(block, key,    s) {
      if (match(block, "\"" key "\"[[:space:]]*:[[:space:]]*[0-9.]+")) {
        s = substr(block, RSTART, RLENGTH)
        sub(/.*:[[:space:]]*/, "", s)
        return s
      }
      return "0"
    }
    function extract_str(block, key,    s) {
      if (match(block, "\"" key "\"[[:space:]]*:[[:space:]]*\"[^\"]*\"")) {
        s = substr(block, RSTART, RLENGTH)
        sub(/.*:[[:space:]]*"/, "", s)
        sub(/".*/, "", s)
        return s
      }
      return "?"
    }
    { all = all $0 }
    END {
      ctx_block = extract_block(all, "context_window")
      rate_block = extract_block(all, "rate_limits")
      model_block = extract_block(all, "model")
      cost_block = extract_block(all, "cost")

      ctx = ctx_block != "" ? extract_num(ctx_block, "used_percentage") : "0"

      h5 = "0"; d7 = "0"
      if (rate_block != "") {
        h5_block = extract_block(rate_block, "five_hour")
        d7_block = extract_block(rate_block, "seven_day")
        if (h5_block != "") h5 = extract_num(h5_block, "used_percentage")
        if (d7_block != "") d7 = extract_num(d7_block, "used_percentage")
      }

      model = model_block != "" ? extract_str(model_block, "display_name") : "?"
      cost = cost_block != "" ? extract_num(cost_block, "total_cost_usd") : "0"

      printf "%s\t%s\t%s\t%s\t%s", ctx, h5, d7, model, cost
    }
  ')
  IFS=$'\t' read -r CTX_PCT LIMIT_5H_PCT LIMIT_7D_PCT MODEL_NAME COST_USD <<< "$PARSED"
fi

# Defaults se campo ausente
CTX_PCT=${CTX_PCT:-0}
LIMIT_5H_PCT=${LIMIT_5H_PCT:-0}
LIMIT_7D_PCT=${LIMIT_7D_PCT:-0}
MODEL_NAME=${MODEL_NAME:-?}
COST_USD=${COST_USD:-0.00}

# Inteiros pra comparacao de faixa (remove decimais)
CTX_INT=${CTX_PCT%.*}
LIMIT_5H_INT=${LIMIT_5H_PCT%.*}
LIMIT_7D_INT=${LIMIT_7D_PCT%.*}
[ -z "$CTX_INT" ] && CTX_INT=0
[ -z "$LIMIT_5H_INT" ] && LIMIT_5H_INT=0
[ -z "$LIMIT_7D_INT" ] && LIMIT_7D_INT=0

# Cap em 100 (defesa contra valores absurdos do extract)
[ "$CTX_INT" -gt 100 ] 2>/dev/null && CTX_INT=100
[ "$LIMIT_5H_INT" -gt 100 ] 2>/dev/null && LIMIT_5H_INT=100
[ "$LIMIT_7D_INT" -gt 100 ] 2>/dev/null && LIMIT_7D_INT=100

# --- Resolvedores de cor (escrevem em variavel, sem subshell) ---
CTX_COLOR=""
ctx_color() {
  local pct="$1"
  local t1 t2 t3
  IFS=',' read -r t1 t2 t3 <<< "$FAIXAS_CONTEXTO"
  if   [ "$pct" -le "$t1" ]; then CTX_COLOR="$GREEN"
  elif [ "$pct" -le "$t2" ]; then CTX_COLOR="$YELLOW"
  elif [ "$pct" -le "$t3" ]; then CTX_COLOR="$ORANGE"
  else                            CTX_COLOR="$RED"
  fi
}

LIMIT_COLOR=""
limit_color() {
  local pct="$1"
  if   [ "$pct" -le 50 ]; then LIMIT_COLOR="$GREEN"
  elif [ "$pct" -le 75 ]; then LIMIT_COLOR="$YELLOW"
  elif [ "$pct" -le 90 ]; then LIMIT_COLOR="$ORANGE"
  else                         LIMIT_COLOR="$RED"
  fi
}

BAR=""
render_bar() {
  local pct="$1"
  local filled=$(( pct / 10 ))
  [ "$filled" -gt 10 ] && filled=10
  [ "$filled" -lt 0 ] && filled=0
  local empty=$(( 10 - filled ))
  local i out=""
  for ((i=0; i<filled; i++)); do out+="█"; done
  for ((i=0; i<empty; i++));  do out+="░"; done
  BAR="${out} ${pct}%"
}

# --- Montar segmentos (cor embutida em cada segmento, sem stdout vazado) ---
declare -a SEGMENTS=()
IFS=',' read -ra ITEM_LIST <<< "$ITEMS"
for item in "${ITEM_LIST[@]}"; do
  item="${item// /}"
  case "$item" in
    contexto)
      ctx_color "$CTX_INT"
      if [ "$ESTILO_CONTEXTO" = "barra" ]; then
        render_bar "$CTX_INT"
        SEGMENTS+=("${CTX_COLOR}Contexto: ${BAR}${RESET}")
      else
        SEGMENTS+=("${CTX_COLOR}Ctx: ${CTX_INT}%${RESET}")
      fi
      ;;
    limite-5h)
      limit_color "$LIMIT_5H_INT"
      if [ "$ESTILO_LIMITE_5H" = "barra" ]; then
        render_bar "$LIMIT_5H_INT"
        SEGMENTS+=("${LIMIT_COLOR}5h: ${BAR}${RESET}")
      else
        SEGMENTS+=("${LIMIT_COLOR}5h: ${LIMIT_5H_INT}%${RESET}")
      fi
      ;;
    limite-7d)
      limit_color "$LIMIT_7D_INT"
      if [ "$ESTILO_LIMITE_7D" = "barra" ]; then
        render_bar "$LIMIT_7D_INT"
        SEGMENTS+=("${LIMIT_COLOR}7d: ${BAR}${RESET}")
      else
        SEGMENTS+=("${LIMIT_COLOR}7d: ${LIMIT_7D_INT}%${RESET}")
      fi
      ;;
    modelo)
      SEGMENTS+=("$MODEL_NAME")
      ;;
    custo)
      SEGMENTS+=("\$${COST_USD}")
      ;;
  esac
done

# --- Unir com separador e imprimir uma unica vez ---
OUTPUT=""
for s in "${SEGMENTS[@]}"; do
  if [ -z "$OUTPUT" ]; then
    OUTPUT="$s"
  else
    OUTPUT="${OUTPUT}${SEP}${s}"
  fi
done

printf '%s' "$OUTPUT"
