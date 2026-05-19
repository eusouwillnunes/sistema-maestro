---
name: maestro-onboarding
description: >
  Onboarding guiado do Sistema Maestro. Apresenta o sistema, configura o projeto
  e orienta os primeiros passos. Detectado automaticamente na primeira mensagem
  ou executado manualmente a qualquer momento.
---

> [!important] Antes de executar, verifique se o Sistema Maestro está ativo neste projeto seguindo o `core/protocolos/protocolo-ativacao.md`.
> Aplica: [[protocolo-interacao]]

## 1. Detecção de Modo

Ao ser acionado, verificar o estado atual cruzando 3 sinais físicos do CWD:

1. Existe `<CWD>/.maestro-workspace`? (marker da Área de Trabalho)
2. `Glob <CWD>/*/maestro/config.md` retorna ≥1 match? (Área de Trabalho com pelo menos 1 projeto)
3. Existe `<CWD>/maestro/config.md`? (CWD é projeto Maestro)

| Sinais | Branch |
|---|---|
| (1) sim E (2) ≥1 | **Fluxo de Novo Projeto** (seção 2B) — adiciona projeto na Área de Trabalho existente |
| (1) sim E (2) = 0 | **Recuperação** — Área de Trabalho meia-criada (marker existe mas nenhum projeto). Tratada na seção 2B.-1 com AUQ "Continuar configuração / Cancelar e recomeçar / Voltar" |
| (3) sim sem (1) | CWD = projeto Maestro existente. Tratado na seção 2B.-1 com AUQ ramificado: "Criar projeto novo na mesma Área de Trabalho" / "Reconfigurar este projeto" (Seção 3) / "Voltar" |
| nenhum dos 3 | Verificar se `~/.maestro/config.md` existe (sistema já configurado antes). Se sim → **Fluxo de Novo Projeto, Caso 4** de 2B.-1 (pasta vazia + Maestro globalmente configurado). Se não → **Fluxo de Primeira Vez** (seção 2) — onboarding completo, com confirmação de pasta no T6.5 antes de criar estrutura |

**Após qualquer branch resolver:** se `<CWD>/maestro/config.md` for lido E `onboarding-completo: true` → desviar pro **Fluxo de Re-execução** (Seção 3) ANTES de executar 2/2B.

**Tabela de operações Bash auxiliares:**

```bash
# Sinal 1
[ -f "$CWD/.maestro-workspace" ] && SINAL_1=sim || SINAL_1=nao

# Sinal 2 (find em profundidade exata 3 — projetos vivem em <CWD>/<projeto>/maestro/config.md = depth 3)
# Fix B-F1-9: mindepth/maxdepth 2 deixava o find cego (depth real é 3, não 2). Validação F1 Cenário 12B confirmou empiricamente.
PROJETOS_NA_WORKSPACE=$(find "$CWD" -mindepth 3 -maxdepth 3 -path "*/maestro/config.md" 2>/dev/null | wc -l)

# Sinal 3
[ -f "$CWD/maestro/config.md" ] && SINAL_3=sim || SINAL_3=nao
```

---

## 2. Fluxo de Primeira Vez

### 2.0.A Apresentação humana e consentimento (Turnos 1-3)

> [!critical] Esta seção é GATE OBRIGATÓRIO. Skill começa com chat output ANTES de qualquer Bash, Read, Glob ou tool call. Princípio "evitar executar coisas que o usuário não saiba o que é" — variação inversa do aprendizado #39 do CLAUDE.md (chat obrigatório como Turno 1, não Bash).

#### Camadas de defesa do Fluxo de Primeira Vez (F-Onb-2A)

> [!danger] OBRIGATÓRIO — pular qualquer Camada = bug crítico
> As 4 Camadas abaixo são **defesa estrutural por construção**, não cerimônia opcional. As Camadas 3 e 4 (state file + markers + hook auditor) têm efeito INVISÍVEL pro user (audit trail), mas ativam a proteção contra B-F1-10 e disparos precoces. **NÃO PULAR sob nenhum pretexto** — incluindo "pra encurtar", "pra agilizar", "sistema funciona sem", "TodoWrite não importa", "marker pode ficar pra depois". Confessar o pulo depois NÃO é aceitável; defesa precisa estar ativa por construção. Aprendizados #38, #56, #57 e #58 do CLAUDE.md — Opus 4.7 elimina ATIVAMENTE passos de audit trail invisíveis sob justificativa "funcionalmente OK". Esta seção bloqueia esse comportamento.

**Camada 1 — TodoWrite obrigatório.** ANTES de renderizar T1, abrir TodoWrite com 16 itens (T1, T1.5, T2-T6, T6.5, T7-T9, T11-T15 conforme `turnos-onboarding.md`). Marcar `in_progress` antes do turno e `completed` depois. Pular item deixa rastro visível na UI.

> Nota Sessão 74: T1.5 (captura nome do usuário cedo) substitui T10 (que vinha tarde demais). Se `~/.maestro/memorias/nome-usuario.md` já existe, T1.5 não emite AUQ — apenas lê o nome e marca o item como `completed`.

```python
TodoWrite([
    {"content": "T1 — Apresentação humana (texto literal)", "status": "pending", "activeForm": "Apresentando"},
    {"content": "T1.5 — Nome do usuário (AUQ ou leitura de memória)", "status": "pending", "activeForm": "Capturando nome do usuário"},
    {"content": "T2 — Pré-aviso verificações (texto literal)", "status": "pending", "activeForm": "Avisando das verificações"},
    {"content": "T3 — AUQ consentimento", "status": "pending", "activeForm": "Aguardando consentimento"},
    {"content": "T4 — Verificações técnicas (Bash silencioso)", "status": "pending", "activeForm": "Verificando"},
    {"content": "T5 — Roadmap (texto literal)", "status": "pending", "activeForm": "Mostrando roadmap"},
    {"content": "T6 — Apresentação estrutura (texto literal)", "status": "pending", "activeForm": "Apresentando estrutura"},
    {"content": "T6.5 — AUQ confirmar pasta (3 opções)", "status": "pending", "activeForm": "Aguardando confirmação de pasta"},
    {"content": "T7 — AUQ nome Área de Trabalho", "status": "pending", "activeForm": "Aguardando nome workspace"},
    {"content": "T8 — AUQ nome do projeto", "status": "pending", "activeForm": "Aguardando nome projeto"},
    {"content": "T9 — Confirmação estrutura + criação pastas", "status": "pending", "activeForm": "Criando estrutura"},
    {"content": "T11 — Recado Comunidade Automators (texto literal)", "status": "pending", "activeForm": "Apresentando Comunidade"},
    {"content": "T12 — AUQ Biblioteca", "status": "pending", "activeForm": "Aguardando decisão Biblioteca"},
    {"content": "T13 — AUQ Pesquisa inicial", "status": "pending", "activeForm": "Aguardando decisão Pesquisa"},
    {"content": "T14 — AUQ Material referência", "status": "pending", "activeForm": "Aguardando decisão Material"},
    {"content": "T15 — Finalização + AUQ identidade", "status": "pending", "activeForm": "Finalizando"},
])
```

**Camada 2 — Tabela determinística.** Antes de renderizar cada turno textual, ler `plugin/skills/maestro-onboarding/turnos-onboarding.md` via `Read` e renderizar o bloco `---TEXTO-Tn---` literalmente. NÃO inlinear texto entre aspas neste SKILL.md — referenciar pela tabela. Aprendizado #52 do CLAUDE.md.

**Camada 3 — Markers de turno.** Após cada AUQ crítica, escrever marker via Bash:

```bash
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "<marker>"
```

onde `$HELPERS=$PLUGIN_DIR/core/helpers`, `$STATE_DIR=$CWD/memorias/onboarding` (path que o hook auditor inspeciona — relativo ao CWD do tool call), `$SLUG=<workspace>-<projeto>` (após T7+T8) ou `_tmp_<timestamp>` (antes). Após capturar `projeto_slug` em T8, renomear `state-_tmp_*.md` → `state-<slug>.md`.

**Camada 4 — Hook auditor.** Hook `onboarding-orquestra.py` valida marker antes de dispatch Bibliotecário CRIAR / Pesquisador / SCAFFOLD WORKSPACE. Se hook bloquear (mensagem `marker-ausente` no `permissionDecisionReason`), Maestro lê `plugin/skills/maestro/limites-maestro.md` seção "Bloqueio de turno onboarding" e re-emite a AUQ correspondente antes de tentar de novo.

#### Execução

**Turno T1 — Apresentação humana.** Marcar TodoWrite T1 `in_progress`. Renderizar literal o bloco `---TEXTO-T1---` de `turnos-onboarding.md`. Marcar TodoWrite T1 `completed`.

**Turno T1.5 — Nome do usuário.** Marcar TodoWrite T1.5 `in_progress`.

**Pré-condição:** verificar se `~/.maestro/memorias/nome-usuario.md` existe.

```bash
NOME_FILE="$HOME/.maestro/memorias/nome-usuario.md"
if [ -f "$NOME_FILE" ]; then
    NOME_USUARIO=$(grep -m1 "^nome:" "$NOME_FILE" | sed 's/^nome:[[:space:]]*//')
    [ -z "$NOME_USUARIO" ] && NOME_USUARIO=$(cat "$NOME_FILE" | head -1 | tr -d '\r\n')
    PRECISA_PERGUNTAR_NOME=nao
else
    PRECISA_PERGUNTAR_NOME=sim
fi
```

**Se `PRECISA_PERGUNTAR_NOME=nao`:** usar `<NOME>=$NOME_USUARIO` em todas as mensagens subsequentes que tenham o template. Marcar TodoWrite T1.5 `completed` e prosseguir pra T2.

**Se `PRECISA_PERGUNTAR_NOME=sim`:** renderizar literal o bloco `---TEXTO-T1.5---` de `turnos-onboarding.md`.

`AskUserQuestion`:
- question: "Como você quer que eu te chame?"
- placeholder/exemplo: "Will, Ana, Apelido — qualquer coisa que você usa no dia-a-dia."

Aguardar resposta livre. Guardar como `<NOME>`. Persistir em memória global:

```bash
mkdir -p "$HOME/.maestro/memorias"
cat > "$HOME/.maestro/memorias/nome-usuario.md" <<EOF
nome: $NOME
EOF
```

Renderizar literal o bloco `---TEXTO-T1.5-RESP---` (substituindo `<NOME>`). Marcar TodoWrite T1.5 `completed`.

> Marker `t-nome-usuario` será escrito no state file logo após o init em T3 (que ocorre depois do consentimento). Antes do init não há state file pra escrever marker.

**Turno T2 — Pré-aviso de verificações.** Marcar TodoWrite T2 `in_progress`. Renderizar literal o bloco `---TEXTO-T2---` de `turnos-onboarding.md`. Marcar TodoWrite T2 `completed`.

**Turno T3 — AskUserQuestion de consentimento.** Marcar TodoWrite T3 `in_progress`.

- question: "Pode prosseguir com as verificações?"
- options:
  - label: "Sim, pode prosseguir", description: "Vou checar dependências, permissões e o Obsidian no seu sistema."
  - label: "Agora não", description: "Encerra o onboarding aqui — pode retomar com /maestro-onboarding."

Se "Agora não" → renderizar literal o bloco `---TEXTO-T3-CANCEL---` de `turnos-onboarding.md` e encerrar skill.

Se "Sim, pode prosseguir" → **[CRITICAL]** inicializar state e markers (Camadas 3+4):

> [!critical] Bash OBRIGATÓRIO — não pular sob hipótese alguma
> Este Bash inicializa o state file que ativa as Camadas 3 (markers) e 4 (hook auditor). Sem ele, o hook libera tudo silenciosamente e B-F1-10 fica sem defesa. **NÃO PULAR pra "encurtar"**, **NÃO ASSUMIR que "sistema funciona sem"**, **NÃO ABSORVER junto com outro Bash**. Se este Bash falhar (Edit negado pelo user, erro de permissão, helper ausente), ABORTAR o onboarding com mensagem explicando "preciso ativar a auditoria do onboarding antes de seguir — posso tentar de novo?". Não silenciar, não inferir, não otimizar.

```bash
HELPERS="$PLUGIN_DIR/core/helpers"
STATE_DIR="$CWD/memorias/onboarding"
SLUG_TMP="_tmp_$(date +%s)"
mkdir -p "$STATE_DIR"
python "$HELPERS/onboarding_state.py" init "$STATE_DIR" "$SLUG_TMP" "primeira-vez"
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG_TMP" "t-consentimento"

# Se T1.5 capturou nome (sempre captura no Fluxo de Primeira Vez), gravar marker
if [ -n "$NOME" ]; then
    python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG_TMP" "t-nome-usuario"
fi

# [CRITICAL] verificação inline: state file precisa existir após init
if ! ls "$STATE_DIR"/state-${SLUG_TMP}.md >/dev/null 2>&1; then
    echo "[ERRO CRÍTICO] state file não foi criado em $STATE_DIR. ABORTAR onboarding." >&2
    exit 1
fi
```

Marcar TodoWrite T3 `completed` e seguir pra 2.0.B (verificações técnicas).

### 2.0.B Verificações técnicas pós-consentimento (Turno 4)

ANTES de criar tasks ou iniciar qualquer etapa, verificar silenciosamente o que já está configurado no ambiente do usuário:

1. **Dependências:** testar `python --version`, `pandoc --version` e bibliotecas (`docx`, `openpyxl`, `pdfplumber`)
2. **Permissões:** verificar se `.claude/settings.local.json` já tem a seção `permissions` do Maestro
3. **Memórias e config:** verificar se `maestro/config.md` e `maestro/memorias/` existem
4. **Biblioteca:** verificar se a pasta da empresa já existe com scaffold
5. **Pesquisador:** ler `~/.maestro/config.md` e verificar se `openrouter-api-key` tem valor
6. **Status Line:** ler `~/.claude/settings.json` e verificar se `statusLine` já está configurada
7. **Obsidian:** verificar se está instalado usando TODOS os métodos abaixo (em ordem):
   - Windows: testar se existe `$LOCALAPPDATA/Obsidian/Obsidian.exe` ou `$APPDATA/../Local/Obsidian/Obsidian.exe`
   - macOS: testar se existe `/Applications/Obsidian.app`
   - Linux: testar `which obsidian`
   - **NÃO usar `where obsidian`** — o Obsidian não registra no PATH do Windows
   - Se encontrado em qualquer método, marcar como instalado

