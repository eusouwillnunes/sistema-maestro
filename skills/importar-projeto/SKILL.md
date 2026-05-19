---
name: importar-projeto
description: Slash command /importar-projeto. Importa identidade e/ou produto de outro projeto Maestro a partir de ZIP ou pastas descompactadas. Cria estrutura do projeto novo (em vault zerado ou workspace existente), valida pré-requisitos (status concluido), aplica conflitos via AskUserQuestion, scaffolda o resto via Bibliotecário e roda onboarding pós-import quando aplicável.
---

# Importar Projeto

Skill orquestradora do `/importar-projeto`. Trabalho determinístico no helper `plugin/core/helpers/importar_projeto.py`. Esta skill **nunca escreve no vault diretamente** (D12) — toda escrita estrutural via Bibliotecário, toda escrita de log/dados via subprocess do helper Python.

## Quando usar

Usuário roda `/importar-projeto` quando tem identidade e/ou produto de outro projeto Maestro (ZIP ou pastas descompactadas) que quer reusar no projeto atual.

## Pré-requisito absoluto

Os arquivos importados precisam ter `status: concluido` no frontmatter (D11). Helper aborta se algum vem com status diferente — usuário precisa concluir no projeto-origem antes de exportar.

## Resolver `$HELPERS`

```bash
PLUGIN_DIR=$(find "$HOME/.claude/plugins/marketplaces" -maxdepth 2 -type d -name maestro 2>/dev/null | head -1)
if [ -z "$PLUGIN_DIR" ]; then
    echo "ERRO: plugin maestro nao encontrado em ~/.claude/plugins/marketplaces" >&2
    exit 1
fi
HELPERS="$PLUGIN_DIR/core/helpers"
```

Pre-check: se `$HELPERS/importar_projeto.py` ausente → reportar `STATUS: BLOCKED` motivo "helper importar_projeto.py ausente — plugin desatualizado".

## Detectar TMP_REAL (aprendizado #74)

```bash
case "$(uname -s)" in
  MINGW*|MSYS*) TMP_REAL="/c/tmp" ;;
  *) TMP_REAL="/tmp" ;;
esac
mkdir -p "$TMP_REAL"
```

## Fluxo

### Turno T1 — Apresentação

Render literal:
> "Olá! Vou te ajudar a importar identidade e/ou produto de outro projeto Maestro. Onde tô rodando agora vai virar o projeto novo. Em alguns minutos, sua estrutura tá pronta com os arquivos importados nos lugares certos."

### Turno T2 — Detecção de estado

```bash
ESTADO_JSON=$(python "$HELPERS/importar_projeto.py" detect_state --target "$(pwd)")
```

Parse o JSON: extrair `estado` e `hints`.

### Turno T3 — Ramificação por hints e estado

**Hints excepcionais (verificar primeiro):**

- Se `hints.cwd_ambiguo` → AUQ "Qual projeto vira destino?" com opções vindas de `hints.projetos_disponiveis`. Após escolha, atualizar `TARGET=$(pwd)/<projeto-escolhido>`.
- Se `hints.config_invalida` → AUQ "Encontrei projeto com config quebrada — reparar / cancelar?". Se cancelar, abortar limpo.
- Se `hints.workspace_orfao` → AUQ "Criar projeto novo aqui dentro do workspace?". Se sim, segue como Estado 2.

**Por estado:**

- **Estado 1 (vault zerado):**
  - AUQ "Como chama a Área de Trabalho? E o projeto dentro dela?" (2 perguntas combinadas)
  - Despachar: `Agent(subagent_type="maestro:bibliotecario", prompt="FLUXO: SCAFFOLD WORKSPACE\nmodo: pre-import\nworkspace-nome: <nome>\nprojeto-nome: <nome>")`
  - Aguardar retorno; capturar `TARGET=$(pwd)/<projeto-slug>`

- **Estado 2 (workspace existente, raiz):**
  - AUQ "Como chama o projeto novo?"
  - Despachar: `Agent(subagent_type="maestro:bibliotecario", prompt="FLUXO: SCAFFOLD WORKSPACE\nmodo: pre-import-novo-projeto\nprojeto-nome: <nome>")`
  - Capturar `TARGET=$(pwd)/<projeto-slug>`

- **Estado 3-4:** `TARGET=$(pwd)` direto.

- **Estado 5 (biblioteca cheia):**
  - AUQ destrutivo (texto literal abaixo). Se Cancelar → abortar limpo.

