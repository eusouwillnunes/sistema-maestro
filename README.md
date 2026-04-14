# Sistema Maestro

Plugin de marketing e vendas para Claude Code. Uma equipe completa de agentes especialistas em copywriting, estratégia, branding, mídias sociais e performance — coordenados por IA, com memória entre sessões e entregas no Obsidian.

## Instalação

```bash
/plugin marketplace add eusouwillnunes/sistema-maestro
/plugin install maestro@sistema-maestro
```

Na próxima mensagem, o Maestro faz o setup do seu projeto automaticamente.

## Use quando precisar

- "Cria uma headline pro meu curso"
- "Monta um funil de vendas pro meu produto"
- "Define o posicionamento da minha marca"
- "Faz um calendário de conteúdo pro Instagram"
- "Analisa minha campanha no Meta Ads"
- "Escreve uma página de vendas"
- "Pesquisa meus concorrentes"
- "Cria uma oferta irresistível"
- "Define o tom de voz da minha marca"
- "Faz um diagnóstico do meu negócio"

Você pede em linguagem natural. O Maestro entende, decompõe em tarefas e delega pro especialista certo.

## Agentes Especialistas

### Copywriter

Textos persuasivos baseados nos frameworks de Eugene Schwartz. Headlines, páginas de vendas, VSLs, emails, sequências de nutrição e bullets.

**Use when:** criar headline, escrever página de vendas, montar email de lançamento, criar VSL, escrever copy de anúncio, fazer bullets de oferta

**Categorias:** copywriting, headlines, persuasão, páginas de vendas, email marketing, VSL, scripts de venda

### Estrategista

Estratégia de marketing e negócios com frameworks de Russell Brunson e Alex Hormozi. Funis, ofertas de alto valor, diagnósticos e lançamentos.

**Use when:** montar funil de vendas, criar oferta irresistível, planejar lançamento, fazer diagnóstico de negócio, definir estratégia de aquisição, planejar webinário

**Categorias:** funil de vendas, oferta, lançamento, diagnóstico, aquisição de clientes, webinário, estratégia digital

### Marca

Identidade e posicionamento com frameworks de Simon Sinek e Marty Neumeier. Propósito, Golden Circle, naming, tom de voz e diferenciação.

**Use when:** definir posicionamento, criar identidade de marca, escolher nome de marca, definir tom de voz, criar manifesto, encontrar propósito da empresa

**Categorias:** branding, posicionamento, identidade de marca, naming, tom de voz, propósito, diferenciação, arquétipo

### Mídias Sociais

Estratégia e conteúdo com frameworks de Gary Vaynerchuk e Brendan Kane. Planejamento, calendário editorial, criação de posts, análise e viralização.

**Use when:** criar calendário de conteúdo, planejar posts pro Instagram, montar estratégia de mídias sociais, criar reels, analisar engajamento, planejar conteúdo pro TikTok

**Categorias:** mídias sociais, Instagram, TikTok, LinkedIn, YouTube, calendário editorial, conteúdo, reels, stories, engajamento, viralização

### Performance

Análise de campanhas pagas com frameworks de Perry Marshall. Diagnóstico de métricas, testes A/B, otimização de canais e escala.

**Use when:** analisar campanha no Meta Ads, otimizar Google Ads, diagnosticar performance de anúncios, planejar testes A/B, escalar campanha, analisar ROAS

**Categorias:** tráfego pago, Meta Ads, Google Ads, TikTok Ads, performance, ROAS, CPA, CTR, CPL, teste A/B, remarketing

## Agentes Operacionais

| Agente | O que faz |
|--------|-----------|
| **Pesquisador** | Pesquisa de mercado, concorrência e audiência com fontes verificáveis (WebSearch + Perplexity) |
| **Entrevistador** | Coleta dados do seu negócio via conversa guiada, uma pergunta por vez |
| **Gestor de Tarefas** | Cria e acompanha tarefas e entrevistas no vault Obsidian |
| **Bibliotecário** | Cria e gerencia sua Biblioteca de Marketing (contexto reutilizável) |
| **QA** | Verificação automática de checklists antes de cada entrega |
| **Revisor** | Garante que todo texto soe natural e humano (Protocolo de Escrita Natural) |

