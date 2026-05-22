# Turnos do onboarding — tabela determinística

> [!critical]
> **RENDERIZAÇÃO LITERAL OBRIGATÓRIA.**
>
> Cada bloco entre `---TEXTO-Tn---` e `---END-TEXTO-Tn---` deve ser
> renderizado literalmente, sem paráfrase, sem absorção em mensagem
> anterior, sem omissão. Otimizar "porque parece igual" ou "porque já
> mencionei" é violação. Hook auditor protege apenas dispatches críticos
> — defesa dos turnos textuais é responsabilidade da skill.
>
> **Antes de cada turno**, marque o item correspondente no TodoWrite
> como `in_progress`. **Depois de renderizar**, marque como `completed`
> e (quando aplicável) escreva o marker via:
> `python "$HELPERS/onboarding_state.py" mark "$STATE_DIR" "$SLUG" "<marker>"`.

---

## Fluxo de Primeira Vez

### T1 — Apresentação humana

- **Tipo:** texto-literal
- **Marker pós-render:** —
- **Origem:** SKILL.md seção 2.0.A (Turno 1)
- **Renderize literal:**

---TEXTO-T1---
Olá, tudo bem? Sou o Maestro e vou te ajudar a construir um ambiente de trabalho para marketing e vendas com IA utilizando o Claude Code e a interface e conexões neurais do Obsidian.
---END-TEXTO-T1---

### T1.5 — Nome do usuário (AUQ texto livre)

- **Tipo:** AUQ resposta livre
- **Marker pós-resposta:** `t-nome-usuario`
- **Origem:** F-Onb-2A (refinamento Sessão 74) — capturar nome cedo pra personalizar resto do fluxo. Substitui T10 antigo (que vinha tarde demais, depois de criar estrutura).
- **Pré-condição:** rodar APENAS se `~/.maestro/memorias/nome-usuario.md` não existe. Se existe, ler `<NOME>` da memória, pular T1.5 e marcar item como completed.
- **Renderize literal antes do AUQ:**

---TEXTO-T1.5---
Antes de continuar, como você quer que eu te chame?
---END-TEXTO-T1.5---

- **AUQ:**
  - Pergunta: "Como você quer que eu te chame?"
  - Placeholder/exemplo: "Will, Ana, Apelido — qualquer coisa que você usa no dia-a-dia."
- **Pós-resposta:**
  - Guardar `<NOME>` em variável runtime.
  - Persistir em memória global: gravar `~/.maestro/memorias/nome-usuario.md` com o nome capturado (próximas sessões e fluxos lerão direto, evitando re-perguntar).
  - Escrever marker `t-nome-usuario` no state file.
  - Renderizar literal `---TEXTO-T1.5-RESP---`:

---TEXTO-T1.5-RESP---
Beleza, `<NOME>`! Vou seguir.
---END-TEXTO-T1.5-RESP---

A partir de T2, todas as mensagens que tenham `<NOME>` no template usam o valor capturado.

### T2 — Pré-aviso de verificações técnicas

- **Tipo:** texto-literal
- **Marker pós-render:** —
- **Origem:** SKILL.md seção 2.0.A (Turno 2)
- **Renderize literal:**

---TEXTO-T2---
Antes de seguir, vou checar se você tem as ferramentas que o Maestro precisa no seu computador:

• **Python** — roda os scripts internos do sistema
• **Pandoc** — converte documentos quando você importa material de referência
• **Libs de leitura de documentos** (docx, xlsx, pdf) — leem arquivos quando você absorve material existente

Pode ser que eu precise te pedir alguma permissão durante a checagem.
---END-TEXTO-T2---

### T3 — Consentimento (AUQ)

- **Tipo:** AUQ
- **Marker pós-resposta:** `t-consentimento`
- **Origem:** SKILL.md seção 2.0.A (Turno 3)
- **AUQ:**
  - Pergunta: "Pode prosseguir com as verificações?"
  - Opções:
    - label: "Sim, pode prosseguir", description: "Vou checar dependências, permissões e o Obsidian no seu sistema."
    - label: "Agora não", description: "Encerra o onboarding aqui — pode retomar com /maestro-onboarding."
- **Pós-resposta:**
  - Se "Sim, pode prosseguir" → escrever marker `t-consentimento` e seguir pro T4 (verificações silenciosas).
  - Se "Agora não" → renderizar bloco `---TEXTO-T3-CANCEL---` abaixo e encerrar skill.

