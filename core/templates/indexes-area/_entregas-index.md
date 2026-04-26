---
tipo: index
area: entregas
descricao: "Painel de entregas do projeto"
tags:
  - "#maestro/index"
---

# Entregas

> [!info] Painel de entregas
> Atualizado automaticamente via Dataview. Lista entregas avulsas (entrega-generica) e análises de performance (analise-performance). Requer o plugin Dataview do Obsidian instalado e habilitado.

## Estatísticas

```dataview
TABLE length(rows) as Quantidade
FROM ""
WHERE file.folder = this.file.folder AND (tipo = "entrega-generica" OR tipo = "analise-performance")
GROUP BY status
```

## Em andamento

```dataview
TABLE tipo, agente, data-criacao as "Criado em"
FROM ""
WHERE file.folder = this.file.folder AND (tipo = "entrega-generica" OR tipo = "analise-performance") AND status = "em-andamento"
SORT data-criacao DESC
```

## Concluídas (últimas 15)

```dataview
TABLE tipo, agente, data-conclusao as Conclusão
FROM ""
WHERE file.folder = this.file.folder AND (tipo = "entrega-generica" OR tipo = "analise-performance") AND status = "concluida"
SORT data-conclusao DESC
LIMIT 15
```

## Canceladas (últimas 15)

```dataview
TABLE tipo, agente, motivo-cancelamento as Motivo, data-cancelamento as Cancelamento
FROM ""
WHERE file.folder = this.file.folder AND (tipo = "entrega-generica" OR tipo = "analise-performance") AND status = "cancelada"
SORT data-cancelamento DESC
LIMIT 15
```
