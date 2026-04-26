---
tipo: index
area: funis
descricao: "Painel de funis do projeto"
tags:
  - "#maestro/index"
---

# Funis de Vendas

> [!info] Painel de funis
> Atualizado automaticamente via Dataview. Se você acabou de ativar o Maestro e este painel está vazio, é normal — ele se preenche conforme funis são criados. Requer o plugin Dataview do Obsidian instalado e habilitado.

## Estatísticas

```dataview
TABLE length(rows) as Quantidade
FROM ""
WHERE file.folder = this.file.folder AND tipo = "funil"
GROUP BY status
```

## Em andamento

```dataview
TABLE produto, data-criacao as "Criado em"
FROM ""
WHERE file.folder = this.file.folder AND tipo = "funil" AND status = "em-andamento"
SORT data-criacao DESC
```

## Concluídos (últimos 15)

```dataview
TABLE produto, data-conclusao as Conclusão
FROM ""
WHERE file.folder = this.file.folder AND tipo = "funil" AND status = "concluida"
SORT data-conclusao DESC
LIMIT 15
```

## Cancelados (últimos 15)

```dataview
TABLE produto, motivo-cancelamento as Motivo, data-cancelamento as Cancelamento
FROM ""
WHERE file.folder = this.file.folder AND tipo = "funil" AND status = "cancelada"
SORT data-cancelamento DESC
LIMIT 15
```