---TEXTO-T3-CANCEL---
Sem problemas. Quando estiver pronto, manda `/maestro-onboarding` que retomamos daqui.
---END-TEXTO-T3-CANCEL---

### T4 — Verificações técnicas (Bash silencioso)

- **Tipo:** Bash silencioso (não renderizar texto ao usuário)
- **Marker pós-render:** —
- **Origem:** SKILL.md seção 2.0.B
- **Ações:** executar checklist conforme seção 2.0.B do SKILL.md (dependências, permissões, memórias, biblioteca, pesquisador, status line, Obsidian). Guardar resultados em memória. Etapas concluídas serão puladas com aviso. Exceção: etapa do Obsidian (2.7) NUNCA é pulada pelo checklist.

### T5 — Roadmap

- **Tipo:** texto-literal
- **Marker pós-render:** —
- **Origem:** SKILL.md seção 2.0.C (Turno 5)
- **Renderize literal:**

---TEXTO-T5---
Tudo certo. Agora vou te guiar pelo setup — vai levar uns 20 minutos pra deixar o sistema pronto pra uso. A gente vai: (1) configurar a Área de Trabalho, (2) montar a Biblioteca de Marketing, (3) instalar e configurar o Obsidian com painéis automáticos de tarefas e projetos + atalhos de navegação rápida. Depois disso, partimos pra preencher a identidade da marca — sem pressa, no seu ritmo.
---END-TEXTO-T5---

### T6 — Apresentação da estrutura

- **Tipo:** texto-literal
- **Marker pós-render:** —
- **Origem:** SKILL.md seção 2.1 (Turno 6)
- **Renderize literal:**

---TEXTO-T6---
O Maestro trabalha com dois conceitos: **Área de Trabalho** e **Projetos**. Uma Área de Trabalho contém vários projetos dentro. Um projeto pode ser um cliente, uma marca, uma unidade de negócios — fica a seu critério. Vou te perguntar primeiro o nome da Área de Trabalho e depois o nome do primeiro projeto.
---END-TEXTO-T6---

### T7 — Confirmação de localização (AUQ, 3 opções)

- **Tipo:** AUQ
- **Marker pós-resposta:** `t-confirmacao-pasta` (audit trail) — só nas opções "aqui" e "subpasta".
- **Origem:** F-Onb-2A — princípio "perguntar antes de criar". 3 opções (refinamento Sessão 74).
- **Pré-condição:** ler `<CWD>` (pasta atual onde Claude Code está aberto).
- **Renderize literal antes do AUQ** (substituindo `<CWD>`):

---TEXTO-T7---
Antes de continuar, preciso confirmar onde vou criar tudo. A pasta atual é `<CWD>`.
---END-TEXTO-T7---

- **AUQ:**
  - Pergunta: "Onde quer criar a Área de Trabalho?"
  - Opções:
    - label: "Aqui mesmo nesta pasta", description: "A pasta atual vira a Área de Trabalho. Crio o marker e sigo o setup aqui."
    - label: "Em uma subpasta nova", description: "Crio uma subpasta com o nome da Área de Trabalho dentro da pasta atual e monto tudo lá dentro."
    - label: "Em outra pasta", description: "Encerro o onboarding aqui — abre o Claude Code na pasta que você quer e me chama de novo."
- **Pós-resposta:**
  - "Aqui mesmo nesta pasta" → guardar `SUBFOLDER_CHOICE=aqui`. Renderizar literal `---TEXTO-T7-AQUI---`. Escrever marker `t-confirmacao-pasta`. Prosseguir pra T8.
  - "Em uma subpasta nova" → guardar `SUBFOLDER_CHOICE=subpasta`. Renderizar literal `---TEXTO-T7-SUBPASTA---`. Escrever marker `t-confirmacao-pasta`. Prosseguir pra T8. Workspace path final = `<CWD>/<workspace_slug>/` (slug derivado em T8).
  - "Em outra pasta" → renderizar literal `---TEXTO-T7-OUTRA---` e encerrar skill (sem marker, sem mkdir).

---TEXTO-T7-AQUI---
Beleza, vou usar `<CWD>` como Área de Trabalho.
---END-TEXTO-T7-AQUI---

---TEXTO-T7-SUBPASTA---
Beleza, depois de você me dar o nome da Área de Trabalho, vou criar uma subpasta com esse nome aqui em `<CWD>` e montar tudo dentro dela.
---END-TEXTO-T7-SUBPASTA---