### Turno T3 Estado 5 — texto destrutivo (literal)

```
⚠️ Esse projeto já tem identidade e produto preenchidos. Importar **vai apagar tudo isso** e colocar o que tá no ZIP no lugar. Os arquivos atuais não voltam.

Quer mesmo continuar?
- Sim, substituir (apaga o que tem aqui e usa o que vier no ZIP)
- Cancelar (não toca em nada)
```

### Turno T4 — Pedir input do usuário

Render literal (substituir `$TARGET`):

> "Pronto! Criei a pasta do seu projeto em:
>
> `$TARGET`
>
> Agora, no Explorer (ou Finder, ou onde você gerencia arquivos), abra essa pasta e copie pra dentro dela:
> - Um arquivo .zip com identidade/ e/ou produto/ dentro
> - OU as pastas `identidade/` e `produtos/` já descompactadas (se vier `produto/` no singular, o sistema converte pra `produtos/` plural — é só a convenção nossa)
>
> Quando tiver lá, me diz 'pronto'."

Aguardar resposta livre. Quando vier confirmação → seguir T5.

### Turno T5 — Scan input

```bash
SCAN=$(python "$HELPERS/importar_projeto.py" scan_input --target "$TARGET")
MODO=$(echo "$SCAN" | python -c "import json,sys; print(json.load(sys.stdin)['modo'])")
```

- Se `modo=vazio` → "Não achei nada nessa pasta. Confere se copiou certinho e me avisa de novo." Loop até 3 tentativas. Após 3: aborta.
- Se `modo=zip` → segue T6.
- Se `modo=bare` → captura `SOURCE_NAME="$(basename "$TARGET")-import-$(date +%Y%m%d-%H%M)"` e segue T6 (A12).
- Se `modo=mix` → AUQ "Encontrei um arquivo .zip E pastas descompactadas na mesma pasta. Qual quer usar? (O arquivo .zip / As pastas já descompactadas / Cancelar)". Atualiza `MODO` conforme escolha.

### Turno T6 — Extração / inspeção

Se `MODO=zip`:

```bash
TMP_EXT="$TMP_REAL/maestro-import-$(date +%s)"
ZIP_PATH=$(ls "$TARGET"/*.zip | head -1)
SOURCE_NAME=$(basename "$ZIP_PATH" .zip)
EXTRACT=$(python "$HELPERS/importar_projeto.py" extract_atomic --zip "$ZIP_PATH" --tmp "$TMP_EXT")
OK=$(echo "$EXTRACT" | python -c "import json,sys; print(json.load(sys.stdin)['ok'])")
if [ "$OK" != "True" ]; then
  # Renderizar erro traduzido — prefere mensagem-natural do JSON do helper
  MSG_NATURAL=$(echo "$EXTRACT" | python -c "import json,sys; d=json.load(sys.stdin); print(d.get('mensagem-natural',''))" 2>/dev/null)
  if [ -n "$MSG_NATURAL" ]; then
    echo "$MSG_NATURAL"
  else
    echo "Esse arquivo .zip parece corrompido (ou outro erro). Tenta de novo."
  fi
  python "$HELPERS/importar_projeto.py" cleanup_tmp_externo --tmp "$TMP_EXT" >/dev/null
  exit 1
fi
SOURCE="$TMP_EXT"
```

Se `MODO=bare`: `SOURCE="$TARGET"`.

### Turno T7 — Classificar arquivos por status (D11.1 / C6 / C7)

```bash
# Inicialização defensiva (A5 — evita variável undefined em ramos não-tomados)
INACABADOS_IMPORTADOS="[]"
INACABADOS_PATHS="[]"
INCLUIR_INACABADOS="false"
DECISAO_INACABADOS="nenhum-inacabado"

# B-Imp-cand-25: construir via Python+pathlib retorna paths nativos do SO (Windows: C:\... , Linux/Mac: /tmp/...).
# Antes usava find + stdin: em MINGW retorna paths POSIX /c/tmp/... que Python no Windows não resolve.
export SOURCE
ARQUIVOS=$(python -c "
import json, os
from pathlib import Path
src = Path(os.environ['SOURCE'])
arquivos = []
for area in ['identidade', 'produtos']:
    d = src / area
    if d.is_dir():
        arquivos.extend(str(p) for p in d.rglob('*.md'))
print(json.dumps(arquivos))
")
PRE=$(python "$HELPERS/importar_projeto.py" validate_pre_requisitos --paths "$ARQUIVOS" --source "$SOURCE")
N_INVALIDOS=$(echo "$PRE" | python -c "import json,sys; print(len(json.load(sys.stdin)['invalidos']))")
N_INACABADOS=$(echo "$PRE" | python -c "import json,sys; print(len(json.load(sys.stdin)['inacabados']))")
N_CONCLUIDOS=$(echo "$PRE" | python -c "import json,sys; print(len(json.load(sys.stdin)['concluidos']))")
```

