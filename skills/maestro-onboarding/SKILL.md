---
name: maestro-onboarding
description: >
  Onboarding guiado do Sistema Maestro. Apresenta o sistema, configura o projeto
  e orienta os primeiros passos. Detectado automaticamente na primeira mensagem
  ou executado manualmente a qualquer momento.
---

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

### 2.0 Tasks visuais

ANTES de qualquer outra ação, criar tasks visuais no terminal para o usuário acompanhar o progresso:

```
TaskCreate({ subject: "Apresentar o Sistema Maestro", description: "Mensagem de boas-vindas e explicação do que o Maestro faz", activeForm: "Apresentando o Sistema Maestro" })
TaskCreate({ subject: "Configurar projeto", description: "Coletar nome da empresa e registrar", activeForm: "Configurando projeto" })
TaskCreate({ subject: "Criar estrutura de memórias", description: "Setup técnico: memórias, config e CLAUDE.md", activeForm: "Criando estrutura de memórias" })
TaskCreate({ subject: "Criar Biblioteca de Marketing", description: "Oferecer scaffold da biblioteca no vault", activeForm: "Criando Biblioteca de Marketing" })
TaskCreate({ subject: "Importar material de referência", description: "Oferecer importação de documentos existentes do negócio", activeForm: "Importando material de referência" })
TaskCreate({ subject: "Configurar Obsidian", description: "Oferecer guia de instalação e configuração do Obsidian como editor visual", activeForm: "Configurando Obsidian" })
TaskCreate({ subject: "Configurar Pesquisador", description: "Apresentar opções de pesquisa e configurar se necessário", activeForm: "Configurando Pesquisador" })
TaskCreate({ subject: "Configurar Status Line", description: "Oferecer ativação da barra de status no terminal", activeForm: "Configurando Status Line" })
TaskCreate({ subject: "Finalizar onboarding", description: "Encerrar com sugestão de primeira ação", activeForm: "Finalizando onboarding" })
```

Marcar cada task como `in_progress` ANTES de executar a etapa e `completed` LOGO APÓS terminar.

### 2.1 Apresentação

Marcar task "Apresentar o Sistema Maestro" como `in_progress`.

Enviar mensagem de boas-vindas:

> "Prazer! Eu sou o Maestro — seu assistente de marketing e vendas.
>
> Funciono assim: você me pede qualquer coisa relacionada a marketing — criar headlines, montar um funil, definir posicionamento, planejar conteúdo — e eu direciono pro especialista certo. Cada especialista domina uma área e trabalha com frameworks reais de profissionais renomados.
>
> Vou fazer um setup rápido agora pra personalizar o sistema pro seu negócio."

Marcar task "Apresentar o Sistema Maestro" como `completed`.

### 2.2 Nome da empresa

Marcar task "Configurar projeto" como `in_progress`.

Perguntar:

> "Qual o nome da sua empresa ou projeto?"

Aguardar resposta do usuário. Guardar o nome para usar nos próximos passos.

Marcar task "Configurar projeto" como `completed`.

### 2.3 Setup técnico

Marcar task "Criar estrutura de memórias" como `in_progress`.

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

Informar brevemente: "Estrutura de memórias criada."

Marcar task "Criar estrutura de memórias" como `completed`.

### 2.4 Biblioteca de Marketing

Marcar task "Criar Biblioteca de Marketing" como `in_progress`.

Oferecer:

> "A Biblioteca de Marketing é uma estrutura organizada onde guardamos todo o contexto do seu negócio — identidade, produtos, público, tom de voz. Quer criar agora?"

**Se sim:**
- Chamar o Bibliotecário (`[[maestro:bibliotecario]]`) para fazer scaffold dentro da pasta da empresa
- Informar: "Biblioteca criada! Você pode preencher os templates quando quiser — o sistema funciona mesmo sem eles preenchidos."

**Se não/depois:**
- Informar: "Sem problema! Quando quiser criar, é só pedir: 'cria minha biblioteca de marketing'."

Marcar task "Criar Biblioteca de Marketing" como `completed`.

### 2.4.1 Importar Material de Referência

Marcar task "Importar material de referência" como `in_progress`.

**Só executar se a biblioteca foi criada no passo 2.4.** Se o usuário pulou a biblioteca, pular esta etapa também.

Perguntar:

> "Você já tem documentos sobre seu negócio? Manuais de marca, apresentações, planilhas de produto, textos de site, qualquer coisa com informação sobre a empresa.
>
> Se sim, coloca tudo na pasta `{empresa}/referencias/` e me avisa. Eu leio os arquivos e preencho o que der da biblioteca automaticamente."

**Se sim:**
- Aguardar o usuário colocar os arquivos e confirmar
- Seguir o fluxo de importação do Maestro Biblioteca (seção 9 da sub-skill `maestro/biblioteca`)
- O fluxo inclui: listar arquivos → verificar formatos → oferecer instalar ferramentas se necessário → catalogar → perguntar modo (tudo ou um por um) → preencher via especialistas

