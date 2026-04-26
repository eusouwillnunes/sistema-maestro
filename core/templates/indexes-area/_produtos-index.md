---
tipo: index
area: produtos
descricao: "Painel de produtos do projeto (agrupado por pasta-conceitual)"
tags:
  - "#maestro/index"
---

# Produtos

> [!info] Painel de produtos
> Atualizado automaticamente via Dataview. Cada produto vive em uma pasta com 8 sub-templates de preenchimento (dossiê, oferta, análise de mercado, etc.). O painel agrega cada pasta numa linha, mostrando quantos sub-templates estão preenchidos. Requer o plugin Dataview do Obsidian instalado e habilitado.

## Estatísticas

```dataview
TABLE length(rows) as Pastas
FROM ""
WHERE startswith(file.folder, this.file.folder) AND file.folder != this.file.folder AND tipo = "produto"
GROUP BY file.folder
```

## Produtos

```dataview
TABLE WITHOUT ID
  rows.file.link[0] as Documento,
  split(rows.file.folder[0], "/")[length(split(rows.file.folder[0], "/")) - 1] as Pasta,
  rows.produto[0] as Nome,
  length(filter(rows, (r) => r.status = "preenchido")) + "/" + length(rows) as Preenchidos
FROM ""
WHERE startswith(file.folder, this.file.folder) AND file.folder != this.file.folder AND tipo = "produto"
GROUP BY file.folder
SORT length(rows) DESC
```
