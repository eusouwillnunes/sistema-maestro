---
tipo: index
area: lancamentos
descricao: "Painel de lançamentos do projeto"
tags:
  - "#maestro/index"
---

# Lançamentos

> [!info] Painel de lançamentos
> Atualizado automaticamente via Dataview. Tipos disponíveis: Semente, Rápido (com Live), Meteórico. Requer o plugin Dataview do Obsidian instalado e habilitado.

## Estatísticas

```dataview
TABLE length(rows) as Quantidade
FROM ""
WHERE file.folder = this.file.folder AND tipo = "lancamento"
GROUP BY status
```

## Em andamento

```dataview
TABLE produto, modelo, data-prevista as "Data prevista"
FROM ""
WHERE file.folder = this.file.folder AND tipo = "lancamento" AND status = "em-andamento"
SORT data-prevista ASC
```

## Concluídos (últimos 15)

```dataview
TABLE produto, modelo, data-prevista, data-conclusao as Conclusão
FROM ""
WHERE file.folder = this.file.folder AND tipo = "lancamento" AND status = "concluida"
SORT data-conclusao DESC
LIMIT 15
```

## Cancelados (últimos 15)

```dataview
TABLE produto, modelo, motivo-cancelamento as Motivo, data-cancelamento as Cancelamento
FROM ""
WHERE file.folder = this.file.folder AND tipo = "lancamento" AND status = "cancelada"
SORT data-cancelamento DESC
LIMIT 15
```
