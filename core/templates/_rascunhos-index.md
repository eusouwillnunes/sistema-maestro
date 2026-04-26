---
tipo: index
area: rascunhos
descricao: "Painel de rascunhos do projeto"
tags:
  - "#maestro/index"
---

# Rascunhos

> [!info] Painel de rascunhos
> Atualizado automaticamente via Dataview. Rascunhos expiram 30 dias após criação. Requer plugin Dataview do Obsidian instalado e habilitado.

## Estatísticas

```dataview
TABLE length(rows) as Quantidade
FROM ""
WHERE file.folder = this.file.folder AND tipo = "rascunho"
GROUP BY status
```

## Ativos

```dataview
TABLE agente, tags-dominio as Tags, expira-em as "Expira em", origem-pedido as Pedido
FROM ""
WHERE file.folder = this.file.folder AND tipo = "rascunho" AND status = "rascunho"
SORT expira-em ASC
```

## Por tema

```dataview
TABLE length(rows) as Quantidade
FROM ""
WHERE file.folder = this.file.folder AND tipo = "rascunho" AND status = "rascunho"
FLATTEN tags-dominio AS tag
WHERE startswith(tag, "tema/")
GROUP BY tag
SORT tag ASC
```

## Exploratórios

```dataview
TABLE agente, tags-dominio as Tags, expira-em as "Expira em", origem-pedido as Pedido
FROM ""
WHERE file.folder = this.file.folder AND tipo = "rascunho" AND status = "exploratorio"
SORT expira-em ASC
```

## Promovidos (últimos 15)

```dataview
TABLE agente, tags-dominio as Tags, data as Criado
FROM ""
WHERE file.folder = this.file.folder AND tipo = "rascunho" AND status = "promovido"
SORT file.mtime DESC
LIMIT 15
```

## Arquivados (últimos 15)

```dataview
TABLE agente, tags-dominio as Tags, data as Criado
FROM ""
WHERE file.folder = this.file.folder AND tipo = "rascunho" AND status = "arquivado"
SORT file.mtime DESC
LIMIT 15
```
