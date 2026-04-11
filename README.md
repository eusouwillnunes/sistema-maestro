# Sistema Maestro

Uma equipe completa de agentes especialistas em marketing e vendas, coordenados por IA. Instale no Claude Code e tenha acesso a copywriters, estrategistas, especialistas em marca, mídias sociais, performance e mais — todos trabalhando juntos num sistema integrado.

## Instalação

```bash
/plugin marketplace add eusouwillnunes/sistema-maestro
/plugin install maestro@sistema-maestro
```

Pronto. Na próxima mensagem, o Maestro vai se apresentar e configurar o sistema no seu projeto.

## O que inclui

### Agentes Especialistas

| Agente | O que faz |
|--------|-----------|
| **Maestro** | Orquestrador central — recebe seus pedidos, decompõe em tarefas e delega pro especialista certo |
| **Copywriter** | Textos persuasivos: headlines, páginas de vendas, emails, scripts (Eugene Schwartz) |
| **Estrategista** | Funis, ofertas, lançamentos, diagnósticos de negócio (Russell Brunson + Alex Hormozi) |
| **Marca** | Identidade, posicionamento, naming, tom de voz (Simon Sinek + Marty Neumeier) |
| **Mídias Sociais** | Conteúdo, calendário, análise, estratégia social (Gary Vee + Brendan Kane) |
| **Performance** | Diagnóstico de campanhas pagas, testes A/B, canais de tráfego (Perry Marshall) |

### Agentes Operacionais

| Agente | O que faz |
|--------|-----------|
| **Pesquisador** | Pesquisa de mercado, concorrência e audiência com fontes verificáveis |
| **Entrevistador** | Coleta dados do seu negócio via conversa guiada, uma pergunta por vez |
| **Gestor de Tarefas** | Cria e acompanha tarefas e entrevistas no vault Obsidian |
| **Bibliotecário** | Cria e gerencia sua Biblioteca de Marketing (contexto reutilizável) |
| **QA** | Verificação automática de checklists antes da entrega |
| **Revisor** | Garante que todo texto soe natural e humano (Protocolo de Escrita Natural) |

## Como usar

Basta pedir. O Maestro entende o que você precisa e delega pro agente certo:

- "Cria uma headline pro meu curso" → Copywriter
- "Monta um funil de vendas" → Estrategista
- "Define o posicionamento da minha marca" → Marca
- "Faz um calendário de conteúdo pro Instagram" → Mídias Sociais
- "Analisa minha campanha no Meta Ads" → Performance
- "Preenche a identidade da marca" → Maestro decompõe em tarefas e executa
- "Pesquisa meus concorrentes" → Pesquisador

Você também pode chamar qualquer agente diretamente:

## Comandos disponíveis

| Comando | O que faz |
|---------|-----------|
| `/maestro:maestro` | Orquestrador — roteia tarefas pro agente certo |
| `/maestro:copywriter` | Copy, headlines, páginas de vendas, emails |
| `/maestro:estrategista` | Funis, ofertas, lançamentos, diagnósticos |
| `/maestro:marca` | Identidade, posicionamento, naming, tom de voz |
| `/maestro:midias-sociais` | Conteúdo, calendário, análise, estratégia social |
| `/maestro:performance` | Diagnóstico de campanhas, testes A/B, canais |
| `/maestro:pesquisador` | Pesquisa de mercado, concorrência, audiência |
| `/maestro:entrevistador` | Conduzir entrevistas para coleta de dados |
| `/maestro:gestor-tarefas` | Consultar e gerenciar tarefas no vault |
| `/maestro:bibliotecario` | Criar e gerenciar a Biblioteca de Marketing |
| `/maestro` | Ativar o Sistema Maestro |
| `/desligar-maestro` | Desativar o Sistema Maestro |
| `/maestro:maestro-onboarding` | Reconfigurar o Sistema Maestro |
| `/maestro:maestro-revisar-memorias` | Revisar e evoluir memórias do sistema |

## Como o Maestro trabalha

O sistema decide automaticamente a melhor forma de executar cada tarefa:

- **Pedidos simples** ("cria uma headline") → delega direto pro agente especialista
- **Pedidos complexos** ("preenche a identidade") → decompõe em tarefas com dependências, executa em sequência
- **Quando faltam dados** → cria entrevistas e aciona o Entrevistador pra coletar do usuário
- **Quando precisa de pesquisa** → despacha o Pesquisador em paralelo enquanto conduz a entrevista

Tudo fica registrado no vault Obsidian: tarefas, entrevistas, pesquisas, entregas. Você acompanha o progresso e retoma de onde parou.

## Primeiros passos

Na primeira ativação, o Maestro vai:

1. **Criar sua Biblioteca de Marketing** — estrutura organizada onde ficam todas as informações do seu negócio (identidade, produtos, referências)
2. **Configurar memórias** — sistema que aprende suas preferências ao longo do tempo
3. **Perguntar sobre seu negócio** — pra começar a preencher o contexto

A partir daí, toda vez que você pedir algo, o sistema já sabe quem você é, qual sua marca, seus produtos e seu público.

## Atualização

```bash
/plugin marketplace update sistema-maestro
```

## Desinstalação

```bash
/plugin uninstall maestro
/plugin marketplace remove sistema-maestro
```

## Autor

**Willian Nunes** — [@eusouwillnunes](https://instagram.com/eusouwillnunes)

Criador do Sistema Maestro e da [Comunidade dos Últimos](https://acomunidadedosultimos.com.br).