---TEXTO-T7-OUTRA---
Sem problema. Encerra essa sessão, abre o Claude Code na pasta que você quer usar como Área de Trabalho e roda `oi maestro` ou `/maestro-onboarding` de novo.
---END-TEXTO-T7-OUTRA---

### T8 — Nome da Área de Trabalho (AUQ)

- **Tipo:** AUQ (resposta livre)
- **Marker pós-resposta:** `t-nome-workspace`
- **Origem:** SKILL.md seção 2.2 passo 1 — slot T8 pós F-Onb-2D
- **AUQ:**
  - Pergunta: "Qual o nome dessa Área de Trabalho?"
  - Placeholder/exemplo: "ex: 'Marketing Primum', 'Agência X', 'Meus Clientes'"
- **Pós-resposta:** guardar `workspace_legivel`; computar `workspace_slug_proposto = slugify(workspace_legivel)`.

### T9 — Nome do primeiro projeto (AUQ)

- **Tipo:** AUQ (resposta livre)
- **Marker pós-resposta:** `t-nome-projeto`
- **Origem:** SKILL.md seção 2.2 passo 2 — slot T9 pós F-Onb-2D
- **AUQ:**
  - Pergunta: "E qual é o nome do primeiro projeto?"
  - Placeholder/exemplo: "uma empresa, cliente ou marca que você vai trabalhar"
- **Pós-resposta:** guardar `projeto_legivel` (este valor é o `{nome-alvo}` referenciado nas mensagens subsequentes); computar `projeto_slug_proposto = slugify(projeto_legivel)`.

### T9.1 — Validação anti-colisão (condicional, AUQ)

- **Tipo:** AUQ condicional (só dispara se `workspace_slug_proposto == projeto_slug_proposto`)
- **Marker pós-resposta:** —
- **Origem:** SKILL.md seção 2.2 passo 3 — slot T9.1 pós F-Onb-2D
- **AUQ:**
  - Pergunta: "Os dois ficaram com o mesmo nome curto (`<workspace_slug_proposto>`). Sugiro deixar a Área de Trabalho mais geral (ex: 'Meu Trabalho') e o projeto específico (ex: '`<projeto_legivel>`'). Quer trocar?"
  - Opções:
    - label: "Trocar Área de Trabalho", description: "Volta pro passo 1 e digita outro nome"
    - label: "Trocar projeto", description: "Volta pro passo 2 e digita outro nome"
    - label: "Manter assim", description: "Aceita os slugs idênticos sob seu risco"

### T9.2 — Preview de slugs (AUQ)

- **Tipo:** AUQ
- **Marker pós-resposta:** —
- **Origem:** SKILL.md seção 2.2 passo 4 — slot T9.2 pós F-Onb-2D
- **Pergunta varia por `SUBFOLDER_CHOICE`** (B-OnbUX-2A-7) — escolha um dos dois textos:

**Variante AQUI (`SUBFOLDER_CHOICE=aqui`):**
- Pergunta: "Vou criar a pasta `<projeto_slug_proposto>` aqui em `<CWD>` (sem subpasta `<workspace_slug_proposto>` — você escolheu usar esta pasta direto). Tudo bem ou quer mudar algum nome?"

**Variante SUBPASTA (`SUBFOLDER_CHOICE=subpasta`):**
- Pergunta: "Vou criar pasta `<workspace_slug_proposto>` com `<projeto_slug_proposto>` dentro. Tudo bem ou quer mudar algum nome?"

**Opções (iguais nas duas variantes):**
- label: "Tudo bem", description: "Cria com esses slugs"
- label: "Mudar Área de Trabalho", description: "Digito o slug direto (sem espaço, só letras minúsculas, números e hífens)"
- label: "Mudar projeto", description: "Digito o slug direto"

### T10 — Confirmação da estrutura e aviso do marker

- **Tipo:** texto-literal
- **Marker pós-render:** —
- **Origem:** SKILL.md seção 2.2.bis (Turno 10) — slot T10 pós F-Onb-2D
- **Renderize literal** (substituindo `{workspace_legivel}` e `{projeto_legivel}` pelos valores capturados em T8 e T9):

