---
tipo: analise-performance
pasta-destino: entregas/
naming: cronologico
descricao: Análise de performance de campanhas de tráfego pago (Meta Ads, Google Ads, etc.)
---

> Aplica: [[protocolo-biblioteca]] (seção "Wikilinks em frontmatter")

## Frontmatter do artefato

```yaml
# === 🤖 Operacional (Gerente preenche) ===
titulo: "[Título da análise]"
tipo: analise-performance
plataforma: "[Meta|Google|TikTok|LinkedIn]"
campanha: "[[campanhas/<slug>]]"         # ex: "[[campanhas/black-friday-2026]]"
periodo: "[YYYY-MM-DD a YYYY-MM-DD]"
status: em-andamento
data-criacao: "[timestamp]"
data-cancelamento: ~
motivo-cancelamento: ~
tags-dominio:
  - produto/[preencher]   # obrigatório — preencher com o produto da campanha analisada (slugify)
  - tema/[preencher]       # obrigatório — pelo menos 1 do catálogo (plugin/core/templates/catalogo-tags.md + override user)
tags:
  # OBRIGATÓRIO: espelhar todos os valores de tags-dominio aqui. Obsidian tag pane só renderiza hierarquia via este campo nativo. Manter também tags do sistema.
  - "#maestro/entrega"
  - analise-performance

# === ✍️ Criativo (Especialista preenche) ===
# (nenhum — análise tem frontmatter 100% operacional; valores das métricas e recomendações ficam no corpo)
```

## Seções-base

> [!info] 🤖 Casca operacional (Gerente preenche)
> Gerente preenche apenas o frontmatter operacional acima. Não tocar no corpo abaixo.

# [Título]

> [!note] ✍️ Conteúdo (Especialista preenche)
> Especialista entra com a casca limpa e preenche todas as seções abaixo.

## Contexto

## Métricas principais

| Métrica | Valor | Benchmark | Avaliação |
|---------|-------|-----------|-----------|
| CTR | — | — | — |
| CPC | — | — | — |
| CPA | — | — | — |
| ROAS | — | — | — |

## Análise por conjunto de anúncios

## Recomendações

## Decisões estratégicas

| Ponto | Escolha | Origem |
|---|---|---|
| [preenchido pelo especialista] | [escolha] | [Escolha do usuário \| Inferido do contexto \| Herdado do projeto \| Herdado do produto] |

> Se a tarefa não tocou nenhum ponto canônico, substitua a tabela pela frase: "Nenhuma decisão estratégica canônica nesta tarefa." O cabeçalho `## Decisões estratégicas` deve permanecer pro QA validar.

## Fontes e wiki-links
