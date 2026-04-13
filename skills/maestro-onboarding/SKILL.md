---
name: maestro-onboarding
description: >
  Onboarding guiado do Sistema Maestro. Apresenta o sistema, configura o projeto
  e orienta os primeiros passos. Detectado automaticamente na primeira mensagem
  ou executado manualmente a qualquer momento.
---

> [!important] Antes de executar, verifique se o Sistema Maestro está ativo neste projeto seguindo o `core/protocolos/protocolo-ativacao.md`.

## 1. Detecção de Modo

Ao ser acionado, verificar o estado atual:

1. Tentar ler `maestro/config.md` no vault do projeto
2. Verificar o campo `onboarding-completo`

**Se `onboarding-completo` não existe ou é `false`:**
→ Executar o **Fluxo de Primeira Vez** (seção 2)

**Se `onboarding-completo: true`:**
→ Executar o **Fluxo de Re-execução** (seção 3)

---

## 2. Fluxo de Primeira Vez

### 2.0 Checklist pré-onboarding

ANTES de criar tasks ou iniciar qualquer etapa, verificar o que já está configurado no ambiente do usuário. Ler silenciosamente:

1. **Dependências:** testar `python --version` e bibliotecas (`docx`, `openpyxl`, `pdfplumber`)
2. **Permissões:** verificar se `.claude/settings.local.json` já tem a seção `permissions` do Maestro
3. **Memórias e config:** verificar se `maestro/config.md` e `maestro/memorias/` existem
4. **Biblioteca:** verificar se a pasta da empresa já existe com scaffold
5. **Pesquisador:** ler `user/config.md` e verificar se `openrouter-api-key` tem valor
6. **Status Line:** ler `~/.claude/settings.json` e verificar se `statusLine` já está configurada
7. **Obsidian:** tentar detectar se está instalado

Guardar o resultado em memória para uso nos passos seguintes. Etapas já concluídas serão puladas automaticamente com aviso ao usuário (ex: "Dependências já instaladas. Pulando.").

### 2.0.1 Tasks visuais

APÓS o checklist, criar tasks visuais no terminal. Criar APENAS as tasks de etapas que precisam ser executadas (pular as já concluídas):

```
TaskCreate({ subject: "Apresentar o Sistema Maestro", description: "Mensagem de boas-vindas", activeForm: "Apresentando o Sistema Maestro" })
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

### 2.0.2 Marcadores visuais

Ao iniciar cada etapa, exibir um separador visual antes da mensagem ao usuário:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Passo N de T — Nome da etapa
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Onde N é o número do passo atual e T é o total de passos a executar (descontando os pulados pelo checklist). Isso ajuda o usuário a saber onde está no processo.

### 2.1 Apresentação

Marcar task "Apresentar o Sistema Maestro" como `in_progress`.

Enviar mensagem de boas-vindas:

> "Prazer! Eu sou o Maestro, seu assistente de marketing e vendas.
>
> Funciono assim: você me pede qualquer coisa relacionada a marketing (criar headlines, montar um funil, definir posicionamento, planejar conteúdo) e eu direciono pro especialista certo. Cada especialista domina uma área e trabalha com frameworks reais de profissionais renomados.
>
> Vou fazer um setup rápido agora pra personalizar o sistema pro seu negócio."

Marcar task "Apresentar o Sistema Maestro" como `completed`.

**Aguardar confirmação do usuário antes de prosseguir.**

### 2.2 Nome da empresa

Marcar task "Configurar projeto" como `in_progress`.

Perguntar:

> "Qual o nome da sua empresa ou projeto?"

Aguardar resposta do usuário. Guardar o nome para usar nos próximos passos.

Marcar task "Configurar projeto" como `completed`.

### 2.3 Verificar dependências

Marcar task "Verificar dependências" como `in_progress`.

O Maestro precisa de ferramentas instaladas pra ler diferentes formatos de arquivo (PDF, DOCX, XLSX, etc.). Verificar e instalar o que for necessário.

1. **Verificar Python:**
   - Tentar `python --version`, depois `python3 --version` como fallback
   - Se nenhum funcionar: informar que o Python é necessário e pedir pro usuário instalar

2. **Verificar bibliotecas de leitura de documentos:**
   - Testar: `python -c "import docx" 2>/dev/null`, `python -c "import openpyxl" 2>/dev/null`, `python -c "import pdfplumber" 2>/dev/null`
   - Listar o que está faltando

3. **Pedir autorização pra instalar:**

   Se faltam bibliotecas:
   > "Pra ler seus documentos (PDF, Word, Excel), preciso instalar algumas ferramentas. São bibliotecas do Python usadas só pra leitura de arquivos:
   >
   > {lista do que falta, ex: python-docx, openpyxl, pdfplumber}
   >
   > Posso instalar?"

   **Se sim:** executar `python -m pip install {pacotes faltantes}`
   **Se não:** informar que a leitura de alguns formatos pode não funcionar e seguir adiante

4. Se tudo já está instalado, informar brevemente: "Dependências verificadas. Tudo pronto pra leitura de documentos."

Marcar task "Verificar dependências" como `completed`.

**Aguardar confirmação do usuário antes de prosseguir.**

### 2.4 Permissões do projeto

Marcar task "Configurar permissões" como `in_progress`.

Explicar ao usuário o que são as permissões e pedir consentimento ANTES de criar qualquer coisa (substituir `{CWD}` pelo caminho real):

> "Pra funcionar bem, o Maestro precisa de permissão pra ler, criar e editar arquivos dentro desta pasta (`{CWD}`).
>
> Sem isso, ele precisaria pedir sua autorização a cada arquivo, o que tornaria o trabalho bem lento.
>
> As permissões ficam restritas a este projeto. Fora desta pasta, o Maestro só acessa configurações do próprio Claude Code (como a barra de status).
>
> Posso configurar essas permissões?"

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
      "Bash(curl *)"
    ]
  }
}
```