---TEXTO-T10---
Beleza, vou montar a Área de Trabalho **{workspace_legivel}** com **{projeto_legivel}** como primeiro projeto. Detalhe: vou criar um arquivo invisível chamado `.maestro-workspace` no canto pra eu reconhecer essa pasta como Área de Trabalho — não apague, ele que segura a estrutura.
---END-TEXTO-T10---

### T10-LEGACY — REMOVIDO no schema antigo (Sessão 74, refinamento F-Onb-2A)

> Esta seção marcava o slot T10 ANTES da F-Onb-2D (v2.40.2). Com a renumeração da F-Onb-2D, o conteúdo de "Confirmação da estrutura" (era T9 no schema antigo) ocupa o slot T10 atual. Esta nota fica como rastreabilidade histórica — não é mais um slot vazio operacional.
>
> **Detalhe histórico:** a captura do nome do usuário foi movida pra **T1.5** (logo após T1 Apresentação humana) na Sessão 74. Motivação: `<NOME>` precisa estar disponível em todo o fluxo subsequente pra personalizar mensagens — pedir só no slot T10 antigo era tarde demais. T1.5 grava em `~/.maestro/memorias/nome-usuario.md` e marca `t-nome-usuario` no state.

### T11 — Persistir verificações (Bash silencioso)

- **Tipo:** Bash silencioso (não renderizar texto ao usuário)
- **Marker pós-render:** `t-verificacoes` (já gravado em T4; aqui é o passo pós-estrutura)
- **Origem:** SKILL.md seção 2.5.5 (adicionado em F-Onb-2C) — roda APÓS setup técnico (2.5) criar `<projeto>/maestro/config.md`
- **Ações:** executar Bashes A+B da seção 2.5.5 (`check_tools.py log` + `patch_frontmatter.py mirror em config.md`). Detalhes completos na seção 2.5.5 do SKILL.md. Verificação obrigatória antes de marcar `completed` — ver pre-output verification do SKILL.md.

### T12 — Recado da Comunidade Automators

- **Tipo:** texto-literal
- **Marker pós-render:** —
- **Origem:** SKILL.md seção 2.2.qua (Turno 12)

> [!critical] Renderize INTEGRAL os 3 parágrafos + linha final com link (B-OnbUX-2A-13)
> A última linha (`Conheça a Comunidade Automators... https://automators.com.br`) é **parte literal**, não opcional. Aprendizado #52: Opus tende a omitir essa linha julgando "redundante" ou "fora do tom autoral". Resista — o link é o ponto mais importante do recado.

- **Renderize literal:**

---TEXTO-T12---
Antes de começarmos, um recado rápido:

O Sistema Maestro foi carinhosamente construído por Willian Nunes (@eusouwillnunes) para o time da Primum e para os membros da Comunidade Automators. Nosso foco é criar treinamentos rápidos, práticos e que resolvam problemas reais de marketing e vendas usando inteligência artificial, automações e vibe coding.

Na Comunidade você encontra o treinamento completo sobre o Sistema Maestro e todos os seus recursos. Além disso, enquanto sua assinatura estiver ativa, você recebe todas as atualizações automaticamente.

Conheça a Comunidade Automators e os benefícios de ser assinante em https://automators.com.br
---END-TEXTO-T12---

Após renderizar, perguntar (Turno 13): "Podemos continuar?" e aguardar resposta antes de prosseguir.

### T13 — Biblioteca de Marketing (texto + AUQ)

- **Tipo:** texto-literal + AUQ
- **Marker pós-resposta:** `t-auq-biblioteca`
- **Origem:** SKILL.md seção 2.6
- **Renderize literal antes do AUQ:**

---TEXTO-T13---
A Biblioteca de Marketing é onde guardamos todo o contexto de **{nome-alvo}**: identidade, produtos, público, tom de voz. É uma estrutura organizada com templates prontos pra preencher.
---END-TEXTO-T13---

- **AUQ:**
  - Pergunta: "Quer criar a Biblioteca de Marketing agora?"
  - Opções:
    - label: "Criar agora (Recomendado)", description: "Monta a estrutura com todos os templates prontos pra preencher"
    - label: "Depois", description: "Pula por enquanto. Você cria quando quiser pedindo 'cria minha biblioteca'"
- **Pós-resposta:**
  - Se "Criar agora" → despachar Bibliotecário FLUXO=CRIAR; informar literal: "Biblioteca criada! Você pode preencher os templates quando quiser. O sistema funciona mesmo sem eles preenchidos."
  - Se "Depois" → informar literal: "Sem problema! Quando quiser criar, é só pedir: 'cria minha biblioteca de marketing'."

