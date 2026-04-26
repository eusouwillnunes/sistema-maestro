---
tipo: lancamento
pasta-destino: lancamentos/
naming: conceitual
estrutura: pasta-conceitual
descricao: Lançamento de produto (Semente, Rápido com Live, Meteórico)
---

> Aplica: [[protocolo-biblioteca]] (seção "Wikilinks em frontmatter")

## Frontmatter do artefato

```yaml
# === 🤖 Operacional (Gerente preenche) ===
titulo: "[Nome do lançamento]"
tipo: lancamento
produto: "[[produtos/<slug>]]"           # ex: "[[produtos/curso-completo]]"
status: em-andamento
data-criacao: "[timestamp]"
data-cancelamento: ~
motivo-cancelamento: ~
tags-dominio:
  - produto/[preencher]   # obrigatório — deriva de produto: via slugify (lowercase + espaços→hífen + sem acentos)
  - tema/[preencher]       # obrigatório — pelo menos 1 do catálogo (plugin/core/templates/catalogo-tags.md + override user)
tags:
  # OBRIGATÓRIO: espelhar todos os valores de tags-dominio aqui. Obsidian tag pane só renderiza hierarquia via este campo nativo. Manter também tags do sistema.
  - "#maestro/entrega"
  - lancamento

# === ✍️ Criativo (Especialista preenche) ===
modelo: ~                             # semente | rapido | meteorico — decisão estratégica do Estrategista
data-prevista: ~                      # YYYY-MM-DD — decisão estratégica de cronograma
```

## Seções-base

> [!info] 🤖 Casca operacional (Gerente preenche)
> Gerente preenche apenas o frontmatter operacional acima. Não tocar no corpo abaixo.

# [Título]

> [!note] ✍️ Conteúdo (Especialista preenche)
> Especialista entra com a casca limpa e preenche todas as seções abaixo.

## Modelo de lançamento

## Cronograma

## Etapas (pre-lançamento, lançamento, carrinho aberto, pós)

## Peças necessárias

## Métricas esperadas

## Decisões estratégicas

| Ponto | Escolha | Origem |
|---|---|---|
| [preenchido pelo especialista] | [escolha] | [Escolha do usuário \| Inferido do contexto \| Herdado do projeto \| Herdado do produto] |

> Se a tarefa não tocou nenhum ponto canônico, substitua a tabela pela frase: "Nenhuma decisão estratégica canônica nesta tarefa." O cabeçalho `## Decisões estratégicas` deve permanecer pro QA validar.

## Fontes e wiki-links
