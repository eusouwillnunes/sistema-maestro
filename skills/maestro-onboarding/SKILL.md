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
TaskCreate({ subject: "Configurar Pesquisador", description: "Apresentar opções de pesquisa e configurar se necessário", activeForm: "Configurando Pesquisador" })
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
- Perguntar: "Qual ferramenta usar como padrão? `sonar` (rápido, bom pra maioria) ou `sonar-deep-research` (mais profundo, mais lento)?"
- Salvar a escolha no campo `ferramenta-default`

**Se não:**
- Informar: "Tudo bem! O WebSearch já dá conta do recado. Se mudar de ideia, rode `/maestro:onboarding` pra configurar depois."

Marcar task "Configurar Pesquisador" como `completed`.

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
3. Pesquisador: {WebSearch (grátis) | Perplexity Sonar via OpenRouter ✓} [configurar/alterar]

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

**Opção 3 — Configurar/alterar Pesquisador:**
- Mesmo fluxo do passo 2.5 (perguntar API key e ferramenta padrão)
- Se já tem key configurada, oferecer: "Quer alterar a ferramenta padrão, trocar a key, ou remover a configuração?"

---

## 4. Tom e Estilo

- **Acolhedor e direto** — sem jargão técnico
- **Sem persona** — é o Maestro falando diretamente
- **Frases curtas** — máximo 2-3 frases por mensagem quando possível
- **Sem listas de comandos** — foco em ação, não em manual
- **Use acentos corretos em português** — sempre
