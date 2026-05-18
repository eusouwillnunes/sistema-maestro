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
  choice(status = "entregue", "🔄 Aguardando você", choice(status = "concluido", "✅ Aprovado", choice(status = "em-revisao", "🔍 Em revisão", choice(status = "reprovado", "❌ Reprovado", choice(status = "em-andamento", "⚙️ Em andamento", choice(status = "bloqueado", "🚫 Bloqueado", choice(status = "pendente", "⏳ Pendente", status))))))) AS "Status",
  categoria AS "Categoria",
  data-criada AS "Criada"
FROM "{projeto-slug-1}/tarefas" OR "{projeto-slug-2}/tarefas"
WHERE status != "concluido" AND status != "cancelado" AND status != "entregue"
SORT data-criada DESC
```

## Entregues — aguardando seu feedback

Tarefas que o sistema fechou e estão esperando você revisar via `/feedback`. Se essa lista tá grande, vale abrir uma sessão de feedback agora.

```dataview
TABLE WITHOUT ID
  file.link AS "Tarefa",
  projeto AS "Projeto",
  resultado AS "Artefato",
  data-entregue AS "Entregue em"
FROM "{projeto-slug-1}/tarefas" OR "{projeto-slug-2}/tarefas"
WHERE status = "entregue"
SORT data-entregue ASC
```
