---
tipo: index
area: campanhas
descricao: "Painel de campanhas do projeto"
tags:
  - "#maestro/index"
---

# Campanhas

> [!info] Painel de campanhas
> Atualizado automaticamente via Dataview. Tipos: flash sale, data comemorativa, remarketing, reativação, indicação, teste. Requer o plugin Dataview do Obsidian instalado e habilitado.

## Estatísticas

```dataview
TABLE length(rows) as Quantidade
FROM ""
WHERE file.folder = this.file.folder AND tipo = "campanha"
GROUP BY status
```

## Em andamento

```dataview
TABLE produto, periodo as Período
FROM ""
WHERE file.folder = this.file.folder AND tipo = "campanha" AND status = "em-andamento"
SORT data-criacao DESC
```

## Concluídas (últimas 15)

```dataview
TABLE produto, periodo as Período, data-conclusao as Conclusão
FROM ""
WHERE file.folder = this.file.folder AND tipo = "campanha" AND status = "concluida"
SORT data-conclusao DESC
LIMIT 15
```

## Canceladas (últimas 15)

```dataview
TABLE produto, motivo-cancelamento as Motivo, data-cancelamento as Cancelamento
FROM ""
WHERE file.folder = this.file.folder AND tipo = "campanha" AND status = "cancelada"
SORT data-cancelamento DESC
LIMIT 15
```
