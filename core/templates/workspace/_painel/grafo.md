---
tipo: painel-workspace
escopo: grafo
projetos:
  - {projeto-slug-1}
  - {projeto-slug-2}
versao-template: 1
---

> [!warning] Painel não está renderizando?
> Significa que falta ativar o plugin **Dataview** no Obsidian.

# Mapa de relações entre projetos

Aqui aparecem tags que se repetem entre seus projetos. Útil pra descobrir oportunidades cross-cliente — temas que conectam vários projetos viram pauta de conteúdo, framework reutilizável, oferta agrupada.

```dataview
TABLE WITHOUT ID
  key AS "Tag",
  length(rows) AS "Aparições",
  rows.projeto AS "Projetos"
FROM "{projeto-slug-1}" OR "{projeto-slug-2}"
WHERE tags
FLATTEN tags AS tag
GROUP BY tag
SORT length(rows) DESC
```
