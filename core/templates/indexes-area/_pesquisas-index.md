---
tipo: index
area: pesquisas
descricao: "Painel de pesquisas do projeto"
tags:
  - "#maestro/index"
---

# Pesquisas

> [!info] Painel de pesquisas
> Atualizado automaticamente via Dataview. Tipos: mercado, concorrente, audiência, referência, livre. Requer o plugin Dataview do Obsidian instalado e habilitado.

## Estatísticas

```dataview
TABLE length(rows) as Quantidade
FROM ""
WHERE file.folder = this.file.folder AND contains(tags, "#maestro/pesquisa")
GROUP BY status
```

## Atuais

```dataview
TABLE tipo as Subtipo, ferramenta, data
FROM ""
WHERE file.folder = this.file.folder AND contains(tags, "#maestro/pesquisa") AND status = "atual"
SORT data DESC
```

## Canceladas (últimas 15)

```dataview
TABLE tipo as Subtipo, ferramenta, motivo-cancelamento as Motivo, data-cancelamento as Cancelamento
FROM ""
WHERE file.folder = this.file.folder AND contains(tags, "#maestro/pesquisa") AND status = "cancelada"
SORT data-cancelamento DESC
LIMIT 15
```