### T14 — Pesquisa inicial do negócio (texto + AUQ implícito)

- **Tipo:** texto-literal + resposta livre
- **Marker pós-resposta:** `t-auq-pesquisa`
- **Origem:** SKILL.md seção 2.9
- **Pré-condição:** só executar se biblioteca foi criada em T12.
- **Renderize literal:**

---TEXTO-T14---
Quer que eu faça uma pesquisa rápida sobre **{nome-alvo}**? Posso analisar o site e redes sociais pra já ter um primeiro retrato.

Isso ajuda a preencher a biblioteca com informações reais desde o início.

Qual o site da {nome-alvo}?
---END-TEXTO-T14---

- **Pós-resposta:**
  - Se informou site → executar `fluxo-entrega.md` com Pesquisador conforme parâmetros da seção 2.9 do SKILL.md.
  - Se não tem site / pular → informar literal: "Sem problema! Quando quiser, peça: 'pesquisa sobre minha empresa'."

### T15 — Importar Material de Referência (texto-literal)

- **Tipo:** texto-literal + resposta livre
- **Marker pós-resposta:** `t-auq-material`
- **Origem:** SKILL.md seção 2.10
- **Pré-condição:** só executar se biblioteca foi criada em T12.
- **Renderize literal:**

---TEXTO-T15---
Você tem documentos sobre **{nome-alvo}**? Manuais de marca, apresentações, planilhas de produto, textos internos, qualquer coisa com informação sobre a empresa.

Se sim, coloca tudo na pasta `{empresa}/referencias/` e me avisa. Eu leio os arquivos e cruzo com o que já encontrei na pesquisa pra preencher o máximo possível da biblioteca.
---END-TEXTO-T15---

- **Pós-resposta:**
  - Se sim → seguir fluxo de importação (sub-skill `maestro/biblioteca` seção 9).
  - Se não/depois → informar literal: "Sem problema! Quando tiver material, coloca na pasta `referencias/` e pede: 'lê meus arquivos de referência'."

### T16 — Finalização (texto-literal + AUQ enfática de identidade)

- **Tipo:** texto-literal + AUQ
- **Marker pós-resposta:** `t-auq-identidade` + `t-conclusao`
- **Origem:** SKILL.md seção 2.12 (passos 3 e 4) — Turno 16
- **Renderize literal — CASO A** (`FASE = completa`, F4 já mergeada — `<workspace>/.obsidian/bookmarks.json` existe):

---TEXTO-T16-CASO-A---
✅ Tudo configurado! Sua Área de Trabalho está em `<workspace-path-absoluto-normalizado>` com seu primeiro projeto dentro.

📊 Pra acessar **{nome-alvo}** rapidamente: abre o Obsidian na pasta `<workspace-path>` → painel **Bookmarks** (ícone de marcador na lateral esquerda) → clica em **📊 Painel da Área de Trabalho** ou no nome do projeto.
---END-TEXTO-T16-CASO-A---

- **Renderize literal — CASO B** (`FASE = reduzida`, F2/F3/F4 ainda em construção):

---TEXTO-T16-CASO-B---
🎉 Área de Trabalho '`<workspace_legivel>`' criada em `<CWD>/<workspace_slug>/`, com o projeto '`<projeto_legivel>`' dentro.

Pra ver tudo no Obsidian:
1. Abra o app Obsidian
2. Clique em 'Open folder as vault' (ou 'Abrir pasta como vault')
3. Navegue até `<CWD>/<workspace_slug>/`
4. Clique em 'Select Folder'

Pra navegar pelos arquivos, use o painel **Files** (ícone de pasta na sidebar esquerda do Obsidian). Se você abrir o painel **Bookmarks** (ícone de marcador na lateral esquerda), também encontra atalhos rápidos pros painéis de tarefas, projetos e biblioteca já scaffoldados.
---END-TEXTO-T16-CASO-B---

- **Renderize literal — finalização enfática (independente de CASO A ou B, NÃO PULAR):**

---TEXTO-T16-IDENTIDADE---
Pronto! Agora a parte mais importante: **antes de qualquer agente trabalhar bem, ele precisa conhecer {nome-alvo}**. Topa começar a preencher a identidade da marca agora? Posso te guiar no chat (uma pergunta de cada vez) ou você abre os arquivos no Obsidian e preenche direto nas Properties — geralmente é mais rápido.
---END-TEXTO-T16-IDENTIDADE---

