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

Ao ser acionado, verificar o estado atual:

1. Tentar ler `maestro/config.md` no vault do projeto
2. Verificar o campo `onboarding-completo`
3. Verificar se `~/.maestro/config.md` existe (sistema já configurado em outro projeto)

**Se `maestro/config.md` não existe E `~/.maestro/config.md` existe:**
→ Executar o **Fluxo de Novo Projeto** (seção 2B) — onboarding leve, pula dependências e configurações globais

**Se `onboarding-completo` não existe ou é `false` (e `~/.maestro/config.md` não existe):**
→ Executar o **Fluxo de Primeira Vez** (seção 2) — onboarding completo

**Se `onboarding-completo: true`:**
→ Executar o **Fluxo de Re-execução** (seção 3)

---

## 2. Fluxo de Primeira Vez

### 2.0 Checklist pré-onboarding

ANTES de criar tasks ou iniciar qualquer etapa, verificar o que já está configurado no ambiente do usuário. Ler silenciosamente:

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

### 2.0.1 Tasks visuais

APÓS o checklist, criar tasks visuais no terminal. Criar APENAS as tasks de etapas que precisam ser executadas (pular as já concluídas):

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

Ao iniciar cada etapa, exibir um separador visual antes da mensagem ao usuário:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Passo N de T — Nome da etapa
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Onde N é o número do passo atual e T é o total de passos a executar (descontando os pulados pelo checklist). Isso ajuda o usuário a saber onde está no processo.

### 2.1 Apresentação, nome do usuário e recado

Marcar task "Apresentar o Sistema Maestro" como `in_progress`.

**Etapa A — Apresentação e nome do usuário:**

Enviar mensagem:

> "Olá, tudo bem? Eu sou o Maestro, responsável por orquestrar a sua equipe de marketing e garantir que tudo vai ser entregue na qualidade que você precisa.
>
> Como você gostaria que eu te chamasse?"

**Aguardar resposta do usuário.** Guardar o nome informado.

Responder:

> "É um prazer, {NOME}!"

Salvar o nome na memória de usuário (`~/.maestro/memorias/`). Criar ou atualizar o arquivo `~/.maestro/memorias/nome-usuario.md` com:

```markdown
---
tipo: usuario
descricao: Como o usuário gostaria de ser chamado
---

Nome: {NOME}
```

Atualizar o index `~/.maestro/memorias/_index.md` se necessário.

A partir deste ponto, usar o nome do usuário nas interações sempre que natural (sem forçar em toda frase).

**Etapa B — Recado da Comunidade dos Últimos:**

Enviar mensagem:

> "Antes de começarmos, eu tenho um recado rápido.
>
> O Sistema Maestro foi construído por Willian Nunes (siga ele no Instagram @eusouwillnunes) para a sua Equipe da Primum e para os membros d'A Comunidade dos Últimos. Na comunidade você encontra um curso completo sobre o Sistema Maestro onde você vai aprender a utilizar todos os recursos do sistema, mesmo se não souber nada de IA. Você também desbloqueia o acesso ao Sistema Maestro PRO, com funcionalidades exclusivas para membros. Todo mês entram novos treinamentos e conteúdos sobre Marketing e Vendas e sobre Desenvolvimento de Software e Aplicativos usando Inteligência Artificial.
>
> Acesse acomunidadedosultimos.com.br, e seja um membro fundador por um valor simbólico e vitalício por mês.
>
> Recado dado, vamos começar!"

Marcar task "Apresentar o Sistema Maestro" como `completed`.

**Perguntar ao usuário: "Podemos continuar?" e aguardar resposta antes de prosseguir.**

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

2. **Corrigir python3 no Windows (se necessário):**
   - Testar `python3 --version` — se retornar exit code 49, é o atalho da Microsoft Store que não funciona
   - Se detectado: informar ao usuário:
     > "Detectei que o comando `python3` no seu computador aponta pra Microsoft Store em vez do Python real. Isso impede a leitura de documentos Word, PDF e Excel.
     >
     > Pra resolver, vou criar um atalho que faz o `python3` apontar pro Python que você já tem instalado. Isso envolve dois ajustes simples:
     > - Criar um arquivo em `~/.local/bin/python3` (um atalho pro Python real)
     > - Adicionar essa pasta no PATH do seu terminal (pra ele encontrar o atalho)
     >
     > Nada é desinstalado ou alterado no seu Python. Posso fazer?"
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
   > {lista do que falta, ex: pandoc, python-docx, openpyxl, pdfplumber}
   >
   > Posso instalar?"

   **Se sim:** executar os comandos de instalação (pandoc via gerenciador de pacotes do SO, bibliotecas Python via `python -m pip install {pacotes faltantes}`)
   **Se não:** informar que a leitura de alguns formatos pode não funcionar e seguir adiante

