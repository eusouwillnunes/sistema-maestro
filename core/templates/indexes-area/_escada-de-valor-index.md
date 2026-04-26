---
tipo: index
area: escada-de-valor
descricao: "Painel de escadas de valor do projeto"
tags:
  - "#maestro/index"
---

# Escadas de Valor

> [!info] Painel de escadas de valor
> Atualizado automaticamente via Dataview. A Escada de Valor conecta lead magnets e produtos em sequência lógica de ascensão. Requer o plugin Dataview do Obsidian instalado e habilitado.

## Estatísticas

```dataview
TABLE length(rows) as Quantidade
FROM ""
WHERE file.folder = this.file.folder AND tipo = "escada-de-valor"
GROUP BY status
```

## Em andamento

```dataview
TABLE produto, data-criacao as "Criada em"
FROM ""
WHERE file.folder = this.file.folder AND tipo = "escada-de-valor" AND status = "em-andamento"
SORT data-criacao DESC
```

## Concluídas (últimas 15)

```dataview
TABLE produto, data-conclusao as Conclusão
FROM ""
WHERE file.folder = this.file.folder AND tipo = "escada-de-valor" AND status = "concluida"
SORT data-conclusao DESC
LIMIT 15
```

## Canceladas (últimas 15)

```dataview
TABLE produto, motivo-cancelamento as Motivo, data-cancelamento as Cancelamento
FROM ""
WHERE file.folder = this.file.folder AND tipo = "escada-de-valor" AND status = "cancelada"
SORT data-cancelamento DESC
LIMIT 15
```