**Branch 1: `N_INVALIDOS > 0` — BLOQUEIO (A1/C7)**

Listar inválidos com motivo traduzido:

| Motivo do helper | Texto pro user |
|---|---|
| `status-fora-do-enum` | "status `<X>` não é válido (deveria ser um de: `<enum-esperado>`)" |
| `status-vazio` | "campo `status:` está vazio" |
| `frontmatter-invalido` | "frontmatter quebrado ou ausente" |
| `tipo-ausente` | "campo `tipo:` ausente no frontmatter" |
| `arquivo-nao-existe` | "arquivo listado mas não existe no ZIP" |

Render literal:

> "Encontrei arquivos no import que o sistema não consegue processar:
>
> [lista traduzida com motivo]
>
> Esses arquivos não dá pra importar como estão. Volta no projeto-origem, conserta lá e exporta de novo."

Cleanup obrigatório + abort:
```bash
python "$HELPERS/importar_projeto.py" cleanup_tmp_externo --tmp "$TMP_EXT" >/dev/null 2>&1
exit 1
```

**Branch 2: `N_INACABADOS == 0` — segue normal**

Sem AUQ. `DECISAO_INACABADOS="nenhum-inacabado"` (já inicializada). Segue T8.

**Branch 3: `N_INACABADOS > 0 AND N_CONCLUIDOS > 0` — AUQ 3 opções**

Montar lista de inacabados em Markdown (truncar com `...e mais N` se > 10, A11):

```bash
LISTA_INACABADOS=$(echo "$PRE" | python -c "
import json, sys
data = json.load(sys.stdin)
items = data['inacabados']
trunc = items[:10]
linhas = [f\"- \`{i['path']}\` — {i['status_atual']}\" for i in trunc]
if len(items) > 10:
    linhas.append(f\"- ...e mais {len(items)-10} arquivo(s). Lista completa no log depois do import.\")
print('\\n'.join(linhas))
")
```

Render literal:

> "Trouxe arquivos que ainda não estão prontos no projeto-origem:
>
> $LISTA_INACABADOS
>
> O padrão é trazer só os arquivos terminados (mais seguro pro projeto novo). Mas se quiser trazer os inacabados também, dá pra fazer — eles vêm com o status original e você termina aqui."

AUQ 3 opções:
- **"Importar só os terminados (pula os inacabados acima)"** →
  ```bash
  INACABADOS_PATHS=$(echo "$PRE" | python -c "import json,sys; print(json.dumps([i['path'] for i in json.load(sys.stdin)['inacabados']]))")
  INCLUIR_INACABADOS="false"
  DECISAO_INACABADOS="pulou-inacabados"
  ```
- **"Importar tudo (inacabados vêm com status atual)"** →
  ```bash
  INACABADOS_IMPORTADOS=$(echo "$PRE" | python -c "import json,sys; print(json.dumps([{'path': i['path'], 'status_atual': i['status_atual']} for i in json.load(sys.stdin)['inacabados']]))")
  INCLUIR_INACABADOS="true"
  DECISAO_INACABADOS="incluiu-inacabados"
  ```
- **"Cancelar"** → cleanup + abort:
  ```bash
  python "$HELPERS/importar_projeto.py" cleanup_tmp_externo --tmp "$TMP_EXT" >/dev/null 2>&1
  exit 0
  ```

**Branch 4: `N_INACABADOS > 0 AND N_CONCLUIDOS == 0` — AUQ 2 opções (C5)**

Render literal:

> "Os arquivos do import estão todos inacabados no projeto-origem:
>
> $LISTA_INACABADOS
>
> Dá pra importar mesmo assim — eles vêm com o status original. Você termina aqui no projeto novo."

AUQ 2 opções:
- **"Importar tudo (todos vêm com status atual)"** → mesma lógica do "Importar tudo" da Branch 3.
- **"Cancelar"** → cleanup + abort (mesma lógica da Branch 3).

### Turno T8 — Validar integridade

