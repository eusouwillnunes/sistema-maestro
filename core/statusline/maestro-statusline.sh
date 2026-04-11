#!/usr/bin/env bash
# maestro-statusline.sh — Status line do Sistema Maestro
# Recebe JSON via stdin do Claude Code, renderiza barra de status formatada.
# Gerado pelo Sistema Maestro. Não edite manualmente — use /maestro-statusline configurar.

set -euo pipefail

# --- Configuração (preenchida pela skill ao gerar) ---
ITEMS="contexto,limite-5h,limite-7d,modelo"
ESTILO_CONTEXTO="barra"
ESTILO_LIMITE_5H="numero"
ESTILO_LIMITE_7D="numero"
ESTILO_MODELO="texto"
ESTILO_CUSTO="numero"
FAIXAS_CONTEXTO="40,60,70"

# --- Cores ANSI ---
GREEN='\033[32m'
YELLOW='\033[33m'
ORANGE='\033[38;5;208m'
RED='\033[31m'
RESET='\033[0m'
DIM='\033[2m'
SEP=" ${DIM}│${RESET} "

# --- Ler JSON do stdin ---
JSON=$(cat)

# --- Funções auxiliares ---
extract() {
  local key="$1"
  if command -v jq &>/dev/null; then
    echo "$JSON" | jq -r "$key // empty" 2>/dev/null
  else
    echo "$JSON" | grep -o "\"${key##*.}\"[[:space:]]*:[[:space:]]*[^,}]*" | head -1 | sed 's/.*:[[:space:]]*//' | tr -d '"' | tr -d ' '
  fi
}

color_context() {
  local pct="$1"
  IFS=',' read -r t1 t2 t3 <<< "$FAIXAS_CONTEXTO"
  if [ "$pct" -le "$t1" ]; then echo -ne "$GREEN"
  elif [ "$pct" -le "$t2" ]; then echo -ne "$YELLOW"
  elif [ "$pct" -le "$t3" ]; then echo -ne "$ORANGE"
  else echo -ne "$RED"
  fi
}

color_limit() {
  local pct="$1"
  if [ "$pct" -le 50 ]; then echo -ne "$GREEN"
  elif [ "$pct" -le 75 ]; then echo -ne "$YELLOW"
  elif [ "$pct" -le 90 ]; then echo -ne "$ORANGE"
  else echo -ne "$RED"
  fi
}

render_bar() {
  local pct="$1"
  local filled=$(( pct / 10 ))
  local empty=$(( 10 - filled ))
  local bar=""
  for ((i=0; i<filled; i++)); do bar+="█"; done
  for ((i=0; i<empty; i++)); do bar+="░"; done
  echo -n "${bar} ${pct}%"
}

render_number() {
  local pct="$1"
  echo -n "${pct}%"
}

# --- Extrair valores do JSON ---
CTX_PCT=$(extract ".context_window.used_percentage")
LIMIT_5H_PCT=$(extract ".rate_limits.five_hour.used_percentage")
LIMIT_7D_PCT=$(extract ".rate_limits.seven_day.used_percentage")
MODEL_NAME=$(extract ".model.display_name")
COST_USD=$(extract ".cost.total_cost_usd")

# Defaults se campo ausente
CTX_PCT=${CTX_PCT:-0}
LIMIT_5H_PCT=${LIMIT_5H_PCT:-0}
LIMIT_7D_PCT=${LIMIT_7D_PCT:-0}
MODEL_NAME=${MODEL_NAME:-"?"}
COST_USD=${COST_USD:-"0.00"}

# Converter pra inteiro (remover decimais)
CTX_PCT=${CTX_PCT%.*}
LIMIT_5H_PCT=${LIMIT_5H_PCT%.*}
LIMIT_7D_PCT=${LIMIT_7D_PCT%.*}

# --- Montar output ---
OUTPUT=""

IFS=',' read -ra ITEM_LIST <<< "$ITEMS"
for item in "${ITEM_LIST[@]}"; do
  item=$(echo "$item" | tr -d ' ')
  segment=""

  case "$item" in
    contexto)
      color_context "$CTX_PCT"
      if [ "$ESTILO_CONTEXTO" = "barra" ]; then
        segment="Contexto: $(render_bar "$CTX_PCT")"
      else
        segment="Ctx: $(render_number "$CTX_PCT")"
      fi
      segment="${segment}${RESET}"
      ;;
    limite-5h)
      color_limit "$LIMIT_5H_PCT"
      if [ "$ESTILO_LIMITE_5H" = "barra" ]; then
        segment="5h: $(render_bar "$LIMIT_5H_PCT")"
      else
        segment="5h: $(render_number "$LIMIT_5H_PCT")"
      fi
      segment="${segment}${RESET}"
      ;;
    limite-7d)
      color_limit "$LIMIT_7D_PCT"
      if [ "$ESTILO_LIMITE_7D" = "barra" ]; then
        segment="7d: $(render_bar "$LIMIT_7D_PCT")"
      else
        segment="7d: $(render_number "$LIMIT_7D_PCT")"
      fi
      segment="${segment}${RESET}"
      ;;
    modelo)
      segment="$MODEL_NAME"
      ;;
    custo)
      segment="\$${COST_USD}"
      ;;
  esac

  if [ -n "$segment" ]; then
    if [ -n "$OUTPUT" ]; then
      OUTPUT="${OUTPUT}${SEP}${segment}"
    else
      OUTPUT="$segment"
    fi
  fi
done

echo -ne "$OUTPUT"