6. Se tudo já está instalado, informar brevemente: "Dependências verificadas. Tudo pronto pra leitura de documentos."

Marcar task "Verificar dependências" como `completed`.

**Perguntar ao usuário: "Podemos continuar?" e aguardar resposta antes de prosseguir.**

### 2.3.5 Verificar ~/.maestro/

Executar silenciosamente, sem mensagem detalhada ao usuário:

1. Verificar se `~/.maestro/` existe: `test -d ~/.maestro`
2. Se **NÃO existir** → criar a estrutura:
   ```bash
   mkdir -p ~/.maestro/memorias/agentes ~/.maestro/overrides ~/.maestro/personas
   ```
3. Verificar se `~/.maestro/config.md` existe: `test -f ~/.maestro/config.md`
   - Se **NÃO existir** → copiar o template inicial: `cp [plugin]/user/config.md ~/.maestro/config.md`
   - Substituir `[plugin]` pelo caminho real do diretório do plugin (onde está o SKILL.md)
4. Se já existir → manter sem alteração (preservar configurações do usuário)

Informar brevemente apenas se precisou criar: "Diretório `~/.maestro/` criado para suas configurações globais."

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

**Perguntar ao usuário: "Podemos continuar?" e aguardar resposta antes de prosseguir.**

### 2.5 Setup técnico

Marcar task "Setup técnico" como `in_progress`.

Executar silenciosamente (sem mensagens detalhadas para cada item):

1. **Ativar sistema:** setar `maestro-ativo: true` em `~/.maestro/config.md`
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
     > Memórias de usuário: ~/.maestro/memorias/
     ```
5. **Memórias de usuário:** verificar se `~/.maestro/memorias/_index.md` existe. Se não existe, criar a estrutura `~/.maestro/` (conforme passo 2.3.5).

Informar brevemente: "Estrutura de memórias e configuração criadas."

Marcar task "Setup técnico" como `completed`.

### 2.5.1 Criar tarefa no vault (se não criada em 2.0.2)

Se a tarefa de onboarding ainda não foi criada (pasta `tarefas/` foi criada agora pelo setup técnico):
- Acionar Gerente de Projetos via Agent(haiku) com o mesmo payload descrito em 2.0.2
- Guardar caminho do arquivo de tarefa para usar na conclusão (step 2.12.1)

### 2.6 Biblioteca de Marketing

Marcar task "Criar Biblioteca de Marketing" como `in_progress`.

Oferecer:

> "A Biblioteca de Marketing é onde guardamos todo o contexto do seu negócio: identidade, produtos, público, tom de voz. É uma estrutura organizada com templates prontos pra preencher."

Usar `AskUserQuestion` (conforme [[protocolo-interacao]]):
- question: "Quer criar a Biblioteca de Marketing agora?"
- options:
  - label: "Criar agora (Recomendado)", description: "Monta a estrutura com todos os templates prontos pra preencher"
  - label: "Depois", description: "Pula por enquanto. Você cria quando quiser pedindo 'cria minha biblioteca'"

**Se sim:**
- Chamar o Bibliotecário via `Skill(maestro:bibliotecario)` para fazer scaffold dentro da pasta da empresa
- Informar: "Biblioteca criada! Você pode preencher os templates quando quiser. O sistema funciona mesmo sem eles preenchidos."

**Se não/depois:**
- Informar: "Sem problema! Quando quiser criar, é só pedir: 'cria minha biblioteca de marketing'."

Marcar task "Criar Biblioteca de Marketing" como `completed`.

**Perguntar ao usuário: "Podemos continuar?" e aguardar resposta antes de prosseguir.**

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

**Perguntar ao usuário: "Podemos continuar?" e aguardar resposta antes de prosseguir.**

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
> Para um tutorial completo com prints e vídeo, acesse A Comunidade dos Últimos: https://acomunidadedosultimos.com.br"

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

**Perguntar ao usuário: "Podemos continuar?" e aguardar resposta antes de prosseguir.**

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

Se a chave falhou (401/403), **remover** o valor salvo em `~/.maestro/config.md` e setar `ferramenta-default: websearch`.

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
- Despachar o Pesquisador com a tarefa de analisar o site da empresa e redes sociais
- O Pesquisador usará `ferramenta-default` do config automaticamente (definido no step 2.8)
- O Pesquisador segue seus próprios protocolos de encomenda e entrega

**Se não tem site ou prefere pular:**
- Informar: "Sem problema! Quando quiser, peça: 'pesquisa sobre minha empresa'."

Marcar task "Pesquisa inicial do negócio" como `completed`.

**Perguntar ao usuário: "Podemos continuar?" e aguardar resposta antes de prosseguir.**

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

**Perguntar ao usuário: "Podemos continuar?" e aguardar resposta antes de prosseguir.**

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
     > Esse projeto está com o trust desativado. Posso ativar?"
   - Se o usuário aceitar: corrigir com replace binário (`false` → `true`). **Nunca usar json.load/json.dump** porque o arquivo tem surrogates Unicode que corrompem na serialização. Informar que a barra aparece após reiniciar.
   - Se o usuário recusar: informar que a barra não vai funcionar sem trust e seguir adiante.
6. Atualizar `~/.maestro/config.md`: setar `statusline-ativo: true` na seção `## Status Line`
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

