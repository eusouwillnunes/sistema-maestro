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
    "$TMP_REAL/maestro-test-workspace/cbi-of-miami/maestro" \
    "$TMP_REAL/maestro-test-workspace/outro-projeto/maestro" \
    "$TMP_REAL/maestro-test-workspace/.maestro/cache" \
    "$TMP_REAL/projeto-fora-de-vault"
printf "modo: agent\n" > "$TMP_REAL/maestro-test-vault/maestro/config.md"
printf "modo: agent\n" > "$TMP_REAL/maestro-test-workspace/cbi-of-miami/maestro/config.md"
printf "modo: agent\n" > "$TMP_REAL/maestro-test-workspace/outro-projeto/maestro/config.md"
touch "$TMP_REAL/maestro-test-workspace/.maestro-workspace"

PASS=0
FAIL=0

for fixture in "$FIXTURES_DIR"/*.json; do
    name=$(basename "$fixture" .json)
    # Fixtures do hook onboarding-orquestra.py rodam em loop separado abaixo.
    [[ "$name" == onb-* ]] && continue
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

# === Hook onboarding-orquestra.py ===
ONB_HOOK="$(dirname "$0")/../onboarding-orquestra.py"

# Setup do estado de teste (idempotente)
mkdir -p \
    "$TMP_REAL/maestro-onb-test/projeto-x/memorias/onboarding" \
    "$TMP_REAL/maestro-onb-test/projeto-sem-onboarding" \
    "$TMP_REAL/maestro-onb-test/projeto-com-marker/memorias/onboarding" \
    "$TMP_REAL/maestro-onb-test/projeto-sem-marker/memorias/onboarding" \
    "$TMP_REAL/maestro-onb-test/projeto-concluido/memorias/onboarding"

# State sem markers (projeto-x e projeto-sem-marker)
for proj in projeto-x projeto-sem-marker; do
    cat > "$TMP_REAL/maestro-onb-test/$proj/memorias/onboarding/state-test.md" <<'EOF'
---
slug: test
fluxo: primeira-vez
inicio: 2026-05-06T10:00:00-03:00
---

## Markers

EOF
done

# State com marker t-auq-biblioteca
cat > "$TMP_REAL/maestro-onb-test/projeto-com-marker/memorias/onboarding/state-test.md" <<'EOF'
---
slug: test
fluxo: primeira-vez
inicio: 2026-05-06T10:00:00-03:00
---

## Markers

- t-auq-biblioteca: 2026-05-06T10:05:00-03:00
EOF

# State concluído (libera tudo via t-conclusao)
cat > "$TMP_REAL/maestro-onb-test/projeto-concluido/memorias/onboarding/state-test.md" <<'EOF'
---
slug: test
fluxo: primeira-vez
inicio: 2026-05-06T10:00:00-03:00
---

## Markers

- t-conclusao: 2026-05-06T10:30:00-03:00
EOF

for fixture in "$FIXTURES_DIR"/onb-*.json; do
    name=$(basename "$fixture" .json)
    expected_file="$EXPECTED_DIR/$name.json"

    if [[ ! -f "$expected_file" ]]; then
        echo "❌ $name — expected file ausente"
        FAIL=$((FAIL+1))
        continue
    fi

    # Roda o hook com a fixture via stdin. Fixtures usam /tmp/maestro-onb-test/...
    # que Python resolve nativamente: Linux/Mac → /tmp; Windows → C:\tmp (= /c/tmp).
    # Bash setup cria os dirs em $TMP_REAL pra bater com a resolução do Python.
    actual_file="$TMP_REAL/onb-actual.json"
    python3 "$ONB_HOOK" < "$fixture" > "$actual_file" 2>&1

    # Compara payload completo (decision + reason quando aplicável) parseando como dict
    # pra normalizar ordem de chaves do JSON serializado.
    if python3 - "$actual_file" "$expected_file" <<'PYEOF' 2>/dev/null
import json, sys
actual = json.load(open(sys.argv[1], encoding='utf-8'))
expected = json.load(open(sys.argv[2], encoding='utf-8'))
ah = actual.get('hookSpecificOutput', {})
eh = expected.get('hookSpecificOutput', {})
if ah.get('permissionDecision') != eh.get('permissionDecision'):
    sys.exit(1)
if eh.get('permissionDecision') == 'deny':
    a_reason = json.loads(ah.get('permissionDecisionReason', '{}'))
    e_reason = json.loads(eh.get('permissionDecisionReason', '{}'))
    if a_reason != e_reason:
        sys.exit(2)
sys.exit(0)
PYEOF
    then
        decision=$(python3 - "$actual_file" <<'PYEOF' 2>&1
import json, sys
print(json.load(open(sys.argv[1], encoding='utf-8'))['hookSpecificOutput']['permissionDecision'])
PYEOF
)
        echo "✅ $name — $decision"
        PASS=$((PASS+1))
    else
        echo "❌ $name"
        echo "    Esperado: $(cat "$expected_file")"
        echo "    Atual:    $(cat "$actual_file")"
        FAIL=$((FAIL+1))
    fi
done

echo ""
echo "Total: $PASS passed, $FAIL failed"
exit $FAIL
