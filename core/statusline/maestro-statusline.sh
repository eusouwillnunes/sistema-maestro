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
  # JSON do Claude Code vem em linha unica. 1 awk com 5 capturas em vez de 5 seds = ~5x mais rapido.
  # Escopo por parent: cada captura ancora no nome do objeto-pai mais proximo do campo alvo.
  PARSED=$(printf '%s' "$JSON" | awk '
    {
      ctx="0"; h5="0"; d7="0"; model="?"; cost="0"
      if (match($0, /"context_window"[^}]*"used_percentage"[[:space:]]*:[[:space:]]*[0-9.]+/)) {
        s = substr($0, RSTART, RLENGTH); sub(/.*:[[:space:]]*/, "", s); ctx = s
      }
      if (match($0, /"five_hour"[^}]*"used_percentage"[[:space:]]*:[[:space:]]*[0-9.]+/)) {
        s = substr($0, RSTART, RLENGTH); sub(/.*:[[:space:]]*/, "", s); h5 = s
      }
      if (match($0, /"seven_day"[^}]*"used_percentage"[[:space:]]*:[[:space:]]*[0-9.]+/)) {
        s = substr($0, RSTART, RLENGTH); sub(/.*:[[:space:]]*/, "", s); d7 = s
      }
      if (match($0, /"model"[[:space:]]*:[[:space:]]*\{[^}]*"display_name"[[:space:]]*:[[:space:]]*"[^"]*"/)) {
        s = substr($0, RSTART, RLENGTH); sub(/.*"display_name"[[:space:]]*:[[:space:]]*"/, "", s); sub(/".*/, "", s); model = s
      }
      if (match($0, /"cost"[[:space:]]*:[[:space:]]*\{[^}]*"total_cost_usd"[[:space:]]*:[[:space:]]*[0-9.]+/)) {
        s = substr($0, RSTART, RLENGTH); sub(/.*:[[:space:]]*/, "", s); cost = s
      }
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
