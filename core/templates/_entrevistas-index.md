---
tipo: index
area: entrevistas
descricao: "Painel de entrevistas do projeto"
tags:
  - "#maestro/index"
---

# Entrevistas

> [!info] Painel de entrevistas
> Atualizado automaticamente via Dataview. Painel vazio é normal em projeto novo. Requer o plugin Dataview do Obsidian instalado e habilitado.

## Estatísticas

```dataview
TABLE length(rows) as Quantidade
FROM ""
WHERE file.folder = this.file.folder AND tipo = "entrevista"
GROUP BY status
```

---

## Pendentes

```dataview
TABLE agente-solicitante as Solicitante, tarefa-relacionada as "Tarefa", data-criacao as Criação
FROM ""
WHERE file.folder = this.file.folder AND tipo = "entrevista" AND status = "pendente"
SORT data-criacao DESC
```

## Em andamento

```dataview
TABLE agente-solicitante as Solicitante, tarefa-relacionada as "Tarefa", data-criacao as Criação
FROM ""
WHERE file.folder = this.file.folder AND tipo = "entrevista" AND status = "em-andamento"
SORT data-criacao DESC
```

## Concluídas (últimas 15)

```dataview
TABLE agente-solicitante as Solicitante, tarefa-relacionada as "Tarefa", data-conclusao as Conclusão
FROM ""
WHERE file.folder = this.file.folder AND tipo = "entrevista" AND status = "concluida"
SORT data-conclusao DESC
LIMIT 15
```

## Canceladas (últimas 15)

```dataview
TABLE agente-solicitante as Solicitante, tarefa-relacionada as "Tarefa", motivo-cancelamento as Motivo, data-cancelamento as Cancelamento
FROM ""
WHERE file.folder = this.file.folder AND tipo = "entrevista" AND status = "cancelada"
SORT data-cancelamento DESC
LIMIT 15
```