Guardar o resultado em memória para uso nos passos seguintes. Etapas já concluídas serão puladas automaticamente com aviso ao usuário (ex: "Dependências já instaladas. Pulando.").

**Exceção:** a etapa do Obsidian (2.7) NUNCA é pulada pelo checklist. Mesmo se detectado como instalado, sempre apresentar a etapa (o usuário pode precisar configurar o vault).

### 2.0.C Roadmap (Turno 5)

**Turno T5.** Marcar TodoWrite T5 `in_progress`. Renderizar literal o bloco `---TEXTO-T5---` de `turnos-onboarding.md`. Marcar TodoWrite T5 `completed`.

### 2.0.1 Tasks visuais

APÓS o roadmap, criar tasks visuais no terminal. Criar APENAS as tasks de etapas que precisam ser executadas (pular as já concluídas):

```
TaskCreate({ subject: "Apresentar o Sistema Maestro", description: "Boas-vindas, nome do usuário e recado da Comunidade", activeForm: "Apresentando o Sistema Maestro" })
TaskCreate({ subject: "Configurar projeto", description: "Coletar nome da empresa", activeForm: "Configurando projeto" })
TaskCreate({ subject: "Verificar dependências", description: "Instalar ferramentas necessárias para leitura de documentos", activeForm: "Verificando dependências" })
TaskCreate({ subject: "Configurar permissões", description: "Pedir autorização para as permissões do sistema", activeForm: "Configurando permissões" })
TaskCreate({ subject: "Setup técnico", description: "Criar memórias, config e CLAUDE.md", activeForm: "Executando setup técnico" })
TaskCreate({ subject: "Criar Biblioteca de Marketing", description: "Scaffold da biblioteca no vault", activeForm: "Criando Biblioteca de Marketing" })
TaskCreate({ subject: "Configurar Obsidian", description: "Guia de instalação e configuração do editor visual", activeForm: "Configurando Obsidian" })
TaskCreate({ subject: "Configurar Pesquisador", description: "Opções de pesquisa básica e avançada", activeForm: "Configurando Pesquisador" })
TaskCreate({ subject: "Pesquisa inicial do negócio", description: "Analisar site e redes sociais do cliente", activeForm: "Pesquisando sobre o negócio" })
TaskCreate({ subject: "Importar material de referência", description: "Importar documentos existentes do negócio", activeForm: "Importando material de referência" })
TaskCreate({ subject: "Configurar Status Line", description: "Barra de status no terminal", activeForm: "Configurando Status Line" })
TaskCreate({ subject: "Finalizar onboarding", description: "Encerrar com sugestão de primeira ação", activeForm: "Finalizando onboarding" })
```

Marcar cada task como `in_progress` ANTES de executar a etapa e `completed` LOGO APÓS terminar.

### 2.0.2 Criar tarefa no vault

Se o projeto já tem pasta `tarefas/` configurada (verificar se `{projeto}/tarefas/_tarefas.md` existe):

Acionar Gerente de Projetos via Agent(haiku):

- Bloco TAREFA: "Criar tarefa para: Onboarding do projeto {nome da empresa}"
- Bloco CONTEXTO:
  - Agente: maestro
  - Categoria: geral
  - Solicitante: [nome do usuário]
  - Caminho do projeto: [CWD]
  - Grupo: onboarding
  - Prioridade: alta
  - Checklist personalizado (não usar checklist da categoria):
    - [ ] Verificar dependências
    - [ ] Configurar permissões
    - [ ] Setup técnico
    - [ ] Criar Biblioteca de Marketing
    - [ ] Configurar Obsidian
    - [ ] Configurar Pesquisador
    - [ ] Pesquisa inicial do negócio
    - [ ] Importar material de referência
    - [ ] Configurar Status Line

Guardar o caminho do arquivo de tarefa retornado pelo Gerente para usar na conclusão (step 2.12.1).

Se o projeto ainda não tem pasta `tarefas/` (primeira vez, setup técnico ainda não rodou):
- Pular esta etapa. A tarefa será criada após o setup técnico — ver step 2.5.1.

### 2.0.3 Marcadores visuais

