---
tipo: tarefa
pasta-destino: tarefas/
naming: cronologico
descricao: Tarefa do fluxo de execução do Maestro (registro de trabalho, não entrega final)
---

> Aplica: [[protocolo-biblioteca]] (seção "Wikilinks em frontmatter")

## Frontmatter do artefato

```yaml
titulo: "[Título da tarefa]"
tipo: tarefa
agente: "[agente destino]"
categoria: "[identidade|copy|estrategia|midias|performance|pesquisa|biblioteca|revisao|validacao-plano|geral]"
status: em-andamento
bloqueada-por: []                          # quando preenchido: lista de "[[tarefas/<slug>]]"
grupo: "[grupo]"
prioridade: media
solicitante: "[nome]"
parte-de: ~                                # ~ em tarefa atômica; "[[planos/<slug>]]" em tarefa de plano
adicionada-em: ~
data-criacao: "[timestamp]"
data-inicio: "[timestamp]"
data-conclusao: ~
data-cancelamento: ~
motivo-cancelamento: ~
resultado: "[[<pasta-destino>/<slug>]]"    # ex: "[[campanhas/campanha-x]]", "[[funis/funil-y]]" — pasta varia conforme tipo do artefato gerado
tags:
  - "#maestro/tarefa"
```

## Seções-base

# [Título]

## Descrição

[Briefing que o especialista vai ler]

## Sub-tarefas

[Preenchido pelo especialista no início da execução]

## Validações

[Fixo por categoria — carregado pelo Gerente]

## Dependências

- **Bloqueada por:** nenhuma
- **Bloqueia:** nenhuma