Confirmar: "Permissões configuradas. Ficam salvas em `.claude/settings.local.json` e valem só pra este projeto."

**Se não:**

Informar: "Sem problema. O Maestro vai funcionar, mas vai pedir sua autorização com mais frequência durante o uso."

Marcar task "Configurar permissões" como `completed`.

**Aguardar confirmação do usuário antes de prosseguir.**

### 2.5 Setup técnico

Marcar task "Setup técnico" como `in_progress`.

Executar silenciosamente (sem mensagens detalhadas para cada item):

1. **Ativar sistema:** setar `maestro-ativo: true` em `user/config.md`
2. **Memórias de projeto:** criar `maestro/memorias/` usando templates de `core/templates/_memorias-projeto-template.md`:
   - `maestro/memorias/_index.md`
   - `maestro/memorias/contexto.md`
   - `maestro/memorias/sessoes.md`
   - `maestro/memorias/decisoes.md`
   - `maestro/memorias/agentes/` (pasta vazia)
3. **Config do projeto:** criar `maestro/config.md` usando `core/templates/_maestro-config-template.md`:
   - Preencher `Empresa:` com o nome coletado
   - Preencher `Vault:` com o caminho do CWD
   - Preencher `Projeto iniciado em:` com a data atual
   - Manter `onboarding-completo: false` (será atualizado no final)
4. **CLAUDE.md do projeto:** verificar se o CLAUDE.md do projeto do usuário tem seção `## Maestro`:
   - Se não existe CLAUDE.md: criar com a seção Maestro
   - Se existe mas sem seção Maestro: adicionar ao final
   - Conteúdo:
     ```
     ## Maestro
     > Sistema Maestro ativo. Configuração e memórias: maestro/config.md
     > Memórias de usuário: [caminho do plugin]/user/memorias/
     ```
5. **Memórias de usuário:** verificar se `user/memorias/_index.md` existe no plugin. Se não existe, informar que precisa ser recriado.

Informar brevemente: "Estrutura de memórias e configuração criadas."

Marcar task "Setup técnico" como `completed`.

### 2.6 Biblioteca de Marketing

Marcar task "Criar Biblioteca de Marketing" como `in_progress`.

Oferecer:

> "A Biblioteca de Marketing é onde guardamos todo o contexto do seu negócio: identidade, produtos, público, tom de voz. É uma estrutura organizada com templates prontos pra preencher.
>
> Quer criar agora?"

**Se sim:**
- Chamar o Bibliotecário (`[[maestro:bibliotecario]]`) para fazer scaffold dentro da pasta da empresa
- Informar: "Biblioteca criada! Você pode preencher os templates quando quiser. O sistema funciona mesmo sem eles preenchidos."