```bash
# B-Imp-cand-23: bloco Bash explícito (antes era prosa, Maestro inventava e errava).
# validate_integrity espera dict {identidade: [arquivos], produtos: {slug: [arquivos]}}, NÃO list.
LAYOUT=$(python -c "
import json, os
from pathlib import Path
src = Path(os.environ['SOURCE'])
layout = {}
ident_dir = src / 'identidade'
if ident_dir.is_dir():
    layout['identidade'] = sorted([p.name for p in ident_dir.glob('*.md')])
prod_dir = src / 'produtos'
if prod_dir.is_dir():
    layout['produtos'] = {}
    for slug in sorted(prod_dir.iterdir()):
        if slug.is_dir():
            layout['produtos'][slug.name] = sorted([p.name for p in slug.glob('*.md')])
print(json.dumps(layout))
")
INTEG=$(python "$HELPERS/importar_projeto.py" validate_integrity --paths "$LAYOUT")
VERDICT=$(echo "$INTEG" | python -c "import json,sys; print(json.load(sys.stdin)['verdict'])")
```

`SOURCE` é env var (já exportada nos turnos anteriores quando MINGW — usar `export SOURCE` antes do bloco se ainda não estiver). Isso garante que paths Windows não quebram a heredoc Python.

Se `VERDICT=bloqueio` → render bloqueios + cleanup + abort.
Se há avisos → guardar pra mostrar no T16.

### Turno T9 — Detectar conflitos

```bash
CONFLITOS=$(python "$HELPERS/importar_projeto.py" detect_conflicts --target "$TARGET" --source "$SOURCE" --inacabados-paths "$INACABADOS_PATHS")
N_CONFLITOS=$(echo "$CONFLITOS" | python -c "import json,sys; print(len(json.load(sys.stdin)['conflitos']))")
```

Quando `INCLUIR_INACABADOS=false`, `INACABADOS_PATHS` contém os arquivos que serão pulados — o helper exclui esses dos conflitos retornados, eliminando AUQ ambíguo no T10 sobre arquivos que não vão entrar (C6 da spec v2). Quando `INCLUIR_INACABADOS=true`, `INACABADOS_PATHS` é `[]` (lista vazia) — todos os conflitos passam.

### Turno T10 — Resolver conflitos via AUQ

> [!critical] Cleanup obrigatório em qualquer cancel (A6)
> Toda saída via "Cancelar" — tanto do T7 (branches 1, 3, 4) quanto do T10 (esta etapa) — DEVE chamar `python "$HELPERS/importar_projeto.py" cleanup_tmp_externo --tmp "$TMP_EXT"` antes de abortar. Sem cleanup, o tmp fica órfão e a próxima sessão de `/importar-projeto` esbarra com fixtures de execuções abandonadas (B-Imp-cand-14).

Se `N_CONFLITOS=0` → segue T11 com `DECISIONS='{}'`.

Se `N_CONFLITOS=1` (1 grupo só) — AUQ simples:

> "Encontrei `<arquivos>` (e outros <N> arquivos) que você já tem aqui no projeto, e versões diferentes vindo no import. Qual quer manter?
> - Usar os novos do ZIP (apaga os seus)
> - Manter os seus (ignora os do ZIP)
> - Cancelar tudo"

Se `N_CONFLITOS≥2` — AUQ por grupo (texto literal abaixo):

> "Tem conflitos em mais de uma área. Decide por área:
>
> | Área | Arquivos | O que fazer? |
> |---|---|---|
> | Identidade | <N> arquivos | [Usar do ZIP / Manter o que tenho / Pular essa área] |
> | Produto: <slug> | <N> arquivos | [...] |
>
> [Confirmar / Cancelar tudo]"

Construir `DECISIONS=` JSON tipo `{"identidade": "sobrescrever", "produto/curso-x": "manter"}` conforme respostas. "Pular essa área" → `"pular"`.

Se "Cancelar tudo" — cleanup obrigatório:
```bash
python "$HELPERS/importar_projeto.py" cleanup_tmp_externo --tmp "$TMP_EXT" >/dev/null 2>&1
exit 0
```

### Turno T11+T12+T13 — Aplicar resolução, scan órfãos, write proveniência (BLOCO ÚNICO)

> [!critical] Esses 3 turnos rodam num único bloco Bash (B-Imp-cand-24)
> Cada `Bash(...)` tool call do Claude Code é um shell efêmero — `export VAR` no Bash 1 NÃO persiste no Bash 2. Solução: T11/T12/T13 ficam no mesmo bloco Bash + JSONs persistidos em arquivos temp pra evitar escape hell de paths Windows.