**Se não/depois:**
- Informar: "Sem problema! Quando tiver material, coloca na pasta `referencias/` e pede: 'lê meus arquivos de referência'."

Marcar task "Importar material de referência" como `completed`.

### 2.4.2 Obsidian

Marcar task "Configurar Obsidian" como `in_progress`.

Explicar:

> "Todos os arquivos que o Maestro cria — biblioteca, pesquisas, entregas — são Markdown puro. Você pode editar direto no terminal, mas existe uma forma muito mais visual: o **Obsidian**.
>
> O Obsidian é um editor gratuito que transforma essa pasta em algo parecido com o Notion — você navega pelos arquivos, edita com formatação visual, e tudo fica conectado por links. É a forma mais confortável de preencher templates e revisar entregas.
>
> Quer que eu te guie na instalação e configuração?"

**Se sim:**

1. Verificar se o Obsidian já está instalado:
   - Tentar detectar via `where obsidian 2>/dev/null` ou verificar se existe em caminhos comuns (`$LOCALAPPDATA/Obsidian`, `/Applications/Obsidian.app`, etc.)
   - **Se encontrado:** informar "Obsidian já está instalado!" → pular para o passo 3

2. Guiar a instalação:
   > "Baixe o Obsidian em **obsidian.md** (é grátis). Instale normalmente e abra o app.
   >
   > Me avise quando estiver pronto."
   - Aguardar confirmação do usuário

3. Guiar a criação do vault:
   > "Agora no Obsidian:
   > 1. Clique em **'Open folder as vault'** (ou 'Abrir pasta como vault')
   > 2. Selecione a pasta do seu projeto: `{caminho do CWD}`
   > 3. Pronto! Você vai ver toda a estrutura de pastas no painel esquerdo.
   >
   > A pasta `{nome da empresa}/` é onde fica sua Biblioteca de Marketing. Pode navegar e editar qualquer arquivo por lá."

4. Sugerir configurações opcionais:
   > "Dica: nas configurações do Obsidian (engrenagem no canto inferior esquerdo), ative **'Files & Links' → 'Detect all file extensions'** para ver todos os arquivos do projeto."

**Se não/depois:**
- Informar: "Sem problema! Tudo funciona no terminal mesmo. Se quiser configurar depois, rode `/maestro:onboarding` e escolha a opção do Obsidian."

Marcar task "Configurar Obsidian" como `completed`.

### 2.5 Pesquisador

Marcar task "Configurar Pesquisador" como `in_progress`.

Explicar:

> "O Maestro tem um agente de pesquisa que busca dados na web — concorrência, mercado, tendências, referências.
>
> Por padrão, ele usa o WebSearch (grátis e já funciona). Se quiser pesquisas mais profundas, pode usar a Perplexity via OpenRouter (tem custo por uso).
>
> Você já tem uma API key do OpenRouter?"

**Se sim:**
- Pedir a key
- Salvar em `user/config.md` no campo `openrouter-api-key`
- Perguntar: "Quer que eu faça um teste rápido pra validar se a chave funciona? É uma chamada simples ao Sonar (custo ~$0.01)."
  - **Se sim:** executar teste conforme seção 2.5.1
  - **Se não:** pular o teste e continuar
- Perguntar: "Qual ferramenta usar como padrão? `sonar` (rápido, bom pra maioria) ou `sonar-deep-research` (mais profundo, mais lento)?"
- Salvar a escolha no campo `ferramenta-default`

**Se não:**
- Informar: "Tudo bem! O WebSearch já dá conta do recado. Se mudar de ideia, rode `/maestro:onboarding` pra configurar depois."

Marcar task "Configurar Pesquisador" como `completed`.

### 2.5.1 Teste da API Key do OpenRouter

Executar uma pesquisa real simples via `curl` ao endpoint do OpenRouter com o modelo mais barato (`perplexity/sonar`):

```bash
curl -s -w "\n%{http_code}" https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {API_KEY}" \
  -d '{"model":"perplexity/sonar","messages":[{"role":"user","content":"Qual é a capital do Brasil? Responda em uma frase."}],"max_tokens":30}'
```

**Interpretar o resultado:**

- **HTTP 200 + resposta válida:** informar "Chave validada! Conexão com o OpenRouter funcionando." → salvar pesquisa de teste (ver abaixo)
- **HTTP 401 ou 403:** informar "A chave não foi aceita pelo OpenRouter. Verifique se está correta e tente novamente com `/maestro:onboarding`."
- **HTTP 402 ou erro de crédito:** informar "A chave é válida, mas sua conta no OpenRouter não tem créditos. Adicione saldo em openrouter.ai e a pesquisa paga vai funcionar."
- **Outro erro (timeout, rede):** informar "Não consegui conectar ao OpenRouter agora. A chave foi salva — você pode testar depois pedindo: 'testa minha conexão com o OpenRouter'."