**Se não/depois:**
- Informar: "Sem problema! Quando quiser criar, é só pedir: 'cria minha biblioteca de marketing'."

Marcar task "Criar Biblioteca de Marketing" como `completed`.

**Aguardar confirmação do usuário antes de prosseguir.**

### 2.7 Obsidian

Marcar task "Configurar Obsidian" como `in_progress`.

Explicar:

> "Todos os arquivos que o Maestro cria são Markdown puro. Você pode editar direto no terminal, mas existe uma forma mais visual: o **Obsidian**.
>
> O Obsidian é um editor gratuito que transforma essa pasta em algo parecido com o Notion. Você navega pelos arquivos, edita com formatação visual, e tudo fica conectado por links. É a forma mais confortável de preencher templates e revisar entregas.
>
> Quer que eu te guie na instalação?"

**Se sim:**

1. Verificar se o Obsidian já está instalado:
   - Tentar detectar via `where obsidian 2>/dev/null` ou verificar se existe em caminhos comuns (`$LOCALAPPDATA/Obsidian`, `/Applications/Obsidian.app`, etc.)
   - **Se encontrado:** informar "Obsidian já está instalado!" e pular para o passo 3

2. Guiar a instalação:
   > "Baixe o Obsidian em https://obsidian.md/ (é grátis). Instale normalmente e abra o app.
   >
   > Me avise quando estiver pronto."
   - Aguardar confirmação do usuário

3. Guiar a criação do vault:
   > "Agora no Obsidian:
   > 1. Clique em **'Open folder as vault'** (ou 'Abrir pasta como vault')
   > 2. Selecione a pasta do seu projeto: `{caminho do CWD}/{nome da empresa}/`
   > 3. Pronto! Você vai ver toda a estrutura no painel esquerdo.
   >
   > Essa pasta tem tudo que é seu: biblioteca, pesquisas, entregas, tarefas. A configuração do sistema fica fora, então você só vê o que importa."

4. Sugerir configurações opcionais:
   > "Dica: nas configurações do Obsidian (engrenagem no canto inferior esquerdo), ative **'Files & Links' → 'Detect all file extensions'** pra ver todos os arquivos do projeto."

**Se não/depois:**
- Informar: "Sem problema! Tudo funciona no terminal mesmo. Se quiser configurar depois, rode `/maestro:onboarding` e escolha a opção do Obsidian."

Marcar task "Configurar Obsidian" como `completed`.

**Aguardar confirmação do usuário antes de prosseguir.**

### 2.8 Pesquisador

Marcar task "Configurar Pesquisador" como `in_progress`.

Explicar:

> "O Maestro tem um agente de pesquisa que busca dados na web: concorrência, mercado, tendências, referências. Pra marketing, ter fontes confiáveis faz toda a diferença na qualidade das entregas.
>
> O pesquisador tem dois modos:
>
> **Uso básico (grátis):** usa o WebSearch do Claude Code. Já funciona sem configuração.
>
> **Uso avançado (pago):** usa a Perplexity, uma ferramenta focada em busca com fontes confiáveis. A conexão é feita pelo OpenRouter, um serviço que dá acesso a vários modelos de IA por uma única API. O custo é por uso (centavos por pesquisa).
>
> Quer configurar o uso avançado agora ou prefere seguir com o básico?"

**Se quer configurar agora:**
- Perguntar: "Você já tem uma API key do OpenRouter?"
  - **Se sim:** pedir a key e salvar em `user/config.md` no campo `openrouter-api-key`
  - **Se não:** informar: "Você pode criar uma conta em https://openrouter.ai/, adicionar créditos e gerar uma API key na seção 'Keys'. Quando tiver, rode `/maestro:onboarding` pra configurar."
- Se a key foi informada, perguntar: "Quer que eu faça um teste rápido pra validar se a chave funciona? É uma chamada simples (custo ~$0.01)."
  - **Se sim:** executar teste conforme seção 2.8.1
  - **Se não:** pular o teste
- Perguntar: "Qual ferramenta usar como padrão? `sonar` (rápido, bom pra maioria das pesquisas) ou `sonar-deep-research` (mais profundo, mais lento, melhor pra análises complexas)?"
- Salvar a escolha no campo `ferramenta-default`

