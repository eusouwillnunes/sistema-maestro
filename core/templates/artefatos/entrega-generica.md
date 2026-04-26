---
tipo: entrega-generica
pasta-destino: entregas/
naming: cronologico
descricao: Fallback universal para entregas que não se encaixam em outro padrão
---

## Frontmatter do artefato

```yaml
# === 🤖 Operacional (Gerente preenche) ===
titulo: "[Título]"
tipo: entrega-generica
agente: "[agente]"
status: em-andamento
data-criacao: "[timestamp]"
data-cancelamento: ~
motivo-cancelamento: ~
tags-dominio:
  - tema/[preencher]       # obrigatório — pelo menos 1 do catálogo (plugin/core/templates/catalogo-tags.md + override user)
  # produto/<slug> é opcional pra este tipo — adicionar se aplicável
tags:
  # OBRIGATÓRIO: espelhar todos os valores de tags-dominio aqui. Obsidian tag pane só renderiza hierarquia via este campo nativo. Manter também tags do sistema.
  - "#maestro/entrega"
  # - tema/[mesmo valor de tags-dominio]
  # - produto/[mesmo valor de tags-dominio]

# === ✍️ Criativo (Especialista preenche) ===
# (nenhum — entrega-generica tem frontmatter 100% operacional; agente vem do contexto da tarefa)
```

## Seções-base

> [!info] 🤖 Casca operacional (Gerente preenche)
> Gerente preenche apenas o frontmatter operacional acima. Não tocar no corpo abaixo.

# [Título]

> [!note] ✍️ Conteúdo (Especialista preenche)
> Especialista entra com a casca limpa e preenche todas as seções abaixo.

## Contexto

## Resultado

## Decisões estratégicas

| Ponto | Escolha | Origem |
|---|---|---|
| [preenchido pelo especialista] | [escolha] | [Escolha do usuário \| Inferido do contexto \| Herdado do projeto \| Herdado do produto] |

> Se a tarefa não tocou nenhum ponto canônico, substitua a tabela pela frase: "Nenhuma decisão estratégica canônica nesta tarefa." O cabeçalho `## Decisões estratégicas` deve permanecer pro QA validar.

## Fontes e wiki-links