Se a chave falhou (401/403), **remover** o valor salvo em `user/config.md` e setar `ferramenta-default: websearch`.

**Salvar pesquisa de teste (apenas quando HTTP 200):**

1. Ler `pasta-pesquisas` de `user/config.md` (padrão: `pesquisas/`)
2. Criar o arquivo `{pasta-pesquisas}/AAAA-MM-DD-teste-conexao-openrouter.md` com:

```
---
titulo: Teste de conexão — OpenRouter
tipo: livre
projeto: {nome da empresa}
ferramenta: sonar
data: AAAA-MM-DD
status: atual
tags: [teste, openrouter, configuração]
---

# Teste de conexão — OpenRouter

## Objetivo
Validar que a API key do OpenRouter está funcionando corretamente.

## Resultado
- **Status:** Conexão bem-sucedida
- **Modelo:** perplexity/sonar
- **Resposta recebida:** {resposta do modelo}

> [!sources]
> - Teste executado via onboarding do Sistema Maestro — {data}
```

3. Atualizar (ou criar) `{pasta-pesquisas}/_pesquisas.md` com nova entrada no topo:

```
| AAAA-MM-DD | Teste de conexão — OpenRouter | livre | sonar | [[AAAA-MM-DD-teste-conexao-openrouter]] |
```

### 2.5.2 Status Line

Marcar task "Configurar Status Line" como `in_progress`.

Oferecer:

> "Quer ativar uma barra de status no terminal? Ela mostra em tempo real o uso de contexto, limites da API e qual modelo está rodando. Você pode desligar a qualquer momento com `/maestro:statusline`."

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
5. Atualizar `user/config.md` — setar `statusline-ativo: true` na seção `## Status Line`
6. Informar: "Barra de status ativada! Ela mostra contexto, limites e modelo. Para configurar ou desligar: `/maestro:statusline`."

**Se não:**
- Informar: "Sem problema! Quando quiser ativar, rode `/maestro:statusline`."

Marcar task "Configurar Status Line" como `completed`.

### 2.6 Finalização

Marcar task "Finalizar onboarding" como `in_progress`.

1. Atualizar `maestro/config.md` — setar `onboarding-completo: true`
2. Enviar mensagem de encerramento:

> "Tudo pronto! Agora é só me pedir o que precisar. Por exemplo: 'Crie headlines para [produto da {nome da empresa}]'."

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
2. Biblioteca: {criada ✓ | não criada} [criar/recriar]
3. Importar referências: {N arquivos importados | nenhum} [importar]
4. Obsidian: {guia de configuração} [configurar]
5. Pesquisador: {WebSearch (grátis) | Perplexity Sonar via OpenRouter ✓} [configurar/alterar]
6. Status Line: {ativa ✓ | desativada} [ativar/configurar]

O que você quer alterar? (número ou "nada")
```

### 3.3 Executar alterações

**Opção 1 — Alterar empresa:**
- Perguntar novo nome
- Atualizar `maestro/config.md` com o novo nome no campo `Empresa:`
- Se a pasta do projeto existir no vault: avisar que o nome foi atualizado no config mas a pasta mantém o nome original (renomear manualmente se quiser)

**Opção 2 — Criar/recriar biblioteca:**
- Informar: "Isso não apaga conteúdo existente — apenas recria arquivos faltantes."
- Chamar o Bibliotecário para scaffold

**Opção 3 — Importar referências:**
- Mesmo fluxo do passo 2.4.1 (verificar pasta, ler arquivos, catalogar, preencher)
- Se já tem arquivos importados, informar quais são e oferecer: "Quer importar novos arquivos ou reimportar os existentes?"

**Opção 4 — Configurar Obsidian:**
- Mesmo fluxo do passo 2.4.2 (verificar instalação, guiar criação do vault)

**Opção 5 — Configurar/alterar Pesquisador:**
- Mesmo fluxo do passo 2.5 (perguntar API key e ferramenta padrão), incluindo o teste da seção 2.5.1 ao informar uma nova key
- Se já tem key configurada, oferecer: "Quer alterar a ferramenta padrão, trocar a key, ou remover a configuração?"

**Opção 6 — Ativar/configurar status line:**
- Se desativada: ler preferências de `user/config.md` (se existem usar, se não usar defaults). Gerar script, configurar settings.json, ativar. Mesmo fluxo da etapa 2.5.2.
- Se ativa: mostrar o menu de configuração da status line (seção 4 da skill `[[maestro:statusline]]`).

---

## 4. Tom e Estilo

- **Acolhedor e direto** — sem jargão técnico
- **Sem persona** — é o Maestro falando diretamente
- **Frases curtas** — máximo 2-3 frases por mensagem quando possível
- **Sem listas de comandos** — foco em ação, não em manual
- **Use acentos corretos em português** — sempre
