---
tipo: index
area: tarefas
descricao: "Painel de gestão de tarefas do projeto"
tags:
  - "#maestro/index"
---

# Tarefas

> [!info] Painel de tarefas
> Atualizado automaticamente via Dataview. Se você acabou de ativar o Maestro e este painel está vazio, é normal — ele se preenche conforme o Gerente cria tarefas. Requer o plugin Dataview do Obsidian instalado e habilitado.

## Estatísticas

```dataview
TABLE length(rows) as Quantidade
FROM ""
WHERE file.folder = this.file.folder AND tipo = "tarefa"
GROUP BY status
```

### Por agente

```dataview
TABLE length(rows) as Total,
      length(filter(rows, (r) => r.status = "concluida")) as Concluídas,
      length(filter(rows, (r) => r.status = "pendente")) as Pendentes,
      length(filter(rows, (r) => r.status = "bloqueada")) as Bloqueadas,
      length(filter(rows, (r) => r.status = "cancelada")) as Canceladas
FROM ""
WHERE file.folder = this.file.folder AND tipo = "tarefa"
GROUP BY agente
```

### Por solicitante

```dataview
TABLE length(rows) as Total,
      length(filter(rows, (r) => r.status = "concluida")) as Concluídas,
      length(filter(rows, (r) => r.status = "em-andamento")) as "Em andamento",
      length(filter(rows, (r) => r.status = "cancelada")) as Canceladas
FROM ""
WHERE file.folder = this.file.folder AND tipo = "tarefa"
GROUP BY solicitante
```

---

## Em Andamento

```dataview
TABLE agente, solicitante, parte-de as Plano, resultado as Resultado, data-inicio as Início
FROM ""
WHERE file.folder = this.file.folder AND tipo = "tarefa" AND status = "em-andamento"
SORT data-inicio DESC
```

## Pendentes

```dataview
TABLE agente, solicitante, parte-de as Plano, resultado as Resultado, prioridade, data-criacao as Criação
FROM ""
WHERE file.folder = this.file.folder AND tipo = "tarefa" AND status = "pendente"
SORT prioridade ASC, data-criacao DESC
```

## Bloqueadas

```dataview
TABLE agente, bloqueada-por as "Bloqueada por", solicitante, parte-de as Plano
FROM ""
WHERE file.folder = this.file.folder AND tipo = "tarefa" AND status = "bloqueada"
```

## Concluídas (últimas 15)

```dataview
TABLE agente, solicitante, parte-de as Plano, resultado as Resultado, data-conclusao as Conclusão, choice(concluido-por = "sistema", "🤖 sistema", choice(concluido-por = "manual", "✋ manual", "— desconhecido")) as Origem
FROM ""
WHERE file.folder = this.file.folder AND tipo = "tarefa" AND status = "concluida"
SORT data-conclusao DESC
LIMIT 15
```

## Canceladas (últimas 15)

```dataview
TABLE agente, solicitante, parte-de as Plano, motivo-cancelamento as Motivo, data-cancelamento as Cancelamento, choice(concluido-por = "sistema", "🤖 sistema", choice(concluido-por = "manual", "✋ manual", "— desconhecido")) as Origem
FROM ""
WHERE file.folder = this.file.folder AND tipo = "tarefa" AND status = "cancelada"
SORT data-cancelamento DESC
LIMIT 15
```