## Como o Maestro trabalha

O sistema decide automaticamente a melhor forma de executar cada tarefa:

- **Pedidos simples** ("cria uma headline") → delega direto pro agente especialista
- **Pedidos complexos** ("preenche a identidade") → decompõe em tarefas com dependências, executa em sequência ou paralelo
- **Quando faltam dados** → cria entrevistas e coleta do usuário antes de produzir
- **Quando precisa de pesquisa** → despacha o Pesquisador em paralelo

Tudo fica registrado no vault Obsidian: tarefas, entrevistas, pesquisas, entregas. Você acompanha o progresso e retoma de onde parou.

## Sessões de trabalho

O Maestro tem rituais de abertura e fechamento de sessão. Você não precisa decorar comandos — basta falar naturalmente.

**Para iniciar:**
- "Bom dia"
- "Iniciar sessão"
- "Começar trabalho"

O Maestro apresenta um dashboard com o estado do projeto: tarefas pendentes, entrevistas na fila, progresso da biblioteca e o que ficou da última sessão.

**Para encerrar:**
- "Encerrar sessão"
- "Parar por hoje"
- "Chega por hoje"

O Maestro registra o que foi feito, o que ficou em andamento e sugere por onde começar na próxima vez.

## Funcionalidades

- **12 agentes especializados** trabalhando em conjunto
- **Memória entre sessões** — o sistema aprende suas preferências e contexto
- **Biblioteca de Marketing** — templates prontos pra identidade, produto, oferta, público
- **Onboarding guiado** — setup completo em uma conversa
- **Entregas no Obsidian** — tudo vira Markdown editável no seu vault
- **Pesquisa integrada** — busca web nativa + Perplexity via OpenRouter
- **Protocolo de Escrita Natural** — todo texto passa por revisão anti-IA antes da entrega
- **Status line** — acompanhe contexto, limites e modelo direto no terminal

## Comandos

| Comando | Descrição |
|---------|-----------|
| `/maestro` | Ativar o sistema (porta de entrada única) |
| `/maestro:copywriter` | Copy, headlines, páginas de vendas, emails |
| `/maestro:estrategista` | Funis, ofertas, lançamentos, diagnósticos |
| `/maestro:marca` | Identidade, posicionamento, naming, tom de voz |
| `/maestro:midias-sociais` | Conteúdo, calendário, análise, estratégia social |
| `/maestro:performance` | Diagnóstico de campanhas, testes A/B, canais |
| `/maestro:pesquisador` | Pesquisa de mercado, concorrência, audiência |
| `/maestro:entrevistador` | Conduzir entrevistas para coleta de dados |
| `/maestro:gestor-tarefas` | Consultar e gerenciar tarefas no vault |
| `/maestro:bibliotecario` | Criar e gerenciar a Biblioteca de Marketing |
| `/desligar-maestro` | Desativar o sistema no projeto atual |

## Atualização

```bash
/plugin marketplace update sistema-maestro
```

## Desinstalação

```bash
/plugin uninstall maestro
/plugin marketplace remove sistema-maestro
```

## Maestro Pro

Membros da [Comunidade dos Últimos](https://acomunidadedosultimos.com.br) têm acesso ao **Maestro Pro** — com agentes exclusivos, funcionalidades avançadas e novos recursos a cada atualização.

## Autor

**Willian Nunes** — [@eusouwillnunes](https://instagram.com/eusouwillnunes)

Criador do Sistema Maestro e da [Comunidade dos Últimos](https://acomunidadedosultimos.com.br).

---

## English

**Sistema Maestro** is a Claude Code plugin that provides a full marketing and sales team powered by AI agents. It includes specialized agents for copywriting, marketing strategy, branding, social media, and paid ads performance — all coordinated by an orchestrator agent with memory across sessions.

**Features:** 12 specialized agents, marketing library with templates, guided onboarding, Obsidian vault integration, web research, natural writing protocol, persistent memory.

**Keywords:** marketing, sales, copywriting, branding, social media, content creation, sales funnel, landing page, email marketing, digital marketing, AI marketing assistant, Claude Code plugin, marketing automation, lead generation, conversion optimization

```bash
/plugin marketplace add eusouwillnunes/sistema-maestro
```
