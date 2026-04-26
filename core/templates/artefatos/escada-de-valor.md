---
tipo: escada-de-valor
pasta-destino: escada-de-valor/
naming: conceitual
estrutura: pasta-conceitual
descricao: Escada de Valor — sequência de produtos em ordem de ascensão
---

> Aplica: [[protocolo-biblioteca]] (seção "Wikilinks em frontmatter")

## Frontmatter do artefato

```yaml
# === 🤖 Operacional (Gerente preenche) ===
titulo: "[Nome da escada]"
tipo: escada-de-valor
produto: "[[produtos/<slug>]]"           # produto principal da escada (ex: "[[produtos/curso-completo]]")
status: em-andamento
data-criacao: "[timestamp]"
data-cancelamento: ~
motivo-cancelamento: ~
tags-dominio:
  - produto/[preencher]   # obrigatório — preencher com o produto principal da escada (slugify do nome)
  - tema/[preencher]       # obrigatório — pelo menos 1 do catálogo (plugin/core/templates/catalogo-tags.md + override user)
tags:
  # OBRIGATÓRIO: espelhar todos os valores de tags-dominio aqui. Obsidian tag pane só renderiza hierarquia via este campo nativo. Manter também tags do sistema.
  - "#maestro/entrega"
  - escada-de-valor

# === ✍️ Criativo (Especialista preenche) ===
# (nenhum — escada-de-valor tem frontmatter 100% operacional; toda decisão criativa fica no corpo)
```

## Seções-base

> [!info] 🤖 Casca operacional (Gerente preenche)
> Gerente preenche apenas o frontmatter operacional acima. Não tocar no corpo abaixo.

# [Título]

> [!note] ✍️ Conteúdo (Especialista preenche)
> Especialista entra com a casca limpa e preenche todas as seções abaixo.

## Visão geral

## Degraus

### 1. Isca (gratuita)

### 2. Entrada (baixo ticket)

### 3. Core

### 4. Premium

## Jornada entre degraus

## Decisões estratégicas

| Ponto | Escolha | Origem |
|---|---|---|
| [preenchido pelo especialista] | [escolha] | [Escolha do usuário \| Inferido do contexto \| Herdado do projeto \| Herdado do produto] |

> Se a tarefa não tocou nenhum ponto canônico, substitua a tabela pela frase: "Nenhuma decisão estratégica canônica nesta tarefa." O cabeçalho `## Decisões estratégicas` deve permanecer pro QA validar.

## Fontes e wiki-links