### 2.12.1 Concluir tarefa no vault

Acionar Gerente de Projetos via Agent(haiku):

- Bloco TAREFA: "Concluir tarefa: Onboarding do projeto {nome da empresa}"
- Bloco CONTEXTO:
  - Caminho da tarefa: [caminho guardado em 2.0.2 ou 2.5.1]
  - Resultado: "Onboarding completo. Biblioteca criada, pesquisador configurado, vault ativo."

---

## 2B. Fluxo de Novo Projeto

Onboarding leve para quando o usuário já tem o Sistema Maestro configurado (`~/.maestro/` existe) mas está num projeto novo. Pula dependências, permissões, Obsidian, status line e apresentação.

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

### 2B.1 Boas-vindas e nome da empresa

Marcar task "Configurar novo projeto" como `in_progress`.

Ler `~/.maestro/memorias/nome-usuario.md` para recuperar o nome do usuário.

Enviar mensagem:

> "Olá, {NOME}! Vejo que você já usa o Maestro. Vou configurar este novo projeto rapidinho."

Perguntar:

> "Qual o nome da empresa ou projeto?"

Aguardar resposta do usuário. Guardar o nome.

Usar `AskUserQuestion` (conforme [[protocolo-interacao]]):
- question: "A pasta raiz do projeto é o diretório atual?"
- options:
  - label: "Sim, usar {CWD}", description: "O projeto será configurado nesta pasta"
  - label: "Não, quero outra pasta", description: "Informar o caminho correto"

**Se escolheu outra pasta:** perguntar qual o caminho e confirmar.

Marcar task "Configurar novo projeto" como `completed`.

**Perguntar ao usuário: "Podemos continuar?" e aguardar resposta antes de prosseguir.**

### 2B.2 Setup do projeto

Marcar task "Setup do projeto" como `in_progress`.

Executar silenciosamente:

1. **Config do projeto:** criar `maestro/config.md` usando `core/templates/_maestro-config-template.md`:
   - Preencher `Empresa:` com o nome coletado
   - Preencher `Vault:` com o caminho confirmado
   - Preencher `Projeto iniciado em:` com a data atual
   - Setar `maestro-ativo: true`
   - Manter `onboarding-completo: false` (será atualizado no final)
2. **Memórias de projeto:** criar `maestro/memorias/` usando templates de `core/templates/_memorias-projeto-template.md`:
   - `maestro/memorias/_index.md`
   - `maestro/memorias/contexto.md`
   - `maestro/memorias/sessoes.md`
   - `maestro/memorias/decisoes.md`
   - `maestro/memorias/agentes/` (pasta vazia)
3. **CLAUDE.md do projeto:** verificar se o CLAUDE.md do projeto tem seção `## Maestro`:
   - Se não existe CLAUDE.md: criar com a seção Maestro
   - Se existe mas sem seção Maestro: adicionar ao final
   - Conteúdo:
     ```
     ## Maestro
     > Sistema Maestro ativo. Configuração e memórias: maestro/config.md
     > Memórias de usuário: ~/.maestro/memorias/
     ```
