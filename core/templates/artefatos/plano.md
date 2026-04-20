---
tipo: plano
pasta-destino: planos/
naming: cronologico
descricao: Plano agregador de tarefas relacionadas. Cobre plano normal (campo corrige vazio) e plano de correção (campo corrige preenchido apontando pro plano original).
---

## Frontmatter do artefato

```yaml
titulo: "[Título do plano]"
tipo: plano
status: rascunho                      # rascunho | aprovado | em-execucao | aguardando-validacao | concluido | rejeitado
                                      # 'cancelado' é reservado para spec futuro (item 4 do Grupo 3) — não use ainda
grupo: "[slug-do-grupo]"
solicitante: "[nome]"
data-criacao: "[timestamp ISO 8601]"
data-aprovacao: ~
data-conclusao: ~
corrige: ~                            # wiki-link do plano original quando é correção; ~ em plano normal
correcoes: []                         # lista de wiki-links de planos de correção vinculados
tags:
  - "#maestro/plano"
```

## Seções-base

# [Título]

## Pedido original

[Briefing do usuário que motivou o plano]

## Raciocínio da decomposição

[Como o Gerente chegou nesta decomposição — agrupamentos, dependências, razão dos níveis]

## Tarefas

```dataview
TABLE agente, status, resultado, prioridade
FROM "tarefas"
WHERE parte-de = this.file.link
SORT data-criacao ASC
```

## Histórico de alterações

| Data | Evento | Detalhe |
|------|--------|---------|
|      |        |         |

## Feedback da validação final

[Preenchido apenas em plano de correção — contém feedback consolidado do usuário que motivou a correção]