> [!critical] OBRIGATÓRIO renderizar antes de cada etapa (B-OnbUX-2A-6)
> O separador visual abaixo é **parte literal do output** ao iniciar cada etapa principal — não é decoração opcional. NÃO PULAR sob pretexto "encurta o fluxo" ou "user já sabe onde está". Modelo Opus tende a omitir marcadores visuais quando "parece redundante" (aprendizados #52 e #58); resista. Renderize antes da primeira mensagem de cada etapa (Configurar projeto, Verificar dependências, Configurar permissões, Setup técnico, Criar Biblioteca, Configurar Obsidian, Configurar Pesquisador, Pesquisa inicial, Material de referência, Configurar Status Line, Finalizar).

Ao iniciar cada etapa, exibir um separador visual antes da mensagem ao usuário:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Passo N de T — Nome da etapa
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Onde N é o número do passo atual e T é o total de passos a executar (descontando os pulados pelo checklist). Isso ajuda o usuário a saber onde está no processo.

### 2.1 Apresentação da estrutura (Turno 6)

Marcar task "Configurar projeto" como `in_progress`.

**Turno T6.** Marcar TodoWrite T6 `in_progress`. Renderizar literal o bloco `---TEXTO-T6---` de `turnos-onboarding.md`. Marcar TodoWrite T6 `completed`.

### 2.1.5 Confirmação de localização (Turno T6.5)

> Princípio "perguntar antes de criar" (F-Onb-2A). User precisa ter agência sobre onde a Área de Trabalho será criada. 3 opções: criar na pasta atual, criar em subpasta, ou ir pra outra pasta.

**Turno T6.5.** Marcar TodoWrite T6.5 `in_progress`. Renderizar literal o bloco `---TEXTO-T6.5---` de `turnos-onboarding.md` (substituindo `<CWD>` pelo CWD atual).

`AskUserQuestion`:
- question: "Onde quer criar a Área de Trabalho?"
- options:
  - label: "Aqui mesmo nesta pasta", description: "A pasta atual vira a Área de Trabalho. Crio o marker e sigo o setup aqui."
  - label: "Em uma subpasta nova", description: "Crio uma subpasta com o nome da Área de Trabalho dentro da pasta atual e monto tudo lá dentro."
  - label: "Em outra pasta", description: "Encerro o onboarding aqui — abre o Claude Code na pasta que você quer e me chama de novo."

**Pós-resposta:**

- **"Aqui mesmo nesta pasta"** → guardar `SUBFOLDER_CHOICE=aqui`. Renderizar literal `---TEXTO-T6.5-AQUI---`. Persistir marker:

  ```bash
  SUBFOLDER_CHOICE=aqui
  python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG_TMP" "t-confirmacao-pasta"
  ```

  Marcar TodoWrite T6.5 `completed`. Prosseguir pra 2.2 (T7). Em T9 (criação de pastas), `WORKSPACE_PATH=$CWD`.

- **"Em uma subpasta nova"** → guardar `SUBFOLDER_CHOICE=subpasta`. Renderizar literal `---TEXTO-T6.5-SUBPASTA---`. Persistir marker:

  ```bash
  SUBFOLDER_CHOICE=subpasta
  python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG_TMP" "t-confirmacao-pasta"
  ```

  Marcar TodoWrite T6.5 `completed`. Prosseguir pra 2.2 (T7). Em T9 (criação de pastas), `WORKSPACE_PATH=$CWD/$workspace_slug` (slug derivado do nome da Área de Trabalho capturado em T7).

- **"Em outra pasta"** → renderizar literal `---TEXTO-T6.5-OUTRA---` e encerrar skill. Não criar marker `.maestro-workspace`. Não rodar mkdir. State file `state-_tmp_*.md` fica órfão e é limpo no próximo `/ola-maestro` (>24h).

> Decisão `SUBFOLDER_CHOICE` é consumida em 2.5 (criação de estrutura): `WORKSPACE_PATH` é resolvido conforme acima APÓS T7 capturar `workspace_slug`.

### 2.2 Nome da Área de Trabalho e nome do primeiro projeto (Turnos 7-9)

> Marcar TodoWrite T7 `in_progress` antes do passo 1; T7 `completed` após guardar `workspace_legivel`. Marcar TodoWrite T8 `in_progress` antes do passo 2; T8 `completed` após guardar `projeto_legivel`. Os AUQs abaixo correspondem aos blocos de T7 e T8 em `turnos-onboarding.md` — texto e opções devem bater literalmente com a tabela.

**1. Coletar nome da Área de Trabalho via `AskUserQuestion`:**

- question: "Qual o nome dessa Área de Trabalho?"
- placeholder/exemplo no enunciado: "ex: 'Marketing Primum', 'Agência X', 'Meus Clientes'"
- Aguardar resposta livre.
- Guardar como `workspace_legivel` (string original do usuário).
- Computar `workspace_slug_proposto = slugify(workspace_legivel)` (ver função `slugify` formal na spec § "Schema dos artefatos").

**2. Coletar nome do primeiro projeto via `AskUserQuestion`:**

- question: "E qual é o nome do primeiro projeto?"
- placeholder/exemplo: "uma empresa, cliente ou marca que você vai trabalhar"
- Aguardar resposta livre.
- Guardar como `projeto_legivel` (string original do usuário). Esse valor é o **`{nome-alvo}`** referenciado nas mensagens subsequentes da skill.
- Computar `projeto_slug_proposto = slugify(projeto_legivel)`.

**3. Validação anti-colisão (F1-D7 + P12):**

Se `workspace_slug_proposto == projeto_slug_proposto`:

`AskUserQuestion`:
- question: "Os dois ficaram com o mesmo nome curto (`<workspace_slug_proposto>`). Sugiro deixar a Área de Trabalho mais geral (ex: 'Meu Trabalho') e o projeto específico (ex: '`<projeto_legivel>`'). Quer trocar?"
- options:
  - label: "Trocar Área de Trabalho", description: "Volta pro passo 1 e digita outro nome"
  - label: "Trocar projeto", description: "Volta pro passo 2 e digita outro nome"
  - label: "Manter assim", description: "Aceita os slugs idênticos sob seu risco"

Se "Trocar Área de Trabalho" → repetir passo 1.
Se "Trocar projeto" → repetir passo 2.
Se "Manter assim" → seguir.

**4. Preview de slugs:**

> [!critical] Pergunta varia por `SUBFOLDER_CHOICE` (B-OnbUX-2A-7)
> Se `SUBFOLDER_CHOICE=aqui`, NÃO mencionar criação da pasta `<workspace_slug>` — ela não vai existir. Se `SUBFOLDER_CHOICE=subpasta`, manter texto original. Mensagem mentirosa quebra confiança.

`AskUserQuestion`:
- question (se `SUBFOLDER_CHOICE=aqui`): "Vou criar a pasta `<projeto_slug_proposto>` aqui em `<CWD>` (sem subpasta `<workspace_slug_proposto>` — você escolheu usar esta pasta direto). Tudo bem ou quer mudar algum nome?"
- question (se `SUBFOLDER_CHOICE=subpasta`): "Vou criar pasta `<workspace_slug_proposto>` com `<projeto_slug_proposto>` dentro. Tudo bem ou quer mudar algum nome?"
- options:
  - label: "Tudo bem", description: "Cria com esses slugs"
  - label: "Mudar Área de Trabalho", description: "Digito o slug direto (sem espaço, só letras minúsculas, números e hífens)"
  - label: "Mudar projeto", description: "Digito o slug direto"

Se "Mudar Área de Trabalho" → pedir slug direto via texto livre, validar regex `^[a-z0-9-]+$`, sem hífen nas pontas, max 80 chars. Se inválido, repetir até passar. Atualizar `workspace_slug_proposto`.

Se "Mudar projeto" → idem pra `projeto_slug_proposto`.

Se "Tudo bem" → fixar slugs definitivos:
- `workspace_slug = workspace_slug_proposto`
- `projeto_slug = projeto_slug_proposto`

**5. Validação adicional pós-slugify (R9):**

Se `workspace_slug` ou `projeto_slug` resultar em string vazia ou só hifens (ex: input "🌴🌴🌴"):

`AskUserQuestion`:
- question: "Não consegui transformar `<input>` em pasta válida. Pode digitar um nome curto sem caracteres especiais (só letras, números e espaço)?"
- options:
  - label: "Digitar de novo", description: "Volta pra etapa 1 ou 2"

Repetir até `slugify` produzir resultado não-vazio.

**6. Persistir slug definitivo no state file (Camada 3):**

```bash
SLUG=$(python "$HELPERS/onboarding_state.py" slug "$WORKSPACE_NAME" "$PROJETO_NAME")
mv "$STATE_DIR/state-$SLUG_TMP.md" "$STATE_DIR/state-$SLUG.md"
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-nome-workspace"
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-nome-projeto"
```

Onde `$WORKSPACE_NAME=<workspace_legivel>` e `$PROJETO_NAME=<projeto_legivel>` são as strings capturadas nos passos 1 e 2.

Marcar task "Configurar projeto" como `completed`.

### 2.2.bis Confirmação da estrutura e aviso do marker (Turno 9)

**Turno T9.** Marcar TodoWrite T9 `in_progress`. Renderizar literal o bloco `---TEXTO-T9---` de `turnos-onboarding.md`, substituindo `{workspace_legivel}` e `{projeto_legivel}` pelos valores capturados nos Turnos 7 e 8. Marcar TodoWrite T9 `completed` somente após o setup técnico (seção 2.5) terminar de criar a estrutura física.

### 2.2.ter — REMOVIDO (Sessão 74, refinamento F-Onb-2A)

> Captura do nome do usuário foi movida pra **T1.5** (seção 2.0.A, logo após T1 Apresentação humana). A persistência em `~/.maestro/memorias/nome-usuario.md` e o marker `t-nome-usuario` agora acontecem em T1.5/após init. Este placeholder existe pra manter numeração de seções subsequentes; nada a executar aqui.

### 2.2.qua Recado da Comunidade Automators (Turno 11)

**Turno T11.** Marcar TodoWrite T11 `in_progress`. Renderizar literal o bloco `---TEXTO-T11---` de `turnos-onboarding.md`. Marcar TodoWrite T11 `completed`.

> [!critical] Renderizar TEXTO-T11 INTEGRAL — proibido omitir o link da Comunidade (B-OnbUX-2A-13)
> O bloco tem 3 parágrafos e a linha final com URL `https://automators.com.br` é parte literal — NÃO opcional. Aprendizado #52: Opus tende a paragrafrar e cortar a última linha quando "parece redundante" ou "fora do tom". Resista. Pre-output verification: confirme que a string `automators.com.br` aparece no que você vai renderizar antes de mandar.

Marcar task "Apresentar o Sistema Maestro" como `completed`.

**Após renderizar T11, emitir `AskUserQuestion` de continuidade:**

- question: "Podemos continuar?"
- options:
  - label: "Sim, vamos seguir", description: "Continua pra verificação de dependências."
  - label: "Pausa", description: "Encerra aqui — você pode retomar com /maestro-onboarding."

Se "Pausa" → encerrar skill silenciosamente (state file fica como órfão, cleanup automático em 24h via `/ola-maestro`).

### 2.3 Verificar dependências

Marcar task "Verificar dependências" como `in_progress`.

O Maestro precisa de ferramentas instaladas pra ler diferentes formatos de arquivo (PDF, DOCX, XLSX, etc.). Verificar e instalar o que for necessário.

1. **Verificar Python:**
   - Tentar `python --version`, depois `python3 --version` como fallback
   - Se nenhum funcionar: informar que o Python é necessário e pedir pro usuário instalar

2. **Corrigir python3 no Windows (se necessário):**
   - Testar `python3 --version` — se retornar exit code 49, é o atalho da Microsoft Store que não funciona
   - Se detectado: informar ao usuário:
     > "Detectei que o comando `python3` no seu computador aponta pra Microsoft Store em vez do Python real. Isso impede a leitura de documentos Word, PDF e Excel.
     >
     > Pra resolver, vou criar um atalho que faz o `python3` apontar pro Python que você já tem instalado. Isso envolve dois ajustes simples:
     > - Criar um arquivo em `~/.local/bin/python3` (um atalho pro Python real)
     > - Adicionar essa pasta no PATH do seu terminal (pra ele encontrar o atalho)
     >
     > Nada é desinstalado ou alterado no seu Python."

     Após o texto explicativo, emitir `AskUserQuestion` (B-S55-8):
     - question: "Posso criar o atalho do `python3` apontando pro Python real?"
     - options:
       - label: "Sim, pode fazer", description: "Cria atalho + ajusta PATH automaticamente."
       - label: "Não", description: "Pula — leitura de Word/PDF/Excel pode ficar limitada."

   - **Se sim:** executar:
     ```bash
     mkdir -p ~/.local/bin
     echo '#!/bin/bash
     exec python "$@"' > ~/.local/bin/python3
     chmod +x ~/.local/bin/python3
     ```
     Verificar se `~/.bash_profile` já tem `$HOME/.local/bin` no PATH. Se não:
     ```bash
     echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bash_profile
     export PATH="$HOME/.local/bin:$PATH"
     ```
     Confirmar: `python3 --version` deve funcionar
   - **Se não:** informar que a leitura de alguns formatos pode não funcionar e seguir adiante

3. **Verificar pandoc:**
   - Testar `pandoc --version`
   - Se não encontrado: adicionar à lista de ferramentas a instalar
   - Windows: `winget install pandoc` (ou pedir pro usuário instalar manualmente via https://pandoc.org/)
   - macOS: `brew install pandoc`
   - Linux: `sudo apt install pandoc` ou equivalente

4. **Verificar bibliotecas de leitura de documentos:**
   - Testar: `python -c "import docx" 2>/dev/null`, `python -c "import openpyxl" 2>/dev/null`, `python -c "import pdfplumber" 2>/dev/null`
   - Listar o que está faltando

5. **Pedir autorização pra instalar:**

   Se faltam ferramentas ou bibliotecas:
   > "Pra ler seus documentos (PDF, Word, Excel), preciso instalar algumas ferramentas:
   >
   > {lista do que falta, ex: pandoc, python-docx, openpyxl, pdfplumber}"

   Após o texto explicativo, emitir `AskUserQuestion` (B-S55-8):
   - question: "Posso instalar essas ferramentas agora?"
   - options:
     - label: "Sim, pode instalar", description: "Roda os comandos de instalação."
     - label: "Não", description: "Pula — leitura de alguns formatos pode não funcionar."

   **Se sim:** executar os comandos de instalação (pandoc via gerenciador de pacotes do SO, bibliotecas Python via `python -m pip install {pacotes faltantes}`)
   **Se não:** informar que a leitura de alguns formatos pode não funcionar e seguir adiante

6. Se tudo já está instalado, informar brevemente: "Dependências verificadas. Tudo pronto pra leitura de documentos."

Marcar task "Verificar dependências" como `completed`.

**Emitir `AskUserQuestion` de continuidade (B-S55-8):**

- question: "Podemos continuar?"
- options:
  - label: "Sim, vamos seguir", description: "Continua pra próxima etapa do onboarding."
  - label: "Pausa", description: "Encerra aqui — você retoma depois com /maestro-onboarding."

Se "Pausa" → encerrar skill silenciosamente.

### 2.3.5 Verificar ~/.maestro/

Executar silenciosamente, sem mensagem detalhada ao usuário:

1. Verificar se `~/.maestro/` existe: `test -d ~/.maestro`
2. Se **NÃO existir** → criar a estrutura:
   ```bash
   mkdir -p ~/.maestro/memorias/agentes ~/.maestro/overrides ~/.maestro/personas ~/.maestro/templates
   ```
3. Verificar se `~/.maestro/config.md` existe: `test -f ~/.maestro/config.md`
   - Se **NÃO existir** → copiar o template inicial: `cp [plugin]/user/config.md ~/.maestro/config.md`
   - Substituir `[plugin]` pelo caminho real do diretório do plugin (onde está o SKILL.md)
4. Se já existir → manter sem alteração (preservar configurações do usuário)
5. Verificar se `~/.maestro/templates/catalogo-tags.md` existe: `test -f ~/.maestro/templates/catalogo-tags.md`
   - Se **NÃO existir** → criar vazio com frontmatter padrão:
     ```yaml
     ---
     tipo: catalogo
     area: tags
     descricao: "Overrides aditivos do catálogo de tags do usuário"
     ---

     # Catálogo de Tags (overrides)

     > Este arquivo ACRESCENTA ao catálogo core (`plugin/core/templates/catalogo-tags.md`).
     > Tags aprovadas pelo usuário via AskUserQuestion são gravadas aqui automaticamente pelo Maestro.
     ```
   - Se já existir → manter sem alteração (preservar catálogo existente)

Informar brevemente apenas se precisou criar: "Diretório `~/.maestro/` criado para suas configurações globais."

### 2.4 Permissões do projeto

Marcar task "Configurar permissões" como `in_progress`.

Explicar ao usuário o que são as permissões e pedir consentimento ANTES de criar qualquer coisa (substituir `{CWD}` pelo caminho real):

> "Pra funcionar bem, o Maestro precisa de permissão pra ler, criar e editar arquivos dentro desta pasta (`{CWD}`).
>
> Sem isso, ele precisaria pedir sua autorização a cada arquivo, o que tornaria o trabalho bem lento.
>
> As permissões ficam restritas a este projeto. Fora desta pasta, o Maestro só acessa configurações do próprio Claude Code (como a barra de status)."

Após o texto explicativo, emitir `AskUserQuestion` (B-S55-8):
- question: "Posso configurar essas permissões?"
- options:
  - label: "Sim, pode configurar", description: "Cria/atualiza `.claude/settings.local.json` com a lista padrão."
  - label: "Não", description: "Maestro vai pedir autorização a cada arquivo durante o uso."

**Se sim:**

Criar ou atualizar `.claude/settings.local.json` no diretório atual. Se o arquivo já existir, preservar chaves existentes e adicionar/atualizar apenas `permissions`.

```json
{
  "permissions": {
    "allow": [
      "Read(/**)",
      "Write(/**)",
      "Edit(/**)",
      "Glob",
      "Grep",
      "Read(~/.claude/**)",
      "Edit(~/.claude/settings.json)",
      "Write(~/.claude/maestro-statusline.sh)",
      "Bash(mkdir *)",
      "Bash(chmod *)",
      "Bash(cp *)",
      "Bash(ls *)",
      "Bash(python *)",
      "Bash(curl *)",
      "WebSearch",
      "WebFetch(domain:*)"
    ]
  }
}
```

Confirmar: "Permissões configuradas. Ficam salvas em `.claude/settings.local.json` e valem só pra este projeto."

**Se não:**

Informar: "Sem problema. O Maestro vai funcionar, mas vai pedir sua autorização com mais frequência durante o uso."

Marcar task "Configurar permissões" como `completed`.

**Emitir `AskUserQuestion` de continuidade (B-S55-8):**

- question: "Podemos continuar?"
- options:
  - label: "Sim, vamos seguir", description: "Continua pra próxima etapa do onboarding."
  - label: "Pausa", description: "Encerra aqui — você retoma depois com /maestro-onboarding."

Se "Pausa" → encerrar skill silenciosamente.

### 2.5 Setup técnico

Marcar task "Setup técnico" como `in_progress`.

Executar silenciosamente (sem mensagens detalhadas para cada item):

1. **Resolver `WORKSPACE_PATH` e criar estrutura** (baseado em `SUBFOLDER_CHOICE` capturado em T6.5):

   ```bash
   if [ "$SUBFOLDER_CHOICE" = "aqui" ]; then
       WORKSPACE_PATH="$CWD"
   else
       # SUBFOLDER_CHOICE=subpasta → workspace numa subpasta nova
       WORKSPACE_PATH="$CWD/<workspace_slug>"
   fi
   PROJETO_PATH="$WORKSPACE_PATH/<projeto_slug>"

   mkdir -p "$PROJETO_PATH"
   ```

   Daqui em diante, `PROJETO_PATH` e `WORKSPACE_PATH` resolvidos conforme acima.

2. **Criar marker da Área de Trabalho:**

   Copiar template:
   ```bash
   cp "<plugin-root>/core/templates/workspace/.maestro-workspace" "$WORKSPACE_PATH/.maestro-workspace"
   ```

   Ou inline (caso `<plugin-root>` não esteja disponível):
   ```bash
   printf '# Marker do Sistema Maestro — esta pasta é uma Área de Trabalho.\n# Não apague: a detecção de cenário do Onboarding usa este arquivo.\n' > "$WORKSPACE_PATH/.maestro-workspace"
   ```

3. **Ativar sistema:** setar `maestro-ativo: true` em `~/.maestro/config.md`

4. **Memórias de projeto:** criar `$PROJETO_PATH/maestro/memorias/` usando templates de `core/templates/_memorias-projeto-template.md`:
   - `maestro/memorias/_index.md`
   - `maestro/memorias/contexto.md`
   - `maestro/memorias/sessoes/` (pasta vazia; `_sessoes.md` é criado pelo /tchau-maestro na primeira sessão)
   - `maestro/memorias/decisoes.md`
   - `maestro/memorias/preferencias-classificacao.md` — copia de `core/templates/_preferencias-classificacao-template.md` (v2.12.0, Bug 4). Maestro preenche ao longo do uso conforme você responde AskUserQuestion de ambiguidade. Após 3 escolhas iguais pro mesmo padrão, vira preferência aplicada automaticamente com opção de override.
   - `maestro/memorias/pendencias-aceitas/historico.md` — copia de `core/templates/_pendencias-aceitas-historico-template.md` (v2.12.0 origem, v2.23.2 reorganizado). Registra longitudinalmente usos da opção "forçar entrega com pendência" em QA/Revisor. Após 3 usos, Maestro bloqueia a opção e força revisão estrutural do checklist.
   - `maestro/memorias/agentes/` (pasta vazia)

   O arquivo `memorias/decisoes.md` começa vazio e será preenchido automaticamente conforme você toma decisões estratégicas durante o uso do Maestro (arquétipo, formato de lançamento, tom de voz, etc.). O sistema reusa escolhas anteriores pra manter coerência entre entregas.

5. **Config do projeto:** criar `$PROJETO_PATH/maestro/config.md` usando `core/templates/_maestro-config-template.md`:
   - Preencher `Empresa:` com `<projeto_legivel>`
   - Preencher `Vault:` com `$PROJETO_PATH`
   - Preencher `Projeto iniciado em:` com a data atual
   - Manter `onboarding-completo: false` (será atualizado no final)

6. **CLAUDE.md do projeto:** despachar Bibliotecário pra criar/anexar seção Maestro:

   ```python
   Agent(
     subagent_type="maestro:bibliotecario",
     prompt="""
     CONTEXTO:
     path-projeto: $PROJETO_PATH

     FLUXO: CRIAR_CLAUDE_PROJETO
     """
   )
   ```

   O Bibliotecário cria `$PROJETO_PATH/CLAUDE.md` (ou anexa seção `## Maestro` se já existir). Hook PreToolUse libera porque Bibliotecário é subagente (tem `agent_id`). Idempotente — se Bibliotecário retornar `ALREADY_EXISTS`, prosseguir silencioso.

7. **Despachar Bibliotecário SCAFFOLD WORKSPACE (stub em F1, F2/F4 preenchem):**

   ```python
   Agent(
     subagent_type="maestro:bibliotecario",
     prompt="""
     CONTEXTO:
     workspace: $WORKSPACE_PATH
     projeto-slug: <projeto_slug>

     FLUXO: SCAFFOLD WORKSPACE
     """
   )
   ```

   Em F1 retorna `STATUS: DONE` validando o marker. Em F2/F4 vai preencher painel + bookmarks. Se retornar `BLOCKED` (marker ausente), abortar com erro — o passo 2 deveria ter criado.

8. **Memórias de usuário:** verificar se `~/.maestro/memorias/_index.md` existe. Se não existe, criar a estrutura `~/.maestro/` (conforme passo 2.3.5).

9. **Cache de projeto ativo:** persistir o projeto recém-criado em `<workspace>/.maestro/cache/projeto-ativo.md` (ver protocolo-ativacao.md Sub-fluxo 1.5):

   ```bash
   # Normalizar WORKSPACE_PATH para formato Windows (C:/...) ou forward slash.
   # Fix B-F1-4: cygpath converte /c/dev/... → C:/dev/... no Git Bash do Windows.
   # Fix B-OnbUX-2A-8: bash parameter expansion substitui `tr '\\' '/'` (que emitia
   # warning "unescaped backslash at end of string" em algumas versões de tr).
   if command -v cygpath >/dev/null 2>&1; then
     WORKSPACE=$(cygpath -m "$WORKSPACE_PATH")
   else
     WORKSPACE="${WORKSPACE_PATH//\\//}"
   fi
   TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
   mkdir -p "$WORKSPACE/.maestro/cache"
   cat > "$WORKSPACE/.maestro/cache/projeto-ativo.md" <<EOF
   ---
   versao: 1
   slug: <projeto_slug>
   caminho-absoluto: ${WORKSPACE}/<projeto_slug>
   workspace: ${WORKSPACE}
   atualizado-em: ${TIMESTAMP}
   ---
   EOF
   ```

   Onde `<workspace_slug>` e `<projeto_slug>` foram fixados na etapa 2.2. **Importante (fix B-F1-7):** este Bash heredoc é obrigatório — não substituir por Write/Edit. O `$(date)` precisa rodar no shell pra timestamp ser real; se o modelo usar Edit/Write em vez de Bash, o timestamp sai inferido como `T00:00:00Z`. Se o Write falhar por permissão, aviso "cache não pode ser persistido — projeto ativo válido só nessa sessão" e segue.

Informar brevemente: "Estrutura da Área de Trabalho e do projeto criadas."

Marcar task "Setup técnico" como `completed`.

### 2.5.1 Criar tarefa no vault (se não criada em 2.0.2)

Se a tarefa de onboarding ainda não foi criada (pasta `tarefas/` foi criada agora pelo setup técnico):
- Acionar Gerente de Projetos via Agent(haiku) com o mesmo payload descrito em 2.0.2
- Guardar caminho do arquivo de tarefa para usar na conclusão (step 2.12.1)

### 2.6 Biblioteca de Marketing (Turno 12)

Marcar task "Criar Biblioteca de Marketing" como `in_progress`. Marcar TodoWrite T12 `in_progress`.

**Turno T12.** Renderizar literal o bloco `---TEXTO-T12---` de `turnos-onboarding.md` (substituir `{nome-alvo}` por `<projeto_legivel>`).

Em seguida, emitir AUQ correspondente a T12:

- question: "Quer criar a Biblioteca de Marketing agora?"
- options:
  - label: "Criar agora (Recomendado)", description: "Monta a estrutura com todos os templates prontos pra preencher"
  - label: "Depois", description: "Pula por enquanto. Você cria quando quiser pedindo 'cria minha biblioteca'"

**Persistir marker da Camada 3 ANTES de qualquer dispatch:**

```bash
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-auq-biblioteca"
```

**Se sim:**
- Despachar o Bibliotecário via `Agent(subagent_type="maestro:bibliotecario", prompt="FLUXO: CRIAR\nCONTEXTO:\nnome-empresa: {nome-coletado-no-passo-2.1}\npath-projeto: {CWD}")` para fazer scaffold dentro da pasta da empresa. Hook PreToolUse libera porque Bibliotecário é subagente; hook auditor `onboarding-orquestra.py` libera porque marker `t-auq-biblioteca` foi gravado acima.
- Informar literal: "Biblioteca criada! Você pode preencher os templates quando quiser. O sistema funciona mesmo sem eles preenchidos."

**Se não/depois:**
- Informar literal: "Sem problema! Quando quiser criar, é só pedir: 'cria minha biblioteca de marketing'."

Marcar task "Criar Biblioteca de Marketing" como `completed`. Marcar TodoWrite T12 `completed`.

### 2.6.1 Validação automática

O Maestro valida cada entrega contra um checklist automático antes de te entregar. Se algum critério falhar, o Revisor corrige antes de chegar até você.

Você pode personalizar critérios do projeto **{nome-alvo}** editando arquivos em `{projeto}/maestro/checklists/` — o Maestro acabou de criar essa pasta com um README explicando como usar.

Usar `AskUserQuestion`:
- question: "Quer que eu te mostre o README com um exemplo?"
- options:
  - label: "Sim, abre o README", description: "Te mostro como adicionar critérios próprios"
  - label: "Não, vamos seguir", description: "Pulamos pra próxima etapa"

**Se sim:** orientar o usuário a abrir `{projeto}/maestro/checklists/README.md` no Obsidian (ou editor de preferência) — o conteúdo já tem exemplos de customização.

**Emitir `AskUserQuestion` de continuidade (B-S55-8):**

- question: "Podemos continuar?"
- options:
  - label: "Sim, vamos seguir", description: "Continua pra próxima etapa do onboarding."
  - label: "Pausa", description: "Encerra aqui — você retoma depois com /maestro-onboarding."

Se "Pausa" → encerrar skill silenciosamente.

### 2.7 Obsidian

Marcar task "Configurar Obsidian" como `in_progress`.

Explicar:

> "Todos os arquivos que o Maestro cria são Markdown puro. Você pode editar direto no terminal, mas existe uma forma mais visual: o **Obsidian**.
>
> O Obsidian é um editor gratuito que transforma essa pasta em algo parecido com o Notion. Você navega pelos arquivos, edita com formatação visual, e tudo fica conectado por links. É a forma mais confortável de preencher templates e revisar entregas."

Usar `AskUserQuestion` (conforme [[protocolo-interacao]]):
- question: "Quer configurar o Obsidian como editor visual?"
- options:
  - label: "Guiar instalação (Recomendado)", description: "Te guio passo a passo na instalação e configuração do vault"
  - label: "Já tenho instalado", description: "Pula pra configuração do vault direto"
  - label: "Depois", description: "Tudo funciona no terminal. Configura quando quiser via /maestro:onboarding"

Ajustar o fluxo conforme a escolha:
- "Guiar instalação" → segue pra detecção + instalação (passo 2 da seção)
- "Já tenho instalado" → pula pra criação do vault (passo 3 da seção)
- "Depois" → segue pro próximo passo

**Se sim:**

1. Verificar se o Obsidian já está instalado:
   - Windows: `test -f "$LOCALAPPDATA/Obsidian/Obsidian.exe"` (caminho padrão de instalação)
   - macOS: `test -d "/Applications/Obsidian.app"`
   - Linux: `which obsidian 2>/dev/null`
   - **NÃO usar `where obsidian`** — o Obsidian não registra no PATH do Windows
   - **Se encontrado:** informar "Obsidian já está instalado!" e pular para o passo 3
   - **Se NÃO encontrado:** perguntar ao usuário antes de assumir que não tem:
     > "Não consegui detectar o Obsidian instalado no seu computador. Você pode me confirmar se de fato ainda não instalou essa ferramenta?"
     - **Se o usuário confirma que já tem:** informar "Entendido! Vamos direto pra configuração do vault." e pular para o passo 3
     - **Se o usuário confirma que não tem:** seguir para o passo 2

2. Guiar a instalação:
   > "Baixe o Obsidian em https://obsidian.md/ (é grátis). Instale normalmente e abra o app.
   >
   > Me avise quando estiver pronto."
   - Aguardar confirmação do usuário

3. Guiar a criação do vault (apontando pra Área de Trabalho, não pro projeto):

   > "Agora no Obsidian:
   > 1. Clique em **'Open folder as vault'** (ou 'Abrir pasta como vault')
   > 2. Selecione a pasta da sua **Área de Trabalho**: `<CWD>/<workspace_slug>/`
   > 3. Pronto! Você vai ver o projeto `<projeto_legivel>` dentro, e qualquer projeto novo que adicionar depois aparece automaticamente no mesmo vault.
   >
   > A Área de Trabalho é o fichário; cada projeto é uma aba dentro. O Obsidian vai criar uma config própria nessa pasta — é normal."

4. Sugerir configurações opcionais:
   > "Dica: nas configurações do Obsidian (engrenagem no canto inferior esquerdo), ative **'Files & Links' → 'Detect all file extensions'** pra ver todos os arquivos do projeto."

5. Instalar o plugin **Dataview** (obrigatório):
   > "Agora um plugin que é **obrigatório** pro Maestro funcionar bem: o **Dataview**. Ele é quem transforma os painéis de tarefas, planos e entrevistas em tabelas automáticas, sempre atualizadas conforme você trabalha. Sem o Dataview, esses painéis aparecem só como blocos de código — não vão renderizar.
   >
   > Siga:
   > 1. No Obsidian, abra **Settings** (engrenagem, canto inferior esquerdo)
   > 2. Vá em **Community plugins**
   > 3. Se pedir pra habilitar community plugins, clique em **Turn on community plugins**
   > 4. Clique em **Browse** e busque **Dataview**
   > 5. Clique em **Install** e depois em **Enable**
   >
   > Me avise quando estiver pronto."
   - Aguardar confirmação do usuário

6. Dica final — navegação por tags. **Mostrar ao usuário (obrigatório, não pular):**
   > "Última dica: depois de criar alguns artefatos, abra o **painel de Tags** do Obsidian (ícone de `#` no sidebar direito). Seus produtos e temas aparecem como árvore navegável — clicar em qualquer tag filtra o vault. É o jeito mais rápido de ver 'todos os copies do Produto X' ou 'todas as peças de vendas'. As tags vêm do campo `tags-dominio` no topo de cada arquivo da Biblioteca (frontmatter) — quanto mais você preenche os templates, mais tags aparecem aqui."

   > "**Dica bônus:** quando quiser ver o mapa visual de **{nome-alvo}**, abre o **Graph View** no Obsidian (ícone de rede no sidebar — `Ctrl+G` no Windows/Linux ou `Cmd+G` no Mac). Vai aparecer toda a teia de conexões entre produtos, públicos, peças."

**Se não/depois:**
- Informar: "Sem problema! Tudo funciona no terminal mesmo. Se quiser configurar depois, rode `/maestro:onboarding` e escolha a opção do Obsidian. Lembre-se: sem o Dataview instalado, os painéis de tarefas/planos/entrevistas ficam ilegíveis."

Marcar task "Configurar Obsidian" como `completed`.

**Emitir `AskUserQuestion` de continuidade (B-S55-8):**

- question: "Podemos continuar?"
- options:
  - label: "Sim, vamos seguir", description: "Continua pra próxima etapa do onboarding."
  - label: "Pausa", description: "Encerra aqui — você retoma depois com /maestro-onboarding."

Se "Pausa" → encerrar skill silenciosamente.

### 2.8 Pesquisador

Marcar task "Configurar Pesquisador" como `in_progress`.

Explicar:

> "O Maestro tem um agente de pesquisa que busca dados na web: concorrência, mercado, tendências, referências. Pra marketing, ter fontes confiáveis faz toda a diferença na qualidade das entregas.
>
> O pesquisador tem dois modos:
>
> **Uso básico (grátis):** usa o WebSearch do Claude Code. Já funciona sem configuração.
>
> **Uso avançado (pago):** usa a Perplexity, uma ferramenta focada em busca com fontes confiáveis. A conexão é feita pelo OpenRouter, um serviço que dá acesso a vários modelos de IA por uma única API. O custo é por uso (centavos por pesquisa)."

Usar `AskUserQuestion` (conforme [[protocolo-interacao]]):
- question: "Qual modo de pesquisa quer usar?"
- options:
  - label: "Básico (Recomendado)", description: "Usa WebSearch do Claude Code. Grátis, já funciona sem configuração"
  - label: "Avançado", description: "Usa Perplexity via OpenRouter. Pago (~centavos por pesquisa), resultados mais precisos com fontes"
  - label: "Depois", description: "Começa com o básico. Configura o avançado quando quiser"

**Se quer configurar agora:**
- Perguntar: "Você já tem uma API key do OpenRouter?"
  - **Se sim:** pedir a key e salvar em `~/.maestro/config.md` no campo `openrouter-api-key`
  - **Se não:** apresentar guia:

> "Sem problema! Aqui está o passo a passo:
>
> 1. Acesse openrouter.ai e crie uma conta (login com Google funciona)
> 2. Vá em openrouter.ai/settings/keys
> 3. Clique em 'Create Key', dê um nome (ex: 'maestro') e copie a chave gerada
> 4. Adicione créditos em openrouter.ai/settings/credits (mínimo $5 é suficiente pra começar)
> 5. Cole a chave aqui quando estiver pronto
>
> Para um tutorial completo com prints e vídeo, acesse a Comunidade Automators: https://automators.com.br"

  - Aguardar resposta do usuário:
    - Se colou a key: salvar em `~/.maestro/config.md` e seguir pro teste (2.8.1)
    - Se quer pular: seguir com modo básico, setar `ferramenta-default: websearch`
- Se a key foi informada, perguntar: "Quer que eu faça um teste rápido pra validar se a chave funciona? É uma chamada simples (custo ~$0.01)."
  - **Se sim:** executar teste conforme seção 2.8.1
  - **Se não:** pular o teste
- Usar `AskUserQuestion` (conforme [[protocolo-interacao]]):
  - question: "Qual ferramenta usar como padrão?"
  - options:
    - label: "Sonar (Recomendado)", description: "Rápido e econômico. Bom pra maioria das pesquisas"
    - label: "Deep Research", description: "Mais profundo e lento. Melhor pra análises complexas de mercado"
- Salvar a escolha no campo `ferramenta-default`

**Se prefere o básico:**
- Informar: "Perfeito! O WebSearch já funciona bem. Se quiser configurar o avançado depois, rode `/maestro:onboarding`."

Marcar task "Configurar Pesquisador" como `completed`.

**Emitir `AskUserQuestion` de continuidade (B-S55-8):**

- question: "Podemos continuar?"
- options:
  - label: "Sim, vamos seguir", description: "Continua pra próxima etapa do onboarding."
  - label: "Pausa", description: "Encerra aqui — você retoma depois com /maestro-onboarding."

Se "Pausa" → encerrar skill silenciosamente.

### 2.8.1 Teste da API Key do OpenRouter

Executar uma pesquisa real simples via `curl` ao endpoint do OpenRouter com o modelo mais barato (`perplexity/sonar`):

```bash
curl -s -w "\n%{http_code}" https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {API_KEY}" \
  -d '{"model":"perplexity/sonar","messages":[{"role":"user","content":"Qual é a capital do Brasil? Responda em uma frase."}],"max_tokens":30}'
```

**Interpretar o resultado:**

- **HTTP 200 + resposta válida:** informar "Chave validada! Conexão com o OpenRouter funcionando." Marcar a task como `completed` e seguir. **Não despachar Pesquisador aqui** — o `curl` já validou a conexão; salvar artefato de teste no vault polui `pesquisas/` sem valor.
- **HTTP 401 ou 403:** informar "A chave não foi aceita pelo OpenRouter. Verifique se está correta e tente novamente com `/maestro:onboarding`."
- **HTTP 402 ou erro de crédito:** informar "A chave é válida, mas sua conta no OpenRouter não tem créditos. Adicione saldo em openrouter.ai e a pesquisa paga vai funcionar."
- **Outro erro (timeout, rede):** informar "Não consegui conectar ao OpenRouter agora. A chave foi salva. Você pode testar depois pedindo: 'testa minha conexão com o OpenRouter'."

Se a chave falhou (401/403), **remover** o valor salvo em `~/.maestro/config.md` e setar `ferramenta-default: websearch`.

### 2.9 Pesquisa inicial do negócio (Turno 13)

Marcar task "Pesquisa inicial do negócio" como `in_progress`. Marcar TodoWrite T13 `in_progress`.

**Só executar se a biblioteca foi criada no passo 2.6.** Se o usuário pulou a biblioteca, pular esta etapa também (e marcar TodoWrite T13 `completed` sem dispatch).

**Turno T13.** Renderizar literal o bloco `---TEXTO-T13---` de `turnos-onboarding.md` (substituir `{nome-alvo}` por `<projeto_legivel>`). Aguardar resposta livre do usuário (site ou pular).

**Persistir marker da Camada 3 ANTES de despachar Pesquisador:**

```bash
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-auq-pesquisa"
```

**Se informou o site:**

Tratar este passo como uma **Entrega padrão**, exatamente como o hub do Maestro trataria se o usuário tivesse pedido a pesquisa fora do onboarding. Executar o fluxo `plugin/skills/maestro/fluxo-entrega.md` (5 itens, pipeline completo) para o pedido:

> "Pesquisa inicial sobre {nome da empresa}: site {url} e redes sociais. Mapear posicionamento atual, produtos/serviços, público-alvo aparente, tom de voz observado e presença em redes."

Parâmetros do dispatch:
- **Especialista:** Pesquisador
- **Categoria:** `pesquisa`
- **Tipo:** `pesquisa`
- **tags-dominio:** `pesquisa/empresa`
- **Ferramenta:** `ferramenta-default` do `~/.maestro/config.md` (definido no step 2.8)

O fluxo cobre todo o pipeline obrigatório: Gerente cria tarefa → Pesquisador executa via `Agent()` → ciclo QA + Revisor → Gerente conclui tarefa. **Não invocar `Skill("/maestro:pesquisador")` direto aqui** — quebra rastreabilidade (`origem-tarefa:` ausente) e pula validação. Bug B-S55-20 da v2.20.0 aconteceu por causa disso.

**Se não tem site ou prefere pular:**
- Informar literal: "Sem problema! Quando quiser, peça: 'pesquisa sobre minha empresa'."

Marcar task "Pesquisa inicial do negócio" como `completed` somente após o ciclo de validação retornar aprovado (ou após o usuário confirmar que pulou). Marcar TodoWrite T13 `completed`.

### 2.10 Importar Material de Referência (Turno 14)

**Se `SKIP_T14=true` (cenário pós-import via /importar-projeto):** pular esta seção inteira. Render literal "A importação já trouxe seu material — vamos pro próximo passo." e marcar TodoWrite T14 como `completed`. Seguir pro próximo turno.

Caso contrário, manter fluxo atual.

Marcar task "Importar material de referência" como `in_progress`. Marcar TodoWrite T14 `in_progress`.

**Só executar se a biblioteca foi criada no passo 2.6.** Se o usuário pulou a biblioteca, pular esta etapa também (e marcar TodoWrite T14 `completed`).

**Turno T14.** Renderizar literal o bloco `---TEXTO-T14---` de `turnos-onboarding.md` (substituir `{nome-alvo}` e `{empresa}` pelos valores corretos).

**Persistir marker da Camada 3 após resposta:**

```bash
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-auq-material"
```

**Se sim:**
- Aguardar o usuário colocar os arquivos e confirmar
- Seguir o fluxo de importação do Maestro Biblioteca (seção 9 da sub-skill `maestro/biblioteca`)
- O fluxo inclui: listar arquivos, verificar formatos, catalogar, perguntar modo (tudo ou um por um), preencher via especialistas
- Se houve pesquisa inicial (passo 2.9), usar os achados como contexto complementar no preenchimento

**Se não/depois:**
- Informar literal: "Sem problema! Quando tiver material, coloca na pasta `referencias/` e pede: 'lê meus arquivos de referência'."

Marcar task "Importar material de referência" como `completed`. Marcar TodoWrite T14 `completed`.

**Emitir `AskUserQuestion` de continuidade (B-S55-8):**

- question: "Podemos continuar?"
- options:
  - label: "Sim, vamos seguir", description: "Continua pra próxima etapa do onboarding."
  - label: "Pausa", description: "Encerra aqui — você retoma depois com /maestro-onboarding."

Se "Pausa" → encerrar skill silenciosamente.

### 2.11 Status Line

**Se o checklist pré-onboarding (item 6) detectou que `statusLine` já está configurada em `~/.claude/settings.json`:** pular esta etapa silenciosamente. Não perguntar nada. Marcar task como `completed` e seguir.

**Se não está configurada:**

Marcar task "Configurar Status Line" como `in_progress`.

Usar `AskUserQuestion` (conforme [[protocolo-interacao]]):
- question: "Quer ativar uma barra de status no terminal?"
- options:
  - label: "Ativar (Recomendado)", description: "Mostra em tempo real contexto, limites da API e modelo. Desliga quando quiser"
  - label: "Não ativar", description: "Pula por agora. Ativa depois com /maestro-statusline"

**Se sim:**
1. Ler o template do script em `core/statusline/maestro-statusline.sh`
2. Copiar para `~/.claude/maestro-statusline.sh` com os valores default das variáveis de configuração
3. Tornar executável: `chmod +x ~/.claude/maestro-statusline.sh`
4. Ler `~/.claude/settings.json` e adicionar a chave `statusLine`:
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "~/.claude/maestro-statusline.sh"
     }
   }
   ```
5. Verificar workspace trust (mesmo fluxo da seção 2.3 da skill `[[maestro-statusline]]`):
   - Ler `~/.claude.json` em modo binário
   - Buscar o CWD atual e verificar `hasTrustDialogAccepted`
   - Se `false`: explicar e pedir confirmação:
     > "Pra barra de status funcionar, preciso ativar o **workspace trust** neste projeto.
     >
     > O workspace trust é uma trava de segurança do Claude Code. Quando você abre um projeto, o Claude pergunta se confia nele. Enquanto não aceitar, ele bloqueia execução automática de código, como a barra de status, hooks e plugins.
     >
     > Esse projeto está com o trust desativado."

     Após o texto explicativo, emitir `AskUserQuestion` (B-S55-8):
     - question: "Posso ativar o workspace trust deste projeto?"
     - options:
       - label: "Sim, pode ativar", description: "Vou ajustar `~/.claude.json` (replace binário)."
       - label: "Não", description: "A barra de status não vai funcionar sem trust."
   - Se o usuário aceitar: corrigir com replace binário (`false` → `true`). **Nunca usar json.load/json.dump** porque o arquivo tem surrogates Unicode que corrompem na serialização. Informar que a barra aparece após reiniciar.
   - Se o usuário recusar: informar que a barra não vai funcionar sem trust e seguir adiante.
6. Atualizar `~/.maestro/config.md`: setar `statusline-ativo: true` na seção `## Status Line`
7. Informar: "Barra de status ativada! Ela mostra contexto, limites e modelo. Pra configurar ou desligar: `/maestro-statusline`."

