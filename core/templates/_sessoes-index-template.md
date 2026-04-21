---
description: Template para o índice _sessoes.md de visualização Dataview
tags:
  - "#maestro/template"
---

# Template do Índice de Sessões

Template usado pelo `/tchau-maestro` na primeira sessão de cada projeto. Criado uma única vez em `{projeto}/memorias/sessoes/_sessoes.md`. Depois, regenerado automaticamente pelo Obsidian via Dataview.

## Nome do arquivo
Sempre `_sessoes.md` (com underscore pra ficar no topo da pasta no file explorer).

## Conteúdo

````markdown
---
tipo: index
area: sessoes
---

# Sessões

## Últimas 10 sessões

```dataview
TABLE data, hora, foco, parou-em
FROM "memorias/sessoes"
WHERE tipo = "sessao"
SORT data DESC, hora DESC
LIMIT 10
```

## Tarefas concluídas por data (últimos 10 dias)

```dataview
TABLE length(rows) as "Tarefas", list(rows.file.link) as "Links"
FROM "tarefas"
WHERE status = "concluida" AND data-conclusao
GROUP BY dateformat(data-conclusao, "yyyy-MM-dd") as Data
SORT Data DESC
LIMIT 10
```

## Estatísticas mensais (tarefas por agente)

```dataview
TABLE length(rows) as "Tarefas"
FROM "tarefas"
WHERE status = "concluida" AND data-conclusao
GROUP BY dateformat(data-conclusao, "yyyy-MM") as Mês, agente
SORT Mês DESC
```
````

## Princípios

### Por que Dataview no corpo (não contadores no frontmatter da sessão)
Aprendizado do Grupo 3 em `CLAUDE.md`: "Dataview no corpo > contadores no frontmatter. Evita desincronização quando o registro teria que atualizar N campos a cada conclusão."

Se o usuário editar uma tarefa retroativamente (marcar como concluída depois de fechar a sessão), as queries Dataview refletem a realidade automaticamente. Contadores no frontmatter ficariam errados sem mecanismo de reconciliação.

### Por que a primeira query lê de `memorias/sessoes`
Metadados da sessão (`foco`, `parou-em`) vivem no frontmatter do arquivo da sessão. Essa informação não está em outro lugar — só a sessão sabe.

### Por que as outras duas queries leem de `tarefas`
Dados reais (quais tarefas concluíram, por qual agente, em que data) vivem nos arquivos de tarefa. A sessão **não registra** esses contadores — ela apenas lista os links.

## Onde mora

`{projeto}/memorias/sessoes/_sessoes.md`

## Quando é criado

Pelo `/tchau-maestro`, na primeira sessão do projeto (quando `sessoes/` ainda não existe). Cria a pasta e o `_sessoes.md` antes de gravar o primeiro arquivo de sessão.

## Manutenção

Zero. O Obsidian regenera as queries a cada render. O `tchau-maestro` nunca reescreve o `_sessoes.md` após criação.
