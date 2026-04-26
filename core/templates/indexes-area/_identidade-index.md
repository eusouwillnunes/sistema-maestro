---
tipo: index
area: identidade
descricao: "Painel de identidade da marca"
tags:
  - "#maestro/index"
---

# Identidade da Marca

> [!info] Fundação
> A identidade é a base de tudo. Sem ela, nenhum agente consegue trabalhar com precisão.
> Comece pelo Círculo Dourado — é o ponto de partida.

## Camada 1 — Obrigatórios

```dataview
TABLE WITHOUT ID
  file.link as Documento,
  choice(status = "preenchido", "✅ preenchido", choice(status = "vazio", "⚪ vazio", "❓ sem status")) as Status
FROM ""
WHERE file.folder = this.file.folder AND tipo = "identidade" AND camada = 1
SORT file.name ASC
```

## Camada 3 — Enriquecimento

```dataview
TABLE WITHOUT ID
  file.link as Documento,
  choice(status = "preenchido", "✅ preenchido", choice(status = "vazio", "⚪ vazio", "❓ sem status")) as Status
FROM ""
WHERE file.folder = this.file.folder AND tipo = "identidade" AND camada = 3
SORT file.name ASC
```