```bash
# === T11 — apply_resolution ===
APPLY=$(python "$HELPERS/importar_projeto.py" apply_resolution \
  --target "$TARGET" --source "$SOURCE" \
  --decisions "$DECISIONS" \
  --incluir-inacabados "$INCLUIR_INACABADOS" \
  --inacabados-paths "$INACABADOS_PATHS")
# Persistir output do apply em arquivo temp — Python lê via json.load(open(...))
# sem heredoc interpolation hell (B-Imp-cand-24 v3).
echo "$APPLY" > "$TMP_REAL/m-apply.json"

# Cleanup tmp + ZIP original
python "$HELPERS/importar_projeto.py" cleanup_tmp_externo --tmp "$TMP_EXT" >/dev/null
rm -f "$ZIP_PATH"

# === T12 — scan wikilinks órfãos ===
export TARGET
PATHS_SCAN=$(python -c "
import json, os
t = os.environ['TARGET']
print(json.dumps([os.path.join(t, 'identidade'), os.path.join(t, 'produtos')]))
")
ORFAOS=$(python "$HELPERS/importar_projeto.py" scan_orphan_wikilinks --paths "$PATHS_SCAN" --target "$TARGET")
echo "$ORFAOS" > "$TMP_REAL/m-orfaos.json"
TOTAL_PROC=$(echo "$ORFAOS" | python -c "import json,sys; print(json.load(sys.stdin)['total_arquivos_processados'])")

# Se TOTAL_PROC > 20: mostrar "processando $TOTAL_PROC arquivos..." (P12).

# === T13 — write_provenance ===
# Persistir INACABADOS_IMPORTADOS e AVISOS em arquivos (defensivo — vars do Bash
# podem ter caracteres especiais quando paths Windows envolvidos).
echo "${INACABADOS_IMPORTADOS:-[]}" > "$TMP_REAL/m-inacabados.json"
echo "${AVISOS_JSON:-[]}" > "$TMP_REAL/m-avisos.json"

# Exporta vars simples (não-JSON) pro Python ler via os.environ
export SOURCE_NAME
export DECISAO_INACABADOS
export PROJETO_DESTINO="$(basename "$TARGET")"
export TMP_REAL

# Heredoc SINGLE-QUOTED ('PYEOF') — Bash NÃO interpola nada dentro.
# Python lê JSONs de arquivos (sem escape hell) e vars simples de env.
SUMMARY=$(python <<'PYEOF'
import json, os
tmp = os.environ['TMP_REAL']
with open(tmp + '/m-apply.json', encoding='utf-8') as f:
    apply_data = json.load(f)
with open(tmp + '/m-orfaos.json', encoding='utf-8') as f:
    orfaos_data = json.load(f)
with open(tmp + '/m-inacabados.json', encoding='utf-8') as f:
    inacabados = json.load(f)
with open(tmp + '/m-avisos.json', encoding='utf-8') as f:
    avisos = json.load(f)
print(json.dumps({
    'fonte': os.environ['SOURCE_NAME'],
    'projeto_destino': os.environ['PROJETO_DESTINO'],
    'arquivos_importados': apply_data.get('arquivos_importados', []),
    'arquivos_inacabados_importados': inacabados,
    'decisao_inacabados': os.environ['DECISAO_INACABADOS'],
    'avisos': avisos,
    'wikilinks_orfaos': orfaos_data.get('orfaos', []),
}))
PYEOF
)

python "$HELPERS/importar_projeto.py" write_provenance --target "$TARGET" --source-name "$SOURCE_NAME" --summary "$SUMMARY"

# Cleanup dos arquivos temp do summary
rm -f "$TMP_REAL/m-apply.json" "$TMP_REAL/m-orfaos.json" "$TMP_REAL/m-inacabados.json" "$TMP_REAL/m-avisos.json"
```

**Por que funciona:**
1. `<<'PYEOF'` (single-quoted) impede Bash de interpolar `$VAR` dentro do heredoc.
2. JSONs vêm de arquivos via `json.load(open(...))` — sem string Python intermediária que processe `\\`.
3. Vars simples (não-JSON) vêm de `os.environ` — env vars são bytes intactos.
4. Cleanup automático dos 4 arquivos temp depois do write_provenance.

### Turno T14 — Bibliotecário scaffolda resto

```
Agent(
  subagent_type="maestro:bibliotecario",
  prompt="FLUXO: CRIAR
CONTEXTO:
modo: pos-import
path-projeto: $TARGET
areas-ja-presentes: identidade,produto"
)
```