**Se prefere o básico:**
- Informar: "Perfeito! O WebSearch já funciona bem. Se quiser configurar o avançado depois, rode `/maestro:onboarding`."

Marcar task "Configurar Pesquisador" como `completed`.

**Aguardar confirmação do usuário antes de prosseguir.**

### 2.8.1 Teste da API Key do OpenRouter

Executar uma pesquisa real simples via `curl` ao endpoint do OpenRouter com o modelo mais barato (`perplexity/sonar`):

```bash
curl -s -w "\n%{http_code}" https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {API_KEY}" \
  -d '{"model":"perplexity/sonar","messages":[{"role":"user","content":"Qual é a capital do Brasil? Responda em uma frase."}],"max_tokens":30}'
```

**Interpretar o resultado:**

- **HTTP 200 + resposta válida:** informar "Chave validada! Conexão com o OpenRouter funcionando." Acionar o Pesquisador para salvar o documento de teste (delegar a criação do documento ao agente especialista, nunca criar diretamente).
- **HTTP 401 ou 403:** informar "A chave não foi aceita pelo OpenRouter. Verifique se está correta e tente novamente com `/maestro:onboarding`."
- **HTTP 402 ou erro de crédito:** informar "A chave é válida, mas sua conta no OpenRouter não tem créditos. Adicione saldo em openrouter.ai e a pesquisa paga vai funcionar."
- **Outro erro (timeout, rede):** informar "Não consegui conectar ao OpenRouter agora. A chave foi salva. Você pode testar depois pedindo: 'testa minha conexão com o OpenRouter'."

Se a chave falhou (401/403), **remover** o valor salvo em `user/config.md` e setar `ferramenta-default: websearch`.

### 2.9 Pesquisa inicial do negócio

Marcar task "Pesquisa inicial do negócio" como `in_progress`.

**Só executar se a biblioteca foi criada no passo 2.6.** Se o usuário pulou a biblioteca, pular esta etapa também.

Oferecer:

> "Quer que eu faça uma pesquisa rápida sobre o seu negócio? Posso analisar o site da empresa e redes sociais pra já ter um primeiro retrato.
>
> Isso ajuda a preencher a biblioteca com informações reais desde o início.
>
> Qual o site da {nome da empresa}?"

**Se informou o site:**
- Acionar o Pesquisador (`[[maestro:pesquisador]]`) com a tarefa de analisar o site e identificar: o que a empresa faz, produtos/serviços visíveis, tom de comunicação, público aparente, redes sociais linkadas
- Se encontrar redes sociais no site, pesquisar também os perfis
- O Pesquisador gera um documento de pesquisa na pasta `pesquisas/` do projeto
- Informar o resumo dos achados ao usuário

**Se não tem site ou prefere pular:**
- Informar: "Sem problema! Quando quiser, peça: 'pesquisa sobre minha empresa'."

Marcar task "Pesquisa inicial do negócio" como `completed`.

**Aguardar confirmação do usuário antes de prosseguir.**

### 2.10 Importar Material de Referência

Marcar task "Importar material de referência" como `in_progress`.

**Só executar se a biblioteca foi criada no passo 2.6.** Se o usuário pulou a biblioteca, pular esta etapa também.

Perguntar:

> "Você tem documentos sobre seu negócio? Manuais de marca, apresentações, planilhas de produto, textos internos, qualquer coisa com informação sobre a empresa.
>
> Se sim, coloca tudo na pasta `{empresa}/referencias/` e me avisa. Eu leio os arquivos e cruzo com o que já encontrei na pesquisa pra preencher o máximo possível da biblioteca."

**Se sim:**
- Aguardar o usuário colocar os arquivos e confirmar
- Seguir o fluxo de importação do Maestro Biblioteca (seção 9 da sub-skill `maestro/biblioteca`)
- O fluxo inclui: listar arquivos, verificar formatos, catalogar, perguntar modo (tudo ou um por um), preencher via especialistas
- Se houve pesquisa inicial (passo 2.9), usar os achados como contexto complementar no preenchimento

**Se não/depois:**
- Informar: "Sem problema! Quando tiver material, coloca na pasta `referencias/` e pede: 'lê meus arquivos de referência'."

Marcar task "Importar material de referência" como `completed`.

**Aguardar confirmação do usuário antes de prosseguir.**

### 2.11 Status Line