**Se não:**
- Informar: "Sem problema! Quando quiser ativar, rode `/maestro-statusline`."

Marcar task "Configurar Status Line" como `completed`.

### 2.12 Finalização (Turno 15)

Marcar task "Finalizar onboarding" como `in_progress`. Marcar TodoWrite T15 `in_progress`.

> [!critical] Pre-output verification OBRIGATÓRIO
> ANTES de prosseguir, verificar via Bash que o state file ativo existe em `$STATE_DIR`. Se ausente, as Camadas 3+4 nunca foram ativadas (state nunca foi criado em T3) — ABORTAR o T15 e re-rodar o Bash de init do T3 antes de seguir. Aprendizado #58: Opus pode declarar "tudo OK" mesmo com audit trail vazio.
>
> ```bash
> if ! ls "$STATE_DIR"/state-*.md >/dev/null 2>&1; then
>     echo "[ABORTAR] state file ausente. Camadas 3+4 nunca ativaram. Re-rodar Bash de init em T3 antes de finalizar." >&2
>     exit 1
> fi
> ```

1. Atualizar `maestro/config.md`: setar `onboarding-completo: true` (somente após verificação acima passar).

   > [!critical] Use Bash sed — NÃO use tool Edit com `$PROJETO_PATH` literal
   > Variáveis Bash (`$PROJETO_PATH`, `$WORKSPACE_PATH`, `$CWD`) só expandem dentro do tool Bash. Tool Edit/Write trata `$PROJETO_PATH` como string literal e o sed falha com "No such file or directory" (B-OnbUX-2A-3). Use:
   >
   > ```bash
   > sed -i 's/^onboarding-completo:.*/onboarding-completo: true/' "$PROJETO_PATH/maestro/config.md"
   > ```
   >
   > Se precisar usar Edit por algum motivo, expanda primeiro o path em Bash (`echo "$PROJETO_PATH/maestro/config.md"`) e use o caminho absoluto resultante na chamada Edit.