Bibliotecário invoca `biblioteca_scaffold.py scaffold $TARGET <empresa> --plugin-dir $PLUGIN_DIR --skip-areas identidade,produto`.

### Turno T15 — Onboarding pós-import (condicional)

Se estado inicial era 1, 2 ou 3:

- Regenerar painel cross-project: `Skill(maestro:regenerar-painel)`.
- Invocar onboarding pós-import:

```
Skill("maestro:maestro-onboarding", args: "FLUXO: NOVO_PROJETO
modo: pos-import-skip-T14
path-projeto: $TARGET
contexto-import: $DECISAO_INACABADOS")
```

O onboarding lê `contexto-import` (valores: `nenhum-inacabado`, `pulou-inacabados`, `incluiu-inacabados`) e adapta o texto inicial quando `incluiu-inacabados` — avisa o user que arquivos vieram inacabados e oferece atalho pra terminá-los no painel (A8).

Onboarding é skill, não subagent — não usar `Agent(subagent_type="maestro:maestro-onboarding", ...)` (não existe esse subagent type; tentativa de Agent retorna erro "Agent type not found" e quebra o fluxo).

Se estado 4-5: pula T15.

### Turno T16 — Resumo final

Render literal (substituir variáveis):

> "Importação concluída.
>
> Importados: `<N>` arquivos:
> - <lista por área>
>
> Avisos: `<N>`
> - <lista de avisos amigáveis>"

**Bloco extra de inacabados — renderizar SÓ se `DECISAO_INACABADOS == "incluiu-inacabados"` (A7):**

> "⚠️ Importados como inacabados (`<N>` arquivos):
> - `<path>` (status: `<status_atual>`)
> - ...
>
> Esses arquivos vão aparecer no painel da Identidade (e dos Produtos, se for o caso) com o ícone `⚙️ Em andamento`, `⏳ Pendente` ou `🔍 Em revisão`, em vez de `✅ Aprovado`. Esse é o seu sinal pra terminar eles aqui no projeto novo."

**Bloco de wikilinks órfãos (lógica existente):**

> "Ligações pra resolver: `<N>` referências apontam pra arquivos que não vieram no import. Elas vão se resolver sozinhas quando você criar esses arquivos — o Obsidian liga automaticamente. Se não criar, ficam como link quebrado dentro do arquivo (sem perder nada).
>
> [lista de wikilinks órfãos: arquivo + link]
>
> Se aparecer link na lista mencionando `biblioteca-de-marketing/...` (convenção antiga), ele não vai resolver sozinho — esses arquivos agora ficam direto nas pastas como `identidade/` e `produtos/`. Edita o arquivo no Obsidian e corrige o link manualmente (procura `[[biblioteca-de-marketing/` e tira esse pedaço).
>
> Próximo passo: <continuar onboarding pós-import / começar a trabalhar>."

## Tratamento de erros

| Falha | Como reage |
|---|---|
| ZIP corrompido (T6) | "Esse arquivo .zip parece corrompido. Tenta zipar de novo no projeto-origem e refazer." |
| Permissão negada | "Não consegui mexer em `<arquivo-amigável>` — provavelmente o Obsidian tá com o arquivo aberto, ou sua sincronização (Drive/Dropbox/iCloud) tá segurando. Fecha o Obsidian, pausa a sincronização e tenta de novo." |
| Disco cheio | "Sem espaço em disco pra extrair o ZIP. Libera espaço e tenta de novo." |
| Tmp órfão de execução anterior | AUQ "Achei uma importação que não terminou de antes (de X minutos atrás). O que prefere? (Continuar / Começar do zero)" |
| Status inválido (D11) | Texto do T7 |
| Bibliotecário falha no T14 | "Os arquivos foram importados certinho, mas o passo de criar o resto da estrutura travou — roda `/biblioteca` quando puder pra completar." |
| Onboarding falha no T15 | "Import + estrutura ok, mas o último passo de configuração travou — roda `/maestro-onboarding` pra retomar." |

## Princípios

- **Skill NUNCA escreve no vault diretamente** (D12). Toda escrita estrutural via Bibliotecário; toda escrita de log/dados via subprocess Python.
- **Tmp externo (`$TMP_REAL/maestro-import-*`), não dentro do vault** (D13).
- **`status: concluido` obrigatório em arquivos importados** (D11). Aborta com mensagem clara se algum não tiver.
