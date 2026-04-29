#!/usr/bin/env bash
# Runner de cenários de performance do hook PreToolUse.
# Mede latência média + p95 em 3 cenários (vault local, cold start, vault profundo).

set -uo pipefail
HOOK_SCRIPT="$(dirname "$0")/../maestro-orquestra.py"
FIXTURES_DIR="$(dirname "$0")/fixtures"
ITERATIONS=50

# Setup do vault de teste (mesma lógica do run-tests.sh)
if [[ "$(uname -s)" == MINGW* || "$(uname -s)" == MSYS* || "$(uname -s)" == CYGWIN* ]]; then
    TMP_REAL="/c/tmp"
else
    TMP_REAL="/tmp"
fi

mkdir -p "$TMP_REAL/maestro-test-vault/maestro" "$TMP_REAL/maestro-test-vault/identidade"
printf "modo: agent\n" > "$TMP_REAL/maestro-test-vault/maestro/config.md"

measure() {
    local fixture=$1
    local label=$2
    local total_ms=0
    local times=()

    for i in $(seq 1 $ITERATIONS); do
        local start=$(date +%s%N)
        python3 "$HOOK_SCRIPT" < "$fixture" > /dev/null 2>&1
        local end=$(date +%s%N)
        local elapsed=$(( (end - start) / 1000000 ))
        times+=($elapsed)
        total_ms=$((total_ms + elapsed))
    done

    local avg=$((total_ms / ITERATIONS))
    local sorted=$(printf '%s\n' "${times[@]}" | sort -n)
    local p95_idx=$(( (ITERATIONS * 95) / 100 ))
    local p95=$(echo "$sorted" | sed -n "${p95_idx}p")
    local first=${times[0]}

    echo "$label"
    echo "  avg=${avg}ms, p95=${p95}ms, primeira chamada=${first}ms (over $ITERATIONS runs)"
}

echo "=== Hook PreToolUse — Performance ==="
echo ""

echo "Cenário 11 — Vault local (deny path)"
measure "$FIXTURES_DIR/01-hub-identidade-deny.json" "  Hub Write em identidade/ (deny)"

echo ""
echo "Cenário 12 — Vault local (allow path — whitelist)"
measure "$FIXTURES_DIR/03-hub-rascunhos-allow.json" "  Hub Write em rascunhos/ (allow)"

echo ""
echo "Cenário 13 — Cold start (primeira chamada do cenário 11 acima — campo 'primeira chamada')"
echo "  Aceito se < 300ms."

echo ""
echo "=== Limites do spec ==="
echo "  Cenário 11/12 (vault local): p95 ≤ 200ms"
echo "  Cenário 13 (cold start)    : primeira ≤ 300ms"
echo ""
echo "Vault profundo: avaliação manual — criar /c/tmp/deep/a/b/c/.../maestro/config.md"
echo "e rodar measure pra confirmar MAX_DEPTH=20 segura sem stack overflow."