2. **Detectar fase de implementação (F1-D4):**

   ```bash
   if [ -f "$WORKSPACE_PATH/.obsidian/bookmarks.json" ]; then
       FASE="completa"   # F4 já mergeada — bookmarks foram criados pelo Bibliotecário
   else
       FASE="reduzida"   # F1/F2/F3 ainda em construção — sem painel agregado nem bookmarks
   fi
   ```

3. **Renderizar mensagem de encerramento conforme `FASE`:**

   - Se `FASE=completa` → renderizar literal o bloco `---TEXTO-T15-CASO-A---` de `turnos-onboarding.md`, substituindo `<workspace-path-absoluto-normalizado>`, `<workspace-path>` e `{nome-alvo}` pelos valores reais.
   - Se `FASE=reduzida` → renderizar literal o bloco `---TEXTO-T15-CASO-B---` de `turnos-onboarding.md`, substituindo `<workspace_legivel>`, `<CWD>/<workspace_slug>/` e `<projeto_legivel>`.

   **Path normalizado pro SO nativo:** detectar SO antes de mostrar (backslash em Windows, forward em Mac/Linux).

4. **Finalização enfática — preencher identidade.**

Independente do CASO A ou B acima, **toda finalização do Fluxo de Primeira Vez** termina com a renderização de `---TEXTO-T15-IDENTIDADE---` de `turnos-onboarding.md` (substituindo `{nome-alvo}`) seguida da AUQ correspondente. Não pular.

`AskUserQuestion`:
- question: "Como prefere preencher a identidade de {nome-alvo}?"
- options:
  - label: "Guia no chat", description: "Eu te conduzo uma pergunta de cada vez."
  - label: "Vou preencher no Obsidian", description: "Você abre os arquivos e preenche nas Properties."
  - label: "Agora não", description: "Termino o onboarding aqui — pode preencher depois."

**Persistir markers da Camada 3 após resposta:**

```bash
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-auq-identidade"
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-conclusao"
python "$HELPERS/onboarding_state.py" archive "$STATE_DIR" "$SLUG"
```

**Resoluções:**

- **"Guia no chat"** → invocar fluxo do Entrevistador via despacho padrão (Gerente cria tarefa primeiro, depois Entrevistador conduz coleta de identidade pergunta-a-pergunta).

- **"Vou preencher no Obsidian"** → renderizar literal o bloco `---TEXTO-T15-OBSIDIAN---` de `turnos-onboarding.md` (substituindo `<workspace>`, `<projeto_slug>` e `{nome-alvo}`).

- **"Agora não"** → renderizar literal o bloco `---TEXTO-T15-DEPOIS---` de `turnos-onboarding.md` (substituindo `{nome-alvo}`).

Marcar task "Finalizar onboarding" como `completed`. Marcar TodoWrite T15 `completed`.

### 2.12.1 Concluir tarefa no vault

Acionar Gerente de Projetos via Agent(haiku):

