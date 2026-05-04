---
tipo: painel-workspace
escopo: index
projetos:
  - {projeto-slug-1}
  - {projeto-slug-2}
versao-template: 1
---

> [!warning] Painel não está renderizando?
> Significa que falta ativar o plugin **Dataview** no Obsidian. Vá em Configurações → Plugins da Comunidade → Dataview → ligue.

# Projetos da Área de Trabalho

Este painel lista todos os projetos da workspace ordenados por última atividade. Clique no nome pra ir direto ao projeto. Atualiza sozinho — não precisa editar.

```dataview
TABLE WITHOUT ID
  link(key + "/" + key + ".md", key) AS "Projeto",
  max(rows.file.mtime) AS "Última atividade",
  length(filter(rows, (r) => contains(r.file.folder, "/tarefas") AND r.status = "em-progresso")) AS "Tarefas em progresso"
FROM "{projeto-slug-1}" OR "{projeto-slug-2}"
GROUP BY regexreplace(file.folder, "/.*", "")
SORT max(rows.file.mtime) DESC
```