Marcar task "Configurar Status Line" como `in_progress`.

Oferecer:

> "Quer ativar uma barra de status no terminal? Ela mostra em tempo real o uso de contexto, limites da API e qual modelo está rodando. Você pode desligar a qualquer momento com `/maestro-statusline`."

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
     > Esse projeto está com o trust desativado. Posso ativar?"
   - Se o usuário aceitar: corrigir com replace binário (`false` → `true`). **Nunca usar json.load/json.dump** porque o arquivo tem surrogates Unicode que corrompem na serialização. Informar que a barra aparece após reiniciar.
   - Se o usuário recusar: informar que a barra não vai funcionar sem trust e seguir adiante.
6. Atualizar `user/config.md`: setar `statusline-ativo: true` na seção `## Status Line`
7. Informar: "Barra de status ativada! Ela mostra contexto, limites e modelo. Pra configurar ou desligar: `/maestro-statusline`."

**Se não:**
- Informar: "Sem problema! Quando quiser ativar, rode `/maestro-statusline`."

Marcar task "Configurar Status Line" como `completed`.

### 2.12 Finalização

Marcar task "Finalizar onboarding" como `in_progress`.

1. Atualizar `maestro/config.md`: setar `onboarding-completo: true`
2. Enviar mensagem de encerramento:

> "Tudo pronto! Agora é só me pedir o que precisar. Por exemplo: 'Crie headlines pra [produto da {nome da empresa}]'."

Marcar task "Finalizar onboarding" como `completed`.

---

## 3. Fluxo de Re-execução

Quando `onboarding-completo: true`, mostrar o estado atual e permitir alterações seletivas.

### 3.1 Detectar estado atual

Ler `maestro/config.md` e `user/config.md` para montar o status.

### 3.2 Mostrar menu

Apresentar o estado atual:

```
Configuração atual do Maestro:

1. Empresa: "{nome}" [alterar]
2. Dependências: {instaladas ✓ | faltam N} [verificar]
3. Permissões: {configuradas ✓ | não configuradas} [configurar]
4. Biblioteca: {criada ✓ | não criada} [criar/recriar]
5. Obsidian: {guia de configuração} [configurar]
6. Pesquisador: {WebSearch (grátis) | Perplexity Sonar via OpenRouter ✓} [configurar/alterar]
7. Pesquisa inicial: {realizada ✓ | não realizada} [pesquisar]
8. Importar referências: {N arquivos importados | nenhum} [importar]
9. Status Line: {ativa ✓ | desativada} [ativar/configurar]

O que você quer alterar? (número ou "nada")
```

### 3.3 Executar alterações

**Opção 1 — Alterar empresa:**
- Perguntar novo nome
- Atualizar `maestro/config.md` com o novo nome no campo `Empresa:`
- Se a pasta do projeto existir no vault, avisar que o nome foi atualizado no config mas a pasta mantém o nome original (renomear manualmente se quiser)

**Opção 2 — Verificar dependências:**
- Mesmo fluxo do passo 2.3 (verificar Python e bibliotecas de leitura)

**Opção 3 — Configurar permissões:**
- Mesmo fluxo do passo 2.4 (explicar e pedir consentimento)

**Opção 4 — Criar/recriar biblioteca:**
- Informar: "Isso não apaga conteúdo existente, apenas recria arquivos faltantes."
- Chamar o Bibliotecário para scaffold

**Opção 5 — Configurar Obsidian:**
- Mesmo fluxo do passo 2.7 (verificar instalação, guiar criação do vault)

**Opção 6 — Configurar/alterar Pesquisador:**
- Mesmo fluxo do passo 2.8 (básico vs avançado, API key, ferramenta padrão), incluindo o teste da seção 2.8.1 ao informar nova key
- Se já tem key configurada, oferecer: "Quer alterar a ferramenta padrão, trocar a key ou remover a configuração?"

**Opção 7 — Pesquisa inicial:**
- Mesmo fluxo do passo 2.9 (pedir site, acionar Pesquisador)

**Opção 8 — Importar referências:**
- Mesmo fluxo do passo 2.10 (verificar pasta, ler arquivos, catalogar, preencher via especialistas)
- Se já tem arquivos importados, informar quais são e oferecer: "Quer importar novos arquivos ou reimportar os existentes?"

**Opção 9 — Ativar/configurar status line:**
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
