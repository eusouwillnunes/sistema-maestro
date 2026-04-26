---
tipo: index
area: qa
descricao: Tarefas com pendência de qualidade (reprovação ou em revisão)
---

# Pendências de Qualidade

> [!info] O que aparece aqui
> Tarefas com `status: aprovado-com-pendencia` (entrega forçada após 3 reprovações) ou `categoria: revisao` ativa. Quando vazio, mostra mensagem de "sem pendências".

## Pendências ativas

```dataview
TABLE titulo AS "Tarefa", categoria AS "Categoria", status AS "Status", data-criacao AS "Criada em"
FROM ""
WHERE (startswith(file.folder, this.file.folder + "/") OR file.folder = this.file.folder)
  AND tipo = "tarefa"
  AND (status = "aprovado-com-pendencia" OR (categoria = "revisao" AND status != "concluida" AND status != "cancelada"))
SORT data-criacao DESC
```

> Sem pendências? O painel renderiza vazio — sinal de que tudo passou pelo QA limpo.
