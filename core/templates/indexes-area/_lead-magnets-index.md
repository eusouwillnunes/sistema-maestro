---
tipo: index
area: lead-magnets
descricao: "Painel de lead magnets do projeto"
tags:
  - "#maestro/index"
---

# Lead Magnets

> [!info] Painel de lead magnets
> Atualizado automaticamente via Dataview. Formatos: ebook, checklist, video, template, mini-curso. Requer o plugin Dataview do Obsidian instalado e habilitado.

## Estatísticas

```dataview
TABLE length(rows) as Quantidade
FROM ""
WHERE file.folder = this.file.folder AND tipo = "lead-magnet"
GROUP BY status
```

## Em andamento

```dataview
TABLE produto-destino as "Produto destino", formato
FROM ""
WHERE file.folder = this.file.folder AND tipo = "lead-magnet" AND status = "em-andamento"
SORT data-criacao DESC
```

## Concluídos (últimos 15)

```dataview
TABLE produto-destino as "Produto destino", formato, data-conclusao as Conclusão
FROM ""
WHERE file.folder = this.file.folder AND tipo = "lead-magnet" AND status = "concluida"
SORT data-conclusao DESC
LIMIT 15
```

## Cancelados (últimos 15)

```dataview
TABLE produto-destino as "Produto destino", motivo-cancelamento as Motivo, data-cancelamento as Cancelamento
FROM ""
WHERE file.folder = this.file.folder AND tipo = "lead-magnet" AND status = "cancelada"
SORT data-cancelamento DESC
LIMIT 15
```
