---
tipo: index
area: qa
descricao: Tarefas com pendência de qualidade (reprovação ou em revisão)
---

# Pendências de Qualidade

> [!info] O que aparece aqui
> Tarefas com `pendencias-aceitas` preenchido (entrega aceita com ressalva via `/feedback` — F-Status M6) ou `categoria: revisao` ativa. Quando vazio, mostra mensagem de "sem pendências".

## Pendências ativas

```dataview
TABLE titulo AS "Tarefa", categoria AS "Categoria", status AS "Status", data-criacao AS "Criada em"
FROM ""
WHERE file.folder = this.file.folder
  AND tipo = "tarefa"
  AND (pendencias-aceitas != null OR (categoria = "revisao" AND status != "concluido" AND status != "cancelado"))
SORT data-criacao DESC
```

> Sem pendências? O painel renderiza vazio — sinal de que tudo passou pelo QA limpo.