- **AUQ:**
  - Pergunta: "Como prefere preencher a identidade de {nome-alvo}?"
  - Opções:
    - label: "Guia no chat", description: "Eu te conduzo uma pergunta de cada vez."
    - label: "Vou preencher no Obsidian", description: "Você abre os arquivos e preenche nas Properties."
    - label: "Agora não", description: "Termino o onboarding aqui — pode preencher depois."
- **Pós-resposta:**
  - "Guia no chat" → invocar fluxo do Entrevistador via despacho padrão (Gerente cria tarefa primeiro).
  - "Vou preencher no Obsidian" → renderizar literal:

---TEXTO-T16-OBSIDIAN---
Beleza! Os arquivos da identidade estão em `<workspace>/<projeto_slug>/biblioteca-de-marketing/`. Abre o `_index-biblioteca.md` no Obsidian — ele lista todos os templates da identidade (manifesto, círculo dourado, posicionamento, perfil do público, tom de voz, personalidade da marca, identidade visual, história dos fundadores). Cada um tem **Properties** no topo do arquivo — clica em qualquer Property pra editar visualmente. Quando quiser, manda `quero preencher a identidade de {nome-alvo}` no chat e eu te guio pelo que faltar.
---END-TEXTO-T16-OBSIDIAN---

  - "Agora não" → renderizar literal:

---TEXTO-T16-DEPOIS---
Beleza, quando quiser, manda `quero preencher a identidade de {nome-alvo}`.
---END-TEXTO-T16-DEPOIS---

Após resposta, escrever marker `t-conclusao` e despachar Gerente para concluir tarefa de onboarding (SKILL.md seção 2.12.1).

---

## Fluxo de Novo Projeto (2B)

### T0 — Pasta vazia + Maestro globalmente configurado (Caso 4 do 2B.-1)

- **Tipo:** texto-literal + AUQ
- **Marker pós-resposta "Sim":** `t-consentimento` (substitui consentimento técnico que não existe nesse fluxo) + `t-confirmacao-pasta`
- **Origem:** F-Onb-2A — Caso 4 de 2B.-1. Disparado quando: nenhum dos 3 sinais detectados E `~/.maestro/config.md` existe.
- **Pré-condição:** ler `~/.maestro/memorias/nome-usuario.md` para `<NOME>` (se existir).
- **Renderize literal antes do AUQ** (substituindo `<NOME>` se disponível, e `<CWD>`):

---TEXTO-T0---
Olá de novo, `<NOME>`! Você já tem o Sistema Maestro configurado, mas esta pasta (`<CWD>`) está vazia — sem Área de Trabalho nem projeto. Vou usar ela como Área de Trabalho?
---END-TEXTO-T0---

> Se `<NOME>` não estiver disponível em `~/.maestro/memorias/nome-usuario.md`, omitir vocativo: "Você já tem o Sistema Maestro..." (sem `Olá de novo, X!`).

- **AUQ** (3 opções — ver SKILL.md seção 2B.-1 para detalhes do Bash crítico):
  - Pergunta: "Vou usar esta pasta como Área de Trabalho?"
  - Opções:
    - label: "Sim, usar esta pasta", description: "Crio o marker `.maestro-workspace` aqui e sigo o setup do primeiro projeto."
    - label: "Não, quero outra pasta", description: "Encerro o onboarding aqui — abre o Claude Code na pasta certa e me chama de novo."
    - label: "Cancelar", description: "Não fazer nada agora."
- **Pós-resposta:**
  - "Sim, usar esta pasta" → renderizar literal `---TEXTO-T0-SIM---`, inicializar state file (Bash obrigatório — ver SKILL.md), escrever markers `t-consentimento` + `t-confirmacao-pasta`, criar marker `.maestro-workspace`, prosseguir pra T1B (nome do novo projeto).
  - "Não, quero outra pasta" → renderizar literal `---TEXTO-T0-NAO---` e encerrar skill (sem marker, sem mkdir).
  - "Cancelar" → renderizar literal `---TEXTO-T0-CANCEL---` e encerrar skill (mesmo tratamento de "Não").

---TEXTO-T0-SIM---
Beleza! Vou montar a Área de Trabalho aqui em `<CWD>` e já criar o primeiro projeto dentro.
---END-TEXTO-T0-SIM---