4. **Atualização de permissões existentes (patch silencioso):**
   - Se o projeto já tem `.claude/settings.local.json`, abra o arquivo e verifique se `permissions.allow` contém `WebSearch` e `WebFetch(domain:*)`. Se faltar alguma das duas, adicione ao array. Não pergunte consentimento — o usuário já autorizou o padrão de permissões no onboarding completo anterior. Apenas informe: "Permissões atualizadas com WebSearch e WebFetch (necessárias para o Pesquisador)."
   - Se o projeto não tem `settings.local.json`, criar o arquivo completo com o bloco de permissões padrão (mesma lista do onboarding completo, seção 2.4).

Informar brevemente: "Estrutura do projeto criada."

Marcar task "Setup do projeto" como `completed`.

### 2B.2.1 Criar tarefa no vault (se não criada em 2B.0.1)

Se a tarefa de onboarding ainda não foi criada:
- Acionar Gerente de Projetos via Agent(haiku) com o mesmo payload descrito em 2B.0.1
- Guardar caminho do arquivo de tarefa para usar na conclusão

### 2B.3 Biblioteca de Marketing

Mesmo fluxo da etapa 2.6 do onboarding completo:

Marcar task "Criar Biblioteca de Marketing" como `in_progress`.

Oferecer:

> "A Biblioteca de Marketing é onde guardamos todo o contexto do seu negócio: identidade, produtos, público, tom de voz."

Usar `AskUserQuestion` (conforme [[protocolo-interacao]]):
- question: "Quer criar a Biblioteca de Marketing agora?"
- options:
  - label: "Criar agora (Recomendado)", description: "Monta a estrutura com todos os templates prontos pra preencher"
  - label: "Depois", description: "Pula por enquanto. Você cria quando quiser pedindo 'cria minha biblioteca'"

**Se sim:** chamar o Bibliotecário via `Skill(maestro:bibliotecario)` para fazer scaffold dentro da pasta da empresa.

**Se não/depois:** informar: "Sem problema! Quando quiser, é só pedir."

Marcar task "Criar Biblioteca de Marketing" como `completed`.

**Perguntar ao usuário: "Podemos continuar?" e aguardar resposta antes de prosseguir.**

### 2B.4 Pesquisa inicial do negócio

Mesmo fluxo da etapa 2.9 do onboarding completo:

Marcar task "Pesquisa inicial do negócio" como `in_progress`.

**Só executar se a biblioteca foi criada no passo 2B.3.** Se pulou, pular esta etapa também.

> "Quer que eu faça uma pesquisa rápida sobre o seu negócio? Posso analisar o site da empresa e redes sociais.
>
> Qual o site da {nome da empresa}?"

**Se informou o site:**
- Despachar o Pesquisador com a tarefa de analisar o site da empresa e redes sociais
- O Pesquisador usará `ferramenta-default` do config automaticamente

**Se não tem site ou prefere pular:**
- Informar: "Sem problema! Quando quiser, peça: 'pesquisa sobre minha empresa'."

Marcar task "Pesquisa inicial do negócio" como `completed`.

**Perguntar ao usuário: "Podemos continuar?" e aguardar resposta antes de prosseguir.**

### 2B.5 Importar Material de Referência

Mesmo fluxo da etapa 2.10 do onboarding completo:

Marcar task "Importar material de referência" como `in_progress`.

**Só executar se a biblioteca foi criada no passo 2B.3.** Se pulou, pular esta etapa também.

> "Você tem documentos sobre este negócio? Manuais de marca, apresentações, planilhas de produto, textos internos.
>
> Se sim, coloca tudo na pasta `{empresa}/referencias/` e me avisa."

**Se sim:** seguir o fluxo de importação do Maestro Biblioteca.

**Se não/depois:** informar: "Sem problema! Quando tiver material, coloca na pasta `referencias/` e pede: 'lê meus arquivos de referência'."

Marcar task "Importar material de referência" como `completed`.

**Perguntar ao usuário: "Podemos continuar?" e aguardar resposta antes de prosseguir.**

### 2B.6 Finalização

Marcar task "Finalizar projeto" como `in_progress`.

1. Atualizar `maestro/config.md`: setar `onboarding-completo: true`
2. Enviar mensagem:

> "Projeto {nome da empresa} configurado! O que vamos trabalhar?"

Marcar task "Finalizar projeto" como `completed`.

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
