#!/usr/bin/env bash
# Runner dos cenários do hook PreToolUse do Sistema Maestro.
# Roda cada fixture contra o script Python e compara permissionDecision.
#
# Cross-platform: setup do vault de teste cria pastas no path que Python
# resolve quando lê "/tmp/..." nos fixtures.
#   - Linux/Mac: Python resolve /tmp → /tmp (nativo)
#   - Windows (Git Bash): Python resolve /tmp → C:\tmp (literal)
#     Bash /tmp é virtualizado pra %LOCALAPPDATA%\Temp; precisa criar em /c/tmp explicitamente.

set -uo pipefail
HOOK_SCRIPT="$(dirname "$0")/../maestro-orquestra.py"
FIXTURES_DIR="$(dirname "$0")/fixtures"
EXPECTED_DIR="$(dirname "$0")/expected"

# Detecta path real onde Python resolve "/tmp"
if [[ "$(uname -s)" == MINGW* || "$(uname -s)" == MSYS* || "$(uname -s)" == CYGWIN* ]]; then
    TMP_REAL="/c/tmp"
else
    TMP_REAL="/tmp"
fi

# Setup do vault de teste (idempotente)
mkdir -p \
    "$TMP_REAL/maestro-test-vault/maestro" \
    "$TMP_REAL/maestro-test-vault/identidade" \
    "$TMP_REAL/maestro-test-vault/entregas" \
    "$TMP_REAL/maestro-test-vault/rascunhos" \
    "$TMP_REAL/maestro-test-vault/memorias/sessoes" \
    "$TMP_REAL/maestro-test-macro/cbi-of-miami/maestro" \
    "$TMP_REAL/maestro-test-macro/outro-projeto/maestro" \
    "$TMP_REAL/projeto-fora-de-vault" \
    "$TMP_REAL/maestro-test-cache-vault/identidade"
printf "modo: agent\n" > "$TMP_REAL/maestro-test-vault/maestro/config.md"
printf "modo: agent\n" > "$TMP_REAL/maestro-test-macro/cbi-of-miami/maestro/config.md"
printf "modo: agent\n" > "$TMP_REAL/maestro-test-macro/outro-projeto/maestro/config.md"

# Setup cache pra cenário 11 (vault Beta — detectado só via cache)
CACHE_DIR="$HOME/.maestro/projeto-ativo-cache"
mkdir -p "$CACHE_DIR"
# Path absoluto que Python resolve identicamente
CACHE_TEST_PATH="$TMP_REAL/maestro-test-cache-vault"
# Resolve pra path style C:/... no Windows
if [[ "$(uname -s)" == MINGW* || "$(uname -s)" == MSYS* || "$(uname -s)" == CYGWIN* ]]; then
    CACHE_TEST_PATH_RESOLVED=$(cygpath -m "$CACHE_TEST_PATH" 2>/dev/null || echo "$CACHE_TEST_PATH")
else
    CACHE_TEST_PATH_RESOLVED="$CACHE_TEST_PATH"
fi
cat > "$CACHE_DIR/test-cache-fixture.md" <<EOF
---
versao: 1
slug: cache-test
caminho-absoluto: $CACHE_TEST_PATH_RESOLVED
macro: $TMP_REAL
atualizado-em: 2026-04-29T00:00:00Z
---
EOF

PASS=0
FAIL=0

for fixture in "$FIXTURES_DIR"/*.json; do
    name=$(basename "$fixture" .json)
    expected_file="$EXPECTED_DIR/$name.json"

    if [[ ! -f "$expected_file" ]]; then
        echo "❌ $name — expected file ausente"
        FAIL=$((FAIL+1))
        continue
    fi

    # Roda o hook com a fixture via stdin
    actual=$(python3 "$HOOK_SCRIPT" < "$fixture" 2>&1)
    actual_decision=$(echo "$actual" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['hookSpecificOutput']['permissionDecision'])" 2>&1)

    expected_decision=$(python3 -c "import json; d=json.load(open('$expected_file')); print(d['hookSpecificOutput']['permissionDecision'])")

    if [[ "$actual_decision" == "$expected_decision" ]]; then
        echo "✅ $name — $actual_decision"
        PASS=$((PASS+1))
    else
        echo "❌ $name — esperado=$expected_decision, atual=$actual_decision"
        echo "    Output completo: $actual"
        FAIL=$((FAIL+1))
    fi
done

# Cleanup do cache fixture (não polui o cache real entre runs)
rm -f "$CACHE_DIR/test-cache-fixture.md"

echo ""
echo "Total: $PASS passed, $FAIL failed"
exit $FAIL