---TEXTO-T0-NAO---
Sem problema. Encerra essa sessão, abre o Claude Code na pasta que você quer usar como Área de Trabalho e roda `oi maestro` ou `/maestro-onboarding` de novo.
---END-TEXTO-T0-NAO---

---TEXTO-T0-CANCEL---
Sem problema. Encerra essa sessão, abre o Claude Code na pasta que você quer usar como Área de Trabalho e roda `oi maestro` ou `/maestro-onboarding` de novo.
---END-TEXTO-T0-CANCEL---

### T1B — Boas-vindas + nome do novo projeto (texto + AUQ)

- **Tipo:** texto-literal + AUQ
- **Marker pós-resposta:** `t-nome-projeto`
- **Origem:** SKILL.md seção 2B.1
- **Pré-condição:** ler `~/.maestro/memorias/nome-usuario.md` para `<NOME>`; resolver `workspace_legivel` (cache local ou basename do CWD).

> [!critical] Renderizar LITERAL com placeholders preenchidos — proibido parafrasear (B-OnbUX-2A-4)
> Texto exato: vocativo `<NOME>` + nome literal da Área de Trabalho `<workspace_legivel>` entre aspas simples. NÃO substituir por "Beleza!" ou frase neutra. NÃO omitir o nome do workspace. Ambos são gancho personalizado pro user retornante reconhecer onde está. Aprendizado #52 — Opus tende a paragrafrar texto literal "porque parece igual"; resista.

- **Renderize literal antes do AUQ** (substituindo `<NOME>` e `<workspace_legivel>`):

---TEXTO-T1B---
Olá, <NOME>! Você já tem a Área de Trabalho '<workspace_legivel>' montada. Vou só adicionar um projeto novo dentro dela.
---END-TEXTO-T1B---

- **AUQ:**
  - Pergunta: "Qual o nome do novo projeto?"
  - Placeholder/exemplo: "uma empresa, cliente ou marca que você vai trabalhar"
- **Pós-resposta:** guardar `projeto_legivel`; computar `projeto_slug_proposto = slugify(projeto_legivel)`. Aplicar validação anti-duplicata e preview conforme passos 4 e 5 da seção 2B.1.

### T9B — Biblioteca de Marketing (texto + AUQ)

- **Tipo:** texto-literal + AUQ
- **Marker pós-resposta:** `t-auq-biblioteca`
- **Origem:** SKILL.md seção 2B.3
- **Renderize literal antes do AUQ:**

---TEXTO-T9B---
A Biblioteca de Marketing é onde guardamos todo o contexto de **{nome-alvo}**: identidade, produtos, público, tom de voz.
---END-TEXTO-T9B---

- **AUQ:**
  - Pergunta: "Quer criar a Biblioteca de Marketing agora?"
  - Opções:
    - label: "Criar agora (Recomendado)", description: "Monta a estrutura com todos os templates prontos pra preencher"
    - label: "Depois", description: "Pula por enquanto. Você cria quando quiser pedindo 'cria minha biblioteca'"
- **Pós-resposta:**
  - Se "Criar agora" → despachar Bibliotecário FLUXO=CRIAR.
  - Se "Depois" → informar literal: "Sem problema! Quando quiser, é só pedir."

### T10B — Pesquisa inicial do negócio

- **Tipo:** texto-literal + AUQ estruturada
- **Marker pós-resposta:** `t-auq-pesquisa`
- **Origem:** SKILL.md seção 2B.4
- **Pré-condição:** só executar se biblioteca foi criada em T9B.
- **Renderize literal:**

---TEXTO-T10B---
Quer que eu faça uma pesquisa rápida sobre **{nome-alvo}**? Posso analisar o site e redes sociais pra já ter um primeiro retrato.
---END-TEXTO-T10B---

- **AUQ obrigatória (NÃO usar pergunta em texto livre — sempre AskUserQuestion estruturada):**
  - Pergunta: "Quer fazer a pesquisa inicial agora?"
  - Opções:
    - label: "Sim, vou informar o site", description: "Em seguida você digita a URL e eu rodo a pesquisa."
    - label: "Pular", description: "Pode pedir depois com 'pesquisa sobre minha empresa'."

