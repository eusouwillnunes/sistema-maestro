---
titulo: Cascatas em andamento
tipo: index
area: cascatas
tags:
  - "#maestro/cascata"
---

> [!info] Cascatas de cadastro
> Mostra tarefas bloqueadas por entrevistas pendentes. Cada cascata = 1 tarefa pai + N entrevistas filhas geradas pelo Fluxo 10 v2 do Gerente quando o usuário escolhe "preencher" ou "só críticas" no `fluxo-needs.md`.

```dataview
TABLE WITHOUT ID
  link(rows[0].tarefa-relacionada) as "Tarefa pai",
  length(rows) as "Total entrevistas",
  length(filter(rows, (r) => r.status = "concluida")) as "Concluídas",
  length(filter(rows, (r) => r.status = "pendente")) as "Pendentes"
FROM ""
WHERE file.folder = this.file.folder
  AND parte-de-cascata = true
  AND tarefa-relacionada
GROUP BY tarefa-relacionada
SORT length(filter(rows, (r) => r.status = "pendente")) DESC
```

> [!tip] Próximas entrevistas pendentes
> Lista granular pra retomar cascatas de onde parou.

```dataview
TABLE WITHOUT ID
  file.link as "Entrevista",
  link(tarefa-relacionada) as "Tarefa pai",
  template-destino as "Template",
  status as "Status"
FROM ""
WHERE file.folder = this.file.folder
  AND parte-de-cascata = true
  AND status = "pendente"
SORT tarefa-relacionada ASC
```
