---
description: Mapa de contexto obrigatório e recomendado por tipo de tarefa
tags:
  - "#maestro/template"
---

# Contexto por Tarefa

> [!info] Este documento é referência de consulta para desenvolvimento e manutenção do sistema.
> Cada agente tem seu próprio Mapa de Necessidades embutido na skill. Este arquivo NÃO é lido em runtime pelos agentes.

Mapa completo de quais documentos da Biblioteca de Marketing cada tipo de tarefa utiliza. Cada agente especialista tem uma versão simplificada deste mapa na sua seção "Contexto e Biblioteca".

## Legenda

- **Obrigatório:** informação essencial para a tarefa. Se ausente na Biblioteca, o agente pergunta ao usuário.
- **Recomendado:** melhora a qualidade da entrega. Se ausente, o agente segue com seus frameworks.
- **Sem template ≠ bloqueio:** o agente nunca para por falta de template. Resolve com conhecimento próprio.

## Fontes de Contexto — Memórias

> [!note] Memórias continuam sendo carregadas pelo Maestro e passadas ao agente na delegação.
> Este é o único contexto que o Maestro pré-carrega. Templates da Biblioteca são buscados pelo próprio agente.

Além dos documentos da Biblioteca de Marketing, o sistema carrega memórias relevantes:

| Fonte | Quando carregar | Escopo |
|---|---|---|
| `user/memorias/preferencias.md` | Sempre, em toda tarefa | Usuário |
| `user/memorias/agentes/[agente].md` | Quando o agente de destino tem ajustes | Usuário |
| `maestro/memorias/contexto.md` | Quando a tarefa precisa de contexto do negócio | Projeto |
| `maestro/memorias/agentes/[agente].md` | Quando o agente tem feedbacks do projeto | Projeto |
| `maestro/memorias/sessoes.md` | Só quando o usuário perguntar sobre histórico | Projeto |
| `maestro/memorias/decisoes.md` | Quando a tarefa envolve decisões já tomadas | Projeto |

> **Regra:** indexes (`_index.md`) são SEMPRE lidos primeiro. Só depois carregar os arquivos relevantes.

---

## Tabela

| Tarefa | Agente | Contexto Obrigatório | Contexto Recomendado |
|--------|--------|---------------------|---------------------|
| Headline | Copywriter | Identidade, Dossiê, Prospect | Desejos de Massa, Nível de Consciência |
| Copy de anúncio | Copywriter | Identidade, Dossiê, Prospect | Desejos de Massa, Prova Social |
| Página de vendas | Copywriter | Identidade, Dossiê, Prospect, Oferta | Desejos, Prova Social, Big Idea |
| Script de VSL | Copywriter | Identidade, Dossiê, Prospect, Oferta | Desejos, Prova Social, Big Idea |
| Sequência de emails | Copywriter | Identidade, Dossiê, Prospect, Oferta | Funil, Lançamento |
| Bullets / fascinations | Copywriter | Dossiê, Prospect, Oferta | Desejos de Massa |
| Diagnóstico de negócio | Estrategista | Identidade, Dossiê | Mercado, Concorrência |
| Criação de oferta | Estrategista | Identidade, Dossiê, Prospect | Escada de Valor, Prova Social |
| Planejamento de funil | Estrategista | Identidade, Dossiê, Prospect | Escada de Valor, Oferta |
| Criação de lead magnet | Estrategista | Identidade, Dossiê, Prospect, Oferta | Funil, Mercado |
| Script de vendas/aquisição | Estrategista | Identidade, Dossiê, Prospect, Oferta | Objeções, Prova Social |
| Estrutura de webinário/VSL | Estrategista | Identidade, Dossiê, Prospect, Oferta | Crenças do Público, Prova Social |
| Estratégia de lançamento | Estrategista | Identidade, Dossiê, Prospect, Mercado | Escada de Valor, Funil |
| Identidade de marca | Marca | (coleta do zero ou docs existentes) | Referências de concorrência |
| Posicionamento de marca | Marca | Identidade | Mercado, Concorrência |
| Naming / nome de marca | Marca | Identidade, Posicionamento | Público, Concorrência, Arquétipo |
| Manifesto de marca | Marca | Identidade | Posicionamento, Tom de Voz |
| Tom de voz | Marca | Identidade, Personalidade | Público, Concorrência |
| Estratégia de mídias sociais | Mídias Sociais | Identidade, Dossiê, Prospect | Plataformas Ativas, Métricas |
| Criação de conteúdo viral | Mídias Sociais | Identidade, Dossiê, Prospect | Tom de Voz, Plataforma-alvo |
| Análise de performance social | Mídias Sociais | Identidade, Métricas | Conteúdos Recentes, Plataformas |
| Calendário editorial | Mídias Sociais | Identidade, Dossiê | Recursos Disponíveis, Plataformas |
| Calendário operacional | Mídias Sociais | Identidade, Dossiê | Recursos Disponíveis, Plataformas, Arquivo Morto |
| Repurposing de conteúdo | Mídias Sociais | Identidade, Pillar Content | Plataformas-alvo |
| Diagnóstico de campanha paga | Performance | Identidade, Métricas | Plataforma, Período, Metas |
| Planejamento de testes A/B | Performance | Identidade, Métricas | Campanhas Ativas, Budget |
| Seleção de canais de tráfego | Performance | Identidade, Dossiê | Público, Modelo de Negócio, Budget |
| Otimização de budget | Performance | Métricas | Canais Ativos, Budget Total |
| Revisão de texto | Revisor | Identidade (tom de voz) | Tom de Voz, Elementos Verbais |
| Pesquisa de mercado | Pesquisador | Identidade, Dossiê | Mercado, Concorrência |
| Análise de concorrentes | Pesquisador | Identidade, Dossiê | Mercado, Posicionamento |
| Mapeamento de audiência | Pesquisador | Identidade, Dossiê, Prospect | Mercado |
| Pesquisa de referências | Pesquisador | Identidade | Mercado, Concorrência |
| Pesquisa livre | Pesquisador | (objetivo definido pelo usuário) | — |
| Criar biblioteca de marketing | Bibliotecário | (nome do projeto) | — |
| Status da biblioteca | Bibliotecário | (biblioteca existente) | — |
| Importar material existente | Bibliotecário | (material do usuário) | — |