- **Pós-resposta:**
  - Se "Sim, vou informar o site" → pedir o site via mensagem curta ("Qual o site da {nome-alvo}?") e em seguida executar `fluxo-entrega.md` com Pesquisador (parâmetros na seção 2B.4 do SKILL.md).
  - Se "Pular" → informar literal: "Sem problema! Quando quiser, peça: 'pesquisa sobre minha empresa'."

### T11B — Importar Material de Referência

- **Tipo:** texto-literal + AUQ estruturada
- **Marker pós-resposta:** `t-auq-material`
- **Origem:** SKILL.md seção 2B.5
- **Pré-condição:** só executar se biblioteca foi criada em T9B.
- **Renderize literal:**

---TEXTO-T11B---
Você tem documentos sobre este negócio? Manuais de marca, apresentações, planilhas de produto, textos internos — qualquer coisa com informação sobre o projeto.
---END-TEXTO-T11B---

- **AUQ obrigatória (NÃO usar pergunta em texto livre — sempre AskUserQuestion estruturada):**
  - Pergunta: "Tem material de referência pra importar agora?"
  - Opções:
    - label: "Sim, tenho material", description: "Coloque os arquivos em `{empresa}/referencias/` e me avise."
    - label: "Não tenho ou prefiro depois", description: "Pode pedir depois com 'lê meus arquivos de referência'."

- **Pós-resposta:**
  - Se "Sim, tenho material" → seguir fluxo de importação do Maestro Biblioteca.
  - Se "Não tenho ou prefiro depois" → informar literal: "Sem problema! Quando tiver material, coloca na pasta `referencias/` e pede: 'lê meus arquivos de referência'."

> **Importante:** T10B e T11B NÃO devem ser mergeadas em uma pergunta única. Cada turno tem sua AUQ. Aprendizado #58 — modelo Opus tende a otimizar mergeando passos quando "parece equivalente"; resista.

### T12B — Finalização (com AUQ de dica de colisão + Bookmarks)

- **Tipo:** AUQ condicional + texto-literal
- **Marker pós-resposta:** `t-conclusao`
- **Origem:** SKILL.md seção 2B.6

**Passo 1 — AUQ condicional de colisão (só dispara se report do REGENERATE PAINEL trouxer `aviso-colisao-pendente: true`):**

- **AUQ:**
  - Pergunta: "Você acabou de criar seu segundo projeto nessa Área de Trabalho. Quer uma dica de 30 segundos pra evitar confusão quando dois projetos tiverem arquivos com nomes parecidos?"
  - Opções:
    - label: "Sim, mostra a dica", description: "Mostro o texto aqui no terminal"
    - label: "Não, valeu", description: "Pula a dica — o callout fica no painel pra consulta depois"
- **Se "Sim" — renderize literal:**

---TEXTO-T12B-DICA---
💡 **Nomes iguais entre projetos:**

Você tem múltiplos projetos nessa Área de Trabalho. Se dois projetos tiverem um arquivo com o mesmo nome (ex: `funil-webinar`), o Obsidian abre o do projeto onde você está agora.

Pra abrir o de outro projeto, use a busca rápida (`Ctrl+O` ou `Cmd+O`) e digite o nome da pasta antes — ex: `cliente-b/funil-webinar`.
---END-TEXTO-T12B-DICA---

Em qualquer caso (Sim ou Não), despachar Bibliotecário FLUXO=UPDATE_FLAG conforme seção 2B.6 passo 5.

**Passo 2 — Mensagem final ensinando Bookmarks (condicional por contagem de projetos):**

- **Se `len(projetos) == 1` — renderize literal:**

---TEXTO-T12B-FINAL-1---
📊 Pra acessar **{nome-alvo}** rapidamente: abre o Obsidian na pasta `<workspace-path-absoluto>` → painel **Bookmarks** (ícone de marcador na lateral esquerda) → clica em **📊 Painel da Área de Trabalho** ou no nome do projeto.
---END-TEXTO-T12B-FINAL-1---

- **Se `len(projetos) >= 2` — renderize literal:**

---TEXTO-T12B-FINAL-2---
📊 Pra navegar entre projetos rapidamente: abre o Obsidian na pasta `<workspace-path-absoluto>` → painel **Bookmarks** → tem o painel da Área de Trabalho e cada projeto a 2 cliques.
---END-TEXTO-T12B-FINAL-2---

Após renderizar, escrever marker `t-conclusao` e despachar Gerente para concluir tarefa (SKILL.md seção 2B.6.1).
