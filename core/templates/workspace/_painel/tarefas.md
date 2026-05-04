---
tipo: painel-workspace
escopo: tarefas
projetos:
  - {projeto-slug-1}
  - {projeto-slug-2}
versao-template: 1
---

> [!warning] Painel não está renderizando?
> Significa que falta ativar o plugin **Dataview** no Obsidian. Vá em Configurações → Plugins da Comunidade → Dataview → ligue. Se não aparecer Dataview na lista, instale primeiro (botão Browse).

# Tarefas — todos os projetos

Este painel lista todas as tarefas em aberto dos seus projetos da workspace. Atualiza sozinho quando você cria, conclui ou cancela tarefas — não precisa editar.

```dataview
TABLE WITHOUT ID
  file.link AS "Tarefa",
  projeto AS "Projeto",
  status AS "Status",
  categoria AS "Categoria",
  data-criada AS "Criada"
FROM "{projeto-slug-1}/tarefas" OR "{projeto-slug-2}/tarefas"
WHERE status != "concluida" AND status != "cancelada"
SORT data-criada DESC
```
