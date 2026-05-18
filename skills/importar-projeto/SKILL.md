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
- Se `modo=bare` → segue T6.
- Se `modo=mix` → AUQ "Encontrei um arquivo .zip E pastas descompactadas na mesma pasta. Qual quer usar? (O arquivo .zip / As pastas já descompactadas / Cancelar)". Atualiza `MODO` conforme escolha.

### Turno T6 — Extração / inspeção

Se `MODO=zip`:

```bash
TMP_EXT="$TMP_REAL/maestro-import-$(date +%s)"
ZIP_PATH=$(ls "$TARGET"/*.zip | head -1)
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

### Turno T7 — Validar pré-requisitos (D11)

```bash
ARQUIVOS=$(find "$SOURCE/identidade" "$SOURCE/produtos" -name "*.md" 2>/dev/null | python -c "import sys,json; print(json.dumps([l.strip() for l in sys.stdin]))")
PRE=$(python "$HELPERS/importar_projeto.py" validate_pre_requisitos --paths "$ARQUIVOS")
OK=$(echo "$PRE" | python -c "import json,sys; print(json.load(sys.stdin)['ok'])")
```

Se `OK=False`:
- Listar arquivos inválidos com o motivo de cada um
- Render texto:
  > "Encontrei arquivos no import que não estão marcados como concluídos no projeto-origem:
  >
  > [lista de arquivos + motivo]
  >
  > Import só rola pra projetos terminados. No projeto-origem, conclui esses arquivos primeiro (status vira `concluido` quando o trabalho fecha), exporta o ZIP de novo e tenta aqui."
- Cleanup: `python "$HELPERS/importar_projeto.py" cleanup_tmp_externo --tmp "$TMP_EXT"`
- Abortar.

### Turno T8 — Validar integridade

Construir layout JSON via Bash (lista arquivos em identidade/ e em cada produto/<slug>/), passar pra `validate_integrity`.

Se `verdict=bloqueio` → render bloqueios + cleanup + abort.
Se há avisos → guardar pra mostrar no T16.

### Turno T9 — Detectar conflitos

```bash
CONFLITOS=$(python "$HELPERS/importar_projeto.py" detect_conflicts --target "$TARGET" --source "$SOURCE")
N_CONFLITOS=$(echo "$CONFLITOS" | python -c "import json,sys; print(len(json.load(sys.stdin)['conflitos']))")
```

### Turno T10 — Resolver conflitos via AUQ

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

Se "Cancelar tudo" → cleanup + abort.

### Turno T11 — Aplicar resolução

```bash
APPLY=$(python "$HELPERS/importar_projeto.py" apply_resolution --target "$TARGET" --source "$SOURCE" --decisions "$DECISIONS")
IMPORTADOS=$(echo "$APPLY" | python -c "import json,sys; print(json.load(sys.stdin)['arquivos_importados'])")
```

Cleanup do tmp externo + do ZIP original:

```bash
python "$HELPERS/importar_projeto.py" cleanup_tmp_externo --tmp "$TMP_EXT" >/dev/null
rm -f "$ZIP_PATH"
```

### Turno T12 — Scan wikilinks órfãos

```bash
PATHS_SCAN=$(python -c "import json; print(json.dumps(['$TARGET/identidade', '$TARGET/produtos']))")
ORFAOS=$(python "$HELPERS/importar_projeto.py" scan_orphan_wikilinks --paths "$PATHS_SCAN" --target "$TARGET")
TOTAL_PROC=$(echo "$ORFAOS" | python -c "import json,sys; print(json.load(sys.stdin)['total_arquivos_processados'])")
```

Se `TOTAL_PROC > 20`: durante a varredura mostrar "processando $TOTAL_PROC arquivos..." pro usuário (P12).

### Turno T13 — Write proveniência

Montar `SUMMARY=` JSON com `fonte`, `projeto_destino`, `arquivos_importados`, `avisos`, `wikilinks_orfaos`:

```bash
SUMMARY=$(python -c "
import json
print(json.dumps({
  'fonte': '$SOURCE_NAME',
  'projeto_destino': '$(basename $TARGET)',
  'arquivos_importados': $IMPORTADOS_JSON,
  'avisos': $AVISOS_JSON,
  'wikilinks_orfaos': $ORFAOS_JSON,
}))
")
python "$HELPERS/importar_projeto.py" write_provenance --target "$TARGET" --source-name "$SOURCE_NAME" --summary "$SUMMARY"
```

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
path-projeto: $TARGET")
```

Onboarding é skill, não subagent — não usar `Agent(subagent_type="maestro:maestro-onboarding", ...)` (não existe esse subagent type; tentativa de Agent retorna erro "Agent type not found" e quebra o fluxo).

Se estado 4-5: pula T15.

### Turno T16 — Resumo final

Render literal (substituir variáveis):

> "Importação concluída.
>
> Importados: <N> arquivos:
> - <lista por área>
>
> Avisos: <N>
> - <lista de avisos amigáveis>
>
> Ligações pra resolver: <N> referências apontam pra arquivos que não vieram no import. Elas vão se resolver sozinhas quando você criar esses arquivos — o Obsidian liga automaticamente. Se não criar, ficam como link quebrado dentro do arquivo (sem perder nada).
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