- Bloco TAREFA: "Concluir tarefa: Onboarding do projeto {nome da empresa}"
- Bloco CONTEXTO:
  - Caminho da tarefa: [caminho guardado em 2.0.2 ou 2.5.1]
  - Resultado: "Onboarding completo. Biblioteca criada, pesquisador configurado, vault ativo."

---

## 2B. Fluxo de Novo Projeto

**Parsing de modo (se vier no CONTEXTO):**

- Procurar linha `modo: <valor>` no bloco CONTEXTO.
- Se `modo == pos-import-skip-T14`: setar variável `SKIP_T14=true` (no escopo da skill). Os demais turnos rodam normais.
- Outros valores ou ausente: rodar fluxo padrão (`SKIP_T14=false`).

Onboarding leve para quando o usuário já tem o Sistema Maestro configurado (`~/.maestro/` existe) mas está num projeto novo. Pula dependências, permissões, Obsidian, status line e apresentação.

#### Camadas de defesa do Fluxo de Novo Projeto (F-Onb-2A)

> [!danger] OBRIGATÓRIO — pular qualquer Camada = bug crítico
> Mesmas regras do Fluxo de Primeira Vez. As Camadas 3 e 4 (state file + markers + hook auditor) têm efeito INVISÍVEL pro user, mas ativam a proteção contra B-F1-10 (slug duplicado entre projetos da mesma sessão) e bloqueiam dispatch precoce do Bibliotecário. **NÃO PULAR pra "encurtar"** — Opus 4.7 tende a tratar audit trail como opcional (aprendizados #38/#57/#58). Esta seção bloqueia.

**Camada 1 — TodoWrite obrigatório.** TodoWrite é aberto **dentro de 2B.-1** baseado no caso detectado:

- **Casos 1-3** (workspace já existe ou é projeto): 5 itens (T1B, T9B, T10B, T11B, T12B).
- **Caso 4** (pasta vazia + sistema globalmente configurado): 6 itens com T0 incluído ANTES de T1B.

```python
# Versão Casos 1-3
TodoWrite([
    {"content": "T1B — Boas-vindas + nome novo projeto (texto + AUQ)", "status": "pending", "activeForm": "Apresentando e coletando nome"},
    {"content": "T9B — AUQ Biblioteca", "status": "pending", "activeForm": "Aguardando decisão Biblioteca"},
    {"content": "T10B — AUQ Pesquisa inicial", "status": "pending", "activeForm": "Aguardando decisão Pesquisa"},
    {"content": "T11B — AUQ Material referência", "status": "pending", "activeForm": "Aguardando decisão Material"},
    {"content": "T12B — Finalização (dica colisão + Bookmarks)", "status": "pending", "activeForm": "Finalizando"},
])

# Versão Caso 4 (com T0)
TodoWrite([
    {"content": "T0 — AUQ confirmar pasta como Área de Trabalho", "status": "pending", "activeForm": "Aguardando confirmação de pasta"},
    {"content": "T1B — Boas-vindas + nome novo projeto (texto + AUQ)", "status": "pending", "activeForm": "Apresentando e coletando nome"},
    {"content": "T9B — AUQ Biblioteca", "status": "pending", "activeForm": "Aguardando decisão Biblioteca"},
    {"content": "T10B — AUQ Pesquisa inicial", "status": "pending", "activeForm": "Aguardando decisão Pesquisa"},
    {"content": "T11B — AUQ Material referência", "status": "pending", "activeForm": "Aguardando decisão Material"},
    {"content": "T12B — Finalização (dica colisão + Bookmarks)", "status": "pending", "activeForm": "Finalizando"},
])
```

**Camada 2 — Tabela determinística.** Antes de renderizar cada turno textual, ler `plugin/skills/maestro-onboarding/turnos-onboarding.md` via `Read` e renderizar o bloco `---TEXTO-TnB---` literalmente. NÃO inlinear texto entre aspas neste SKILL.md.

**Camada 3 — Markers de turno.** Após cada AUQ crítica, escrever marker via Bash:

```bash
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "<marker>"
```

onde `$STATE_DIR=$CWD/memorias/onboarding` (CWD aqui já é a workspace existente — Fluxo Novo Projeto roda com CWD=workspace) e `$SLUG=<workspace>-<projeto>` derivado direto do nome do novo projeto + workspace conhecido. Init do state acontece logo após T1B capturar o `projeto_legivel`.

**Camada 4 — Hook auditor.** Hook `onboarding-orquestra.py` valida marker antes de dispatch Bibliotecário CRIAR / Pesquisador / SCAFFOLD WORKSPACE. Se hook bloquear, Maestro lê `plugin/skills/maestro/limites-maestro.md` e re-emite a AUQ correspondente.

### 2B.-1 Branch de detecção (executar ANTES das tasks visuais)

Decidir qual sub-fluxo seguir baseado nos sinais 1-3 da Seção 1:

**Caso `marker + ≥1 projeto`:** seguir 2B.0 → 2B.6 normalmente.

**Caso `marker + 0 projetos` (recuperação):**

`AskUserQuestion`:
- question: "Detectei que esta Área de Trabalho foi criada (`<CWD>/.maestro-workspace` existe) mas nenhum projeto terminou de configurar. O que fazer?"
- options:
  - label: "Continuar configuração", description: "Retomo de onde parou — vou pedir o nome do primeiro projeto e completar"
  - label: "Cancelar e recomeçar", description: "Apago o marker e começo do zero pelo Fluxo de Primeira Vez"
  - label: "Voltar", description: "Não fazer nada agora"

Se "Continuar configuração":
- Executar Fluxo de Primeira Vez (Seção 2) **a partir da etapa 2.2**, mas com `workspace_slug` derivado do basename do CWD (ou perguntar via AUQ se ambíguo). Pular criação de marker e `mkdir` da workspace na 2.5 (já existe).

Se "Cancelar e recomeçar":
```bash
rm -f "$CWD/.maestro-workspace"
```
Executar Fluxo de Primeira Vez do zero a partir da etapa 2.0.

Se "Voltar": encerrar sem ação.

**Caso `CWD = projeto sem marker` (CWD dentro do projeto, sem Área de Trabalho):**

`AskUserQuestion`:
- question: "Você está dentro do projeto Maestro `<basename(CWD)>`. O que quer fazer?"
- options:
  - label: "Criar projeto novo na mesma Área de Trabalho", description: "Subo um nível, crio marker se faltar, adiciono novo projeto irmão"
  - label: "Reconfigurar este projeto", description: "Vai pra Fluxo de Re-execução (Seção 3)"
  - label: "Voltar", description: "Não fazer nada agora"

Se "Criar projeto novo na mesma Área de Trabalho":
- `WORKSPACE_PARENT=$(dirname "$CWD")`
- Se `<WORKSPACE_PARENT>/.maestro-workspace` ausente → criar (mesmo conteúdo do template).
- Tratar `WORKSPACE_PARENT` como `<workspace>` e seguir 2B.0 → 2B.6 normalmente (adapta `$CWD` → `WORKSPACE_PARENT` nos passos seguintes).

Se "Reconfigurar este projeto" → Seção 3.
Se "Voltar" → encerrar.

**Caso 4 — Pasta vazia + Maestro globalmente configurado** (nenhum dos 3 sinais detectados, `~/.maestro/config.md` existe):

> Princípio "perguntar antes de criar" (F-Onb-2A). User retornante numa pasta vazia merece tratamento curto: confirma se a pasta atual vai ser a Área de Trabalho, sem repetir apresentação humana ou roadmap.

**Turno T0.** Abrir TodoWrite (versão Caso 4 com 6 itens conforme Camada 1 acima). Marcar TodoWrite T0 `in_progress`.

Resolver `<NOME>` lendo `~/.maestro/memorias/nome-usuario.md` se existir. Renderizar literal o bloco `---TEXTO-T0---` de `turnos-onboarding.md` (substituindo `<NOME>` se disponível e `<CWD>`).

`AskUserQuestion`:
- question: "Vou usar esta pasta como Área de Trabalho?"
- options:
  - label: "Sim, usar esta pasta", description: "Crio o marker `.maestro-workspace` aqui e sigo o setup do primeiro projeto."
  - label: "Não, quero outra pasta", description: "Encerro o onboarding aqui — abre o Claude Code na pasta certa e me chama de novo."
  - label: "Cancelar", description: "Não fazer nada agora."

**Pós-resposta:**

- **"Sim, usar esta pasta"** → renderizar literal `---TEXTO-T0-SIM---`. **[CRITICAL]** Inicializar state e markers + criar marker da workspace:

  > [!critical] Bash OBRIGATÓRIO — não pular sob hipótese alguma
  > Mesmas regras do T3 do Fluxo de Primeira Vez. Sem este Bash, Camadas 3+4 ficam inertes e B-F1-10 fica sem defesa. Se Bash falhar, ABORTAR.

  ```bash
  HELPERS="$PLUGIN_DIR/core/helpers"
  STATE_DIR="$CWD/memorias/onboarding"
  SLUG_TMP="_tmp_$(date +%s)"
  mkdir -p "$STATE_DIR"
  python "$HELPERS/onboarding_state.py" init "$STATE_DIR" "$SLUG_TMP" "novo-projeto"
  python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG_TMP" "t-consentimento"
  python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG_TMP" "t-confirmacao-pasta"

  # [CRITICAL] verificação inline: state file precisa existir após init
  if ! ls "$STATE_DIR"/state-${SLUG_TMP}.md >/dev/null 2>&1; then
      echo "[ERRO CRÍTICO] state file não foi criado em $STATE_DIR. ABORTAR onboarding." >&2
      exit 1
  fi

  # Criar marker .maestro-workspace
  cat > "$CWD/.maestro-workspace" <<'EOF'
  # Marker do Sistema Maestro — Área de Trabalho.
  # Não apague este arquivo: ele é o que faz o Maestro reconhecer esta pasta como Área de Trabalho.
  EOF
  ```

  Marcar TodoWrite T0 `completed` e prosseguir pra 2B.0 (Tasks visuais) → 2B.1 (T1B nome do novo projeto).

- **"Não, quero outra pasta"** → renderizar literal `---TEXTO-T0-NAO---` e encerrar skill. Não inicializar state. Não criar marker.

- **"Cancelar"** → renderizar literal `---TEXTO-T0-CANCEL---` e encerrar skill (mesmo tratamento de "Não").

### 2B.0 Tasks visuais

Criar tasks visuais no terminal:

```
TaskCreate({ subject: "Configurar novo projeto", description: "Nome da empresa e pasta raiz", activeForm: "Configurando novo projeto" })
TaskCreate({ subject: "Setup do projeto", description: "Criar config, memórias e CLAUDE.md", activeForm: "Criando estrutura do projeto" })
TaskCreate({ subject: "Criar Biblioteca de Marketing", description: "Scaffold da biblioteca no vault", activeForm: "Criando Biblioteca de Marketing" })
TaskCreate({ subject: "Pesquisa inicial do negócio", description: "Analisar site e redes sociais", activeForm: "Pesquisando sobre o negócio" })
TaskCreate({ subject: "Importar material de referência", description: "Importar documentos existentes do negócio", activeForm: "Importando material de referência" })
TaskCreate({ subject: "Finalizar projeto", description: "Encerrar com sugestão de primeira ação", activeForm: "Finalizando configuração" })
```

Marcar cada task como `in_progress` ANTES de executar a etapa e `completed` LOGO APÓS terminar.

Usar os mesmos marcadores visuais da seção 2.0.3 (separador com número do passo).

### 2B.0.1 Criar tarefa no vault

Se o projeto já tem pasta `tarefas/`:

Acionar Gerente de Projetos via Agent(haiku):

- Bloco TAREFA: "Criar tarefa para: Onboarding do projeto {nome da empresa}"
- Bloco CONTEXTO:
  - Agente: maestro
  - Categoria: geral
  - Solicitante: [nome do usuário]
  - Grupo: onboarding
  - Prioridade: alta
  - Checklist personalizado:
    - [ ] Configurar novo projeto
    - [ ] Setup do projeto
    - [ ] Criar Biblioteca de Marketing
    - [ ] Pesquisa inicial do negócio
    - [ ] Importar material de referência

Se a pasta `tarefas/` ainda não existe, adiar pro step 2B.2.1 (após setup).

Guardar o caminho do arquivo de tarefa para usar na conclusão.

### 2B.1 Boas-vindas e nome do novo projeto (Turno T1B)

Marcar task "Configurar novo projeto" como `in_progress`. Marcar TodoWrite T1B `in_progress`.

Ler `~/.maestro/memorias/nome-usuario.md` para recuperar o nome do usuário (`<NOME>`).

**1. Resolver `workspace_legivel`:**

- Se cache local (`<workspace>/.maestro/cache/projeto-ativo.md`, onde `<workspace>` é o CWD atual no Fluxo Novo Projeto) existe e tem campo `workspace:`, ler de lá.
- Senão, inferir do basename do CWD: `WORKSPACE_LEGIVEL=$(basename "$CWD")` (capitalizado pra exibição: substituir hifens por espaço e capitalizar).

**1.ter Verificar contexto de inacabados (pós-import):**

Procurar no bloco CONTEXTO do dispatch por campo `contexto-import`.

Se `contexto-import == "incluiu-inacabados"`, renderizar ANTES da apresentação do T1B:

> Antes da gente começar: vi que sua identidade veio com arquivos inacabados do projeto-origem. Eles ficaram com o status original (⚙️ em andamento, ⏳ pendente ou 🔍 em revisão). Quando quiser terminá-los, abre o painel `_identidade.md` aqui no Obsidian e clica nos que estão com ícone diferente de ✅.

Se `contexto-import` é qualquer outro valor (`nenhum-inacabado`, `pulou-inacabados`, ausente) → continuar normalmente sem renderizar o aviso.

**1.bis Detectar contexto (Caso 4 vs Casos 1-3):**

```bash
STATE_DIR="$CWD/memorias/onboarding"
TMP_STATE=$(ls "$STATE_DIR"/state-_tmp_*.md 2>/dev/null | head -1)
if [ -n "$TMP_STATE" ]; then
    CONTEXTO_T1B="caso-4"   # T0 já criou state e workspace marker
else
    CONTEXTO_T1B="caso-1-3"  # workspace pré-existente
fi
```

**2. Apresentar:**

- Se `CONTEXTO_T1B=caso-1-3`: renderizar literal o bloco `---TEXTO-T1B---` de `turnos-onboarding.md` (substituindo `<NOME>` e `<workspace_legivel>` pelos valores resolvidos). **Proibido parafrasear** — texto exato com vocativo do user e nome literal da Área de Trabalho entre aspas simples (B-OnbUX-2A-4). Aprendizado #52: Opus tende a substituir por "Beleza!" — resista.
- Se `CONTEXTO_T1B=caso-4`: **pular** renderização do `---TEXTO-T1B---` (T0-SIM já cobriu o contexto "vou montar Área de Trabalho aqui e já criar o primeiro projeto"). Ir direto pro AUQ do passo 3.

**3. Coletar nome do novo projeto via `AskUserQuestion`:**

- question: "Qual o nome do novo projeto?"
- placeholder/exemplo: "uma empresa, cliente ou marca que você vai trabalhar"

Aguardar resposta. Guardar como `projeto_legivel`. Computar `projeto_slug_proposto = slugify(projeto_legivel)`.

**3.bis Persistir state file final (Camada 3):**

```bash
HELPERS="$PLUGIN_DIR/core/helpers"
STATE_DIR="$CWD/memorias/onboarding"
mkdir -p "$STATE_DIR"
SLUG=$(python "$HELPERS/onboarding_state.py" slug "$WORKSPACE_LEGIVEL" "$PROJETO_LEGIVEL")

if [ "$CONTEXTO_T1B" = "caso-4" ]; then
    # Renomear state file _tmp_* para slug definitivo (T0 já criou)
    mv "$TMP_STATE" "$STATE_DIR/state-$SLUG.md"
else
    # Casos 1-3: criar state file novo
    python "$HELPERS/onboarding_state.py" init "$STATE_DIR" "$SLUG" "novo-projeto"
fi

python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-nome-workspace"
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-nome-projeto"
```

**4. Validar contra duplicatas:**

```bash
EXISTING_PROJETOS=$(find "$CWD" -mindepth 3 -maxdepth 3 -path "*/maestro/config.md" -exec dirname {} \; | xargs -I {} dirname {} | xargs -I {} basename {})
```

Se `projeto_slug_proposto` ∈ `EXISTING_PROJETOS`:

`AskUserQuestion`:
- question: "Já existe projeto chamado `<projeto_slug_proposto>` dentro de `<workspace_legivel>`. Outro nome ou cancelar?"
- options:
  - label: "Outro nome", description: "Volta pra etapa 3"
  - label: "Cancelar", description: "Aborta o Fluxo de Novo Projeto"

Se "Outro nome" → repetir etapa 3.
Se "Cancelar" → encerrar.

**5. Preview de slug:**

`AskUserQuestion`:
- question: "Vou criar pasta `<projeto_slug_proposto>` dentro da Área de Trabalho. Tudo bem ou quer mudar?"
- options:
  - label: "Tudo bem", description: "Cria com esse slug"
  - label: "Mudar", description: "Digito o slug direto"

Se "Mudar" → pedir slug direto, validar regex `^[a-z0-9-]+$`, max 80 chars.
Se "Tudo bem" → fixar `projeto_slug = projeto_slug_proposto`.

Aplicar mesma validação R9 do Fluxo de Primeira Vez (slug vazio/só hífens → re-pedir).

Marcar task "Configurar novo projeto" como `completed`. Marcar TodoWrite T1B `completed`.

**Emitir `AskUserQuestion` de continuidade (B-S55-8):**

- question: "Podemos continuar?"
- options:
  - label: "Sim, vamos seguir", description: "Continua pra próxima etapa do onboarding."
  - label: "Pausa", description: "Encerra aqui — você retoma depois com /maestro-onboarding."

Se "Pausa" → encerrar skill silenciosamente.

### 2B.2 Setup do projeto

Marcar task "Setup do projeto" como `in_progress`.

Executar silenciosamente:

1. **Criar pasta do projeto dentro da Área de Trabalho:**

   ```bash
   PROJETO_PATH="$CWD/<projeto_slug>"
   WORKSPACE_PATH="$CWD"
   mkdir -p "$PROJETO_PATH"
   ```

2. **Config do projeto:** criar `$PROJETO_PATH/maestro/config.md` usando `core/templates/_maestro-config-template.md`:
   - Preencher `Empresa:` com `<projeto_legivel>`
   - Preencher `Vault:` com `$PROJETO_PATH`
   - Preencher `Projeto iniciado em:` com a data atual
   - Setar `maestro-ativo: true`
   - Manter `onboarding-completo: false` (será atualizado no final)

3. **Memórias de projeto:** criar `$PROJETO_PATH/maestro/memorias/` usando templates de `core/templates/_memorias-projeto-template.md`:
   - `maestro/memorias/_index.md`
   - `maestro/memorias/contexto.md`
   - `maestro/memorias/sessoes/` (pasta vazia; `_sessoes.md` é criado pelo /tchau-maestro na primeira sessão)
   - `maestro/memorias/decisoes.md`
   - `maestro/memorias/preferencias-classificacao.md` — copia de `core/templates/_preferencias-classificacao-template.md` (v2.12.0, Bug 4). Maestro preenche ao longo do uso conforme você responde AskUserQuestion de ambiguidade. Após 3 escolhas iguais pro mesmo padrão, vira preferência aplicada automaticamente com opção de override.
   - `maestro/memorias/pendencias-aceitas/historico.md` — copia de `core/templates/_pendencias-aceitas-historico-template.md` (v2.12.0 origem, v2.23.2 reorganizado). Registra longitudinalmente usos da opção "forçar entrega com pendência" em QA/Revisor. Após 3 usos, Maestro bloqueia a opção e força revisão estrutural do checklist.
   - `maestro/memorias/agentes/` (pasta vazia)

   O arquivo `memorias/decisoes.md` começa vazio e será preenchido automaticamente conforme você toma decisões estratégicas durante o uso do Maestro (arquétipo, formato de lançamento, tom de voz, etc.). O sistema reusa escolhas anteriores pra manter coerência entre entregas.

4. **CLAUDE.md do projeto:** despachar Bibliotecário pra criar/anexar seção Maestro:

   ```python
   Agent(
     subagent_type="maestro:bibliotecario",
     prompt="""
     CONTEXTO:
     path-projeto: $PROJETO_PATH

     FLUXO: CRIAR_CLAUDE_PROJETO
     """
   )
   ```

   O Bibliotecário cria `$PROJETO_PATH/CLAUDE.md` (ou anexa seção `## Maestro` se já existir). Hook PreToolUse libera porque Bibliotecário é subagente (tem `agent_id`). Idempotente — se Bibliotecário retornar `ALREADY_EXISTS`, prosseguir silencioso.

5. **Despachar Bibliotecário REGENERATE PAINEL (stub em F1, F2/F4 preenchem):**

   ```python
   Agent(
     subagent_type="maestro:bibliotecario",
     prompt="""
     CONTEXTO:
     workspace: $WORKSPACE_PATH
     projeto-slug-novo: <projeto_slug>

     FLUXO: REGENERATE PAINEL
     """
   )
   ```

   Em F1 retorna `STATUS: DONE`. Em F2 vai regenerar FROM clauses dos painéis Dataview. Em F4 vai atualizar bookmarks.

6. **Atualização de permissões existentes (patch silencioso):**
   - Se o projeto já tem `.claude/settings.local.json`, abra o arquivo e verifique se `permissions.allow` contém `WebSearch` e `WebFetch(domain:*)`. Se faltar alguma das duas, adicione ao array. Não pergunte consentimento — o usuário já autorizou o padrão de permissões no onboarding completo anterior. Apenas informe: "Permissões atualizadas com WebSearch e WebFetch (necessárias para o Pesquisador)."
   - Se o projeto não tem `settings.local.json`, criar o arquivo completo com o bloco de permissões padrão (mesma lista do onboarding completo, seção 2.4).

7. **Atualizar cache de projeto ativo** (apontando pro projeto novo) — escrita em `<workspace>/.maestro/cache/projeto-ativo.md`:

   ```bash
   # Fix B-F1-4: cygpath converte /c/dev/... → C:/dev/... no Git Bash do Windows.
   # Fix B-OnbUX-2A-8: bash parameter expansion substitui `tr '\\' '/'`.
   if command -v cygpath >/dev/null 2>&1; then
     CWD_NORM=$(cygpath -m "$CWD")
   else
     CWD_NORM="${CWD//\\//}"
   fi
   # CWD nesta etapa é a workspace (Fluxo Novo Projeto roda com CWD=workspace)
   WORKSPACE="$CWD_NORM"
   TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
   mkdir -p "$WORKSPACE/.maestro/cache"
   cat > "$WORKSPACE/.maestro/cache/projeto-ativo.md" <<EOF
   ---
   versao: 1
   slug: <projeto_slug>
   caminho-absoluto: ${WORKSPACE}/<projeto_slug>
   workspace: ${WORKSPACE}
   atualizado-em: ${TIMESTAMP}
   ---
   EOF
   ```

   **Precedência cache local vs cache pré-existente:** o cache local da workspace é o único — não há cache global pra "vencer". Sobrescrita do cache local é silenciosa.

   **Importante (fix B-F1-7):** este Bash heredoc é obrigatório — não substituir por Write/Edit. O `$(date)` precisa rodar no shell pra timestamp ser real; se o modelo usar Edit/Write em vez de Bash, o timestamp sai inferido como `T00:00:00Z`. Validação manual confirmou em Cenários 4 e 5 da F1: paths C:/... corretos mas timestamp zerado quando o caminho passa por Edit.

Informar brevemente: "Estrutura do projeto criada na Área de Trabalho."

Marcar task "Setup do projeto" como `completed`.

### 2B.2.1 Criar tarefa no vault (se não criada em 2B.0.1)

Se a tarefa de onboarding ainda não foi criada:
- Acionar Gerente de Projetos via Agent(haiku) com o mesmo payload descrito em 2B.0.1
- Guardar caminho do arquivo de tarefa para usar na conclusão

### 2B.3 Biblioteca de Marketing (Turno T9B)

Marcar task "Criar Biblioteca de Marketing" como `in_progress`. Marcar TodoWrite T9B `in_progress`.

**Turno T9B.** Renderizar literal o bloco `---TEXTO-T9B---` de `turnos-onboarding.md` (substituindo `{nome-alvo}`).

Em seguida, emitir AUQ correspondente a T9B:
- question: "Quer criar a Biblioteca de Marketing agora?"
- options:
  - label: "Criar agora (Recomendado)", description: "Monta a estrutura com todos os templates prontos pra preencher"
  - label: "Depois", description: "Pula por enquanto. Você cria quando quiser pedindo 'cria minha biblioteca'"

**Persistir marker da Camada 3 ANTES de qualquer dispatch:**

```bash
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-auq-biblioteca"
```

**Se sim:** despachar o Bibliotecário via `Agent(subagent_type="maestro:bibliotecario", prompt="FLUXO: CRIAR\nCONTEXTO:\nnome-empresa: {nome-coletado-no-passo-2B.1}\npath-projeto: {CWD}")` para fazer scaffold dentro da pasta da empresa. Hook PreToolUse libera porque Bibliotecário é subagente; hook auditor `onboarding-orquestra.py` libera porque marker `t-auq-biblioteca` foi gravado acima.

**Se não/depois:** informar literal: "Sem problema! Quando quiser, é só pedir."

Marcar task "Criar Biblioteca de Marketing" como `completed`. Marcar TodoWrite T9B `completed`.

**Emitir `AskUserQuestion` de continuidade (B-S55-8):**

- question: "Podemos continuar?"
- options:
  - label: "Sim, vamos seguir", description: "Continua pra próxima etapa do onboarding."
  - label: "Pausa", description: "Encerra aqui — você retoma depois com /maestro-onboarding."

Se "Pausa" → encerrar skill silenciosamente.

### 2B.4 Pesquisa inicial do negócio (Turno T10B)

Marcar task "Pesquisa inicial do negócio" como `in_progress`. Marcar TodoWrite T10B `in_progress`.

**Só executar se a biblioteca foi criada no passo 2B.3.** Se pulou, pular esta etapa também (e marcar TodoWrite T10B `completed`).

**Turno T10B.** Renderizar literal o bloco `---TEXTO-T10B---` de `turnos-onboarding.md` (substituindo `{nome-alvo}`).

> [!critical] Usar AskUserQuestion estruturada — NÃO pergunta em texto livre
> Spec D2 (B-OnbUX-2A-2): emita AUQ com 2 opções literais ("Sim, vou informar o site" / "Pular"). NÃO mergear T10B com T11B numa pergunta única ("pesquisa OU material?"). Cada turno tem sua AUQ. Modelo Opus tende a otimizar mergeando — resista.

`AskUserQuestion`:
- question: "Quer fazer a pesquisa inicial agora?"
- options:
  - label: "Sim, vou informar o site", description: "Em seguida você digita a URL e eu rodo a pesquisa."
  - label: "Pular", description: "Pode pedir depois com 'pesquisa sobre minha empresa'."

**Persistir marker da Camada 3 ANTES de despachar Pesquisador:**

```bash
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-auq-pesquisa"
```

**Se "Sim, vou informar o site":** pedir o site numa mensagem curta de chat ("Qual o site da {nome-alvo}?"). Quando user responder, prosseguir.

Tratar este passo como uma **Entrega padrão**, igual ao step 2.9 do onboarding completo. Executar o fluxo `plugin/skills/maestro/fluxo-entrega.md` (5 itens, pipeline completo) para o pedido:

> "Pesquisa inicial sobre {nome da empresa}: site {url} e redes sociais. Mapear posicionamento atual, produtos/serviços, público-alvo aparente, tom de voz observado e presença em redes."

Parâmetros do dispatch:
- **Especialista:** Pesquisador
- **Categoria:** `pesquisa`
- **Tipo:** `pesquisa`
- **tags-dominio:** `pesquisa/empresa`
- **Ferramenta:** `ferramenta-default` do `~/.maestro/config.md`

O fluxo cobre Gerente cria tarefa → Pesquisador via `Agent()` → ciclo QA + Revisor → Gerente conclui. **Não invocar `Skill("/maestro:pesquisador")` direto** (B-S55-20).

**Se "Pular":**
- Informar literal: "Sem problema! Quando quiser, peça: 'pesquisa sobre minha empresa'."

Marcar task "Pesquisa inicial do negócio" como `completed` somente após o ciclo de validação retornar aprovado (ou após o usuário confirmar que pulou). Marcar TodoWrite T10B `completed`.

### 2B.5 Importar Material de Referência (Turno T11B)

**Se `SKIP_T14=true` (cenário pós-import via /importar-projeto):** pular esta seção inteira. Render literal "A importação já trouxe seu material — vamos pro próximo passo." e marcar TodoWrite T11B como `completed`. Seguir pro próximo turno.

Caso contrário, manter fluxo atual.

Marcar task "Importar material de referência" como `in_progress`. Marcar TodoWrite T11B `in_progress`.

**Só executar se a biblioteca foi criada no passo 2B.3.** Se pulou, pular esta etapa também (e marcar TodoWrite T11B `completed`).

**Turno T11B.** Renderizar literal o bloco `---TEXTO-T11B---` de `turnos-onboarding.md`.

> [!critical] Usar AskUserQuestion estruturada — NÃO pergunta em texto livre
> Spec D2 (B-OnbUX-2A-2): emita AUQ com 2 opções literais ("Sim, tenho material" / "Não tenho ou prefiro depois"). NÃO mergear com T10B.

`AskUserQuestion`:
- question: "Tem material de referência pra importar agora?"
- options:
  - label: "Sim, tenho material", description: "Coloque os arquivos em `{empresa}/referencias/` e me avise."
  - label: "Não tenho ou prefiro depois", description: "Pode pedir depois com 'lê meus arquivos de referência'."

**Persistir marker da Camada 3 após resposta:**

```bash
python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-auq-material"
```

**Se "Sim, tenho material":** seguir o fluxo de importação do Maestro Biblioteca.

**Se "Não tenho ou prefiro depois":** informar literal: "Sem problema! Quando tiver material, coloca na pasta `referencias/` e pede: 'lê meus arquivos de referência'."

Marcar task "Importar material de referência" como `completed`. Marcar TodoWrite T11B `completed`.

**Emitir `AskUserQuestion` de continuidade (B-S55-8):**

- question: "Podemos continuar?"
- options:
  - label: "Sim, vamos seguir", description: "Continua pra próxima etapa do onboarding."
  - label: "Pausa", description: "Encerra aqui — você retoma depois com /maestro-onboarding."

Se "Pausa" → encerrar skill silenciosamente.

### 2B.6 Finalização (Turno T12B)

Marcar task "Finalizar projeto" como `in_progress`. Marcar TodoWrite T12B `in_progress`.

> [!critical] Pre-output verification OBRIGATÓRIO
> ANTES de prosseguir, verificar que o state file ativo existe. Se ausente, ABORTAR e re-rodar o Bash de init que ativou Camadas 3+4 (T0 ou T1B conforme caso).
>
> ```bash
> if ! ls "$STATE_DIR"/state-*.md >/dev/null 2>&1; then
>     echo "[ABORTAR] state file ausente. Re-rodar Bash de init de Camadas 3+4 antes de finalizar." >&2
>     exit 1
> fi
> ```

1. Atualizar `$PROJETO_PATH/maestro/config.md`: setar `onboarding-completo: true` (cache já foi escrito na etapa 2B.2 passo 7; somente após verificação acima passar).

   > [!critical] Use Bash sed — NÃO use tool Edit com `$PROJETO_PATH` literal
   > Mesma regra do T15 do Fluxo de Primeira Vez (B-OnbUX-2A-3): variável Bash só expande no Bash. Use:
   >
   > ```bash
   > sed -i 's/^onboarding-completo:.*/onboarding-completo: true/' "$PROJETO_PATH/maestro/config.md"
   > ```

2. **Capturar report do REGENERATE PAINEL** despachado em 2B.2 passo 5. O retorno do `Agent()` é uma string com bloco `---REPORT---/---END-REPORT---`. Buscar dentro desse bloco a linha `aviso-colisao-pendente: true|false`.

   ```python
   # Pseudo-código
   import re
   match = re.search(r"aviso-colisao-pendente:\s*(true|false)", REPORT_REGENERATE)
   aviso_pendente = match.group(1) == "true" if match else False
   ```

3. **Se `aviso_pendente == True`:** emitir AUQ ao usuário (corresponde ao Passo 1 condicional de T12B em `turnos-onboarding.md`):

   ```
   AskUserQuestion:
     question: "Você acabou de criar seu segundo projeto nessa Área de Trabalho. Quer uma dica de 30 segundos pra evitar confusão quando dois projetos tiverem arquivos com nomes parecidos?"
     options:
       - label: "Sim, mostra a dica"
         description: "Mostro o texto aqui no terminal"
       - label: "Não, valeu"
         description: "Pula a dica — o callout fica no painel pra consulta depois"
   ```

4. **Se user respondeu "Sim":** renderizar literal o bloco `---TEXTO-T12B-DICA---` de `turnos-onboarding.md`. *(Texto idêntico ao callout permanente do `_painel/index.md` — single source of truth.)*

5. **Se `aviso_pendente == True`** (em qualquer caso da AUQ — Sim ou Não): despachar Bibliotecário FLUXO=UPDATE_FLAG pra marcar a flag:

   ```python
   Agent(
     subagent_type="maestro:bibliotecario",
     prompt="""
     TAREFA:
     FLUXO: UPDATE_FLAG

     CONTEXTO:
     workspace: $WORKSPACE_PATH
     flag-name: aviso-colisao-wikilink-mostrado
     flag-value: true
     """
   )
   ```

   Hook PreToolUse libera porque Bibliotecário é subagente. Maestro nunca escreve flag direto (aprendizado #46).

6. **Mensagem final ensinando Bookmarks** — condicional por contagem de projetos:

   - Detectar contagem: `glob $WORKSPACE_PATH/*/maestro/config.md` filtrado por `maestro-ativo: true`. Pode reusar resultado já no report do REGENERATE PAINEL (`projetos=<slug-1>,<slug-2>,...`).

   - Se `len(projetos) == 1` → renderizar literal o bloco `---TEXTO-T12B-FINAL-1---` de `turnos-onboarding.md` (substituindo `{nome-alvo}` e `<workspace-path-absoluto>`).
   - Se `len(projetos) >= 2` → renderizar literal o bloco `---TEXTO-T12B-FINAL-2---` de `turnos-onboarding.md` (substituindo `<workspace-path-absoluto>`).

   **Path normalizado pro SO nativo:** em Windows, mostrar com backslash (`C:\dev\...`); em Mac/Linux, com forward slash (`/Users/...`). Detectar via `cygpath -w` (Git Bash) ou `os.sep` se invocando Python.

7. **Persistir markers da Camada 3 + arquivar state:**

   ```bash
   python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "t-conclusao"
   python "$HELPERS/onboarding_state.py" archive "$STATE_DIR" "$SLUG"
   ```

8. **Edge case documentado:** se user fechar Claude Code antes de responder o AUQ no passo 3, a flag NÃO é marcada. Próxima sessão re-pergunta. Aceitável — AUQ é opt-in.

Marcar task "Finalizar projeto" como `completed`. Marcar TodoWrite T12B `completed`.

### 2B.6.1 Concluir tarefa no vault

Acionar Gerente de Projetos via Agent(haiku):

- Bloco TAREFA: "Concluir tarefa: Onboarding do projeto {nome da empresa}"
- Bloco CONTEXTO:
  - Caminho da tarefa: [caminho guardado em 2B.0.1 ou 2B.2.1]
  - Resultado: "Onboarding completo (novo projeto). Biblioteca criada, vault ativo."

---

## 3. Fluxo de Re-execução

Quando `onboarding-completo: true`, mostrar o estado atual e permitir alterações seletivas.

### 3.1 Detectar estado atual

Ler `maestro/config.md` e `~/.maestro/config.md` para montar o status.

### 3.2 Mostrar menu

Apresentar o estado atual:

```
Configuração atual do Maestro:

1. Seu nome: "{nome do usuário}" [alterar]
2. Empresa: "{nome}" [alterar]
3. Dependências: {instaladas ✓ | faltam N} [verificar]
4. Permissões: {configuradas ✓ | não configuradas} [configurar]
5. Biblioteca: {criada ✓ | não criada} [criar/recriar]
6. Obsidian: {guia de configuração} [configurar]
7. Pesquisador: {WebSearch (grátis) | Perplexity Sonar via OpenRouter ✓} [configurar/alterar]
8. Pesquisa inicial: {realizada ✓ | não realizada} [pesquisar]
9. Importar referências: {N arquivos importados | nenhum} [importar]
10. Status Line: {ativa ✓ | desativada} [ativar/configurar]
```

Após mostrar o estado, usar `AskUserQuestion` (conforme [[protocolo-interacao]]) com `multiSelect: true`:

- question: "O que você quer alterar?"
- multiSelect: true
- options:
  - label: "Identidade", description: "Nome, empresa"
  - label: "Infraestrutura", description: "Dependências, permissões, Obsidian, status line"
  - label: "Pesquisa", description: "Pesquisador, pesquisa inicial, importar referências, biblioteca"
  - label: "Nada", description: "Tudo certo, fechar o onboarding"

Quando o usuário escolher uma categoria, apresentar as opções específicas com `AskUserQuestion`:

**Se "Identidade":**
- options: "Meu nome" / "Empresa"

**Se "Infraestrutura":**
- options: "Dependências" / "Permissões" / "Obsidian" / "Status Line"

**Se "Pesquisa":**
- options: "Pesquisador" / "Pesquisa inicial" / "Importar referências" / "Biblioteca"

Executar o fluxo correspondente (seção 3.3) para cada item escolhido. Se marcou múltiplas categorias, executar em sequência.

Para o item 1 (Seu nome), ler `~/.maestro/memorias/nome-usuario.md`. Se não existir, mostrar "não configurado".

### 3.3 Executar alterações

**Opção 1 — Alterar nome do usuário:**
- Perguntar: "Como você gostaria que eu te chamasse?"
- Atualizar `~/.maestro/memorias/nome-usuario.md` com o novo nome
- Confirmar: "Pronto! A partir de agora te chamo de {NOME}."

**Opção 2 — Alterar empresa:**
- Perguntar novo nome
- Atualizar `maestro/config.md` com o novo nome no campo `Empresa:`
- Se a pasta do projeto existir no vault, avisar que o nome foi atualizado no config mas a pasta mantém o nome original (renomear manualmente se quiser)

**Opção 3 — Verificar dependências:**
- Mesmo fluxo do passo 2.3 (verificar Python e bibliotecas de leitura)

**Opção 4 — Configurar permissões:**
- Mesmo fluxo do passo 2.4 (explicar e pedir consentimento)

**Opção 5 — Criar/recriar biblioteca:**
- Informar: "Isso não apaga conteúdo existente, apenas recria arquivos faltantes."
- Chamar o Bibliotecário para scaffold

**Opção 6 — Configurar Obsidian:**
- Mesmo fluxo do passo 2.7 (verificar instalação, guiar criação do vault)

**Opção 7 — Configurar/alterar Pesquisador:**
- Mesmo fluxo do passo 2.8 (básico vs avançado, API key, ferramenta padrão), incluindo o teste da seção 2.8.1 ao informar nova key
- Se já tem key configurada, usar `AskUserQuestion` (conforme [[protocolo-interacao]]):
  - question: "O que quer alterar no Pesquisador?"
  - options:
    - label: "Trocar ferramenta padrão", description: "Alternar entre Sonar e Deep Research"
    - label: "Trocar API key", description: "Substituir a chave atual do OpenRouter"
    - label: "Remover configuração", description: "Volta pro modo básico (WebSearch grátis)"

**Opção 8 — Pesquisa inicial:**
- Mesmo fluxo do passo 2.9 (pedir site, acionar Pesquisador)

**Opção 9 — Importar referências:**
- Mesmo fluxo do passo 2.10 (verificar pasta, ler arquivos, catalogar, preencher via especialistas)
- Se já tem arquivos importados, informar quais são e oferecer: "Quer importar novos arquivos ou reimportar os existentes?"

**Opção 10 — Ativar/configurar status line:**
- Se desativada: mesmo fluxo da etapa 2.11
- Se ativa: mostrar o menu de configuração da status line (seção 4 da skill `[[maestro-statusline]]`)

---

## 4. Tom e Estilo

- Acolhedor e direto, sem jargão técnico
- Sem persona. É o Maestro falando diretamente
- Frases curtas, máximo 2-3 por mensagem quando possível
- Foco em ação, não em manual
- Acentos corretos em português, sempre

## 5. Validação de conteúdo no onboarding

Todo documento com conteúdo textual criado durante o onboarding DEVE passar pelo Ciclo de Validação (seção 6 do Maestro hub) antes de ser salvo. Isso inclui:
- Documentos de pesquisa (ex: teste de conexão do OpenRouter)
- Templates preenchidos via importação de referências
- Qualquer arquivo que o usuário vai ler no vault

**NÃO precisam de validação:** arquivos de configuração (`config.md`), estrutura de pastas (scaffold da biblioteca), indexes, e permissões.

Na prática: ao criar um documento com conteúdo, passar pelo QA + Revisor antes de salvar o arquivo. Se estiver no modo Skill() (sem Agent tool), aplicar o checklist do Protocolo de Escrita Natural manualmente antes de salvar.
