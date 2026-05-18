---
tipo: indice
area: auditoria-sistema
descricao: Painel de auditoria pra detectar violações do princípio "Maestro orquestra, nunca produz" — lista tarefas-filhas de revisão onde a correção pós-Revisor ficou com autoria errada
tags:
  - "#maestro/auditoria"
  - "#maestro/indice"
---

# Violações detectadas — B-S55-47

> Tarefas-filhas de revisão onde a correção pós-Revisor ficou com autoria errada ou ausente.
> Se essa tabela tiver linhas, é evidência de violação do princípio "Maestro orquestra, nunca produz nem julga".
> Investigar caso a caso e re-despachar o especialista certo.

```dataview
TABLE WITHOUT ID
  file.link as "Tarefa de revisão",
  agente as "Agente esperado",
  _ultima-correcao-por as "Quem aplicou",
  status as "Status",
  data-conclusao as "Fechada em"
FROM ""
WHERE file.folder = this.file.folder
  AND tipo = "tarefa"
  AND categoria = "revisao"
  AND agente != "usuario"
  AND (_ultima-correcao-por = "maestro" OR _ultima-correcao-por = null)
  AND pendencias-aceitas = null
SORT data-conclusao DESC
```

## Como funciona

- **Tarefa de revisão** = tarefa-filha criada pelo Fluxo 3 do Gerente quando QA ou Revisor reprovam.
- **Agente esperado** = especialista que produziu o artefato original (Marca, Copywriter, etc.).
- **Quem aplicou** = lido do campo `_ultima-correcao-por` da tarefa-filha. Se for `maestro` ou ausente, viola o princípio.
- **Status** = `aprovado-com-pendencia` significa que o usuário aceitou a pendência conscientemente (rodada 3) — não é violação.

## Painel vazio = sistema saudável

Se essa tabela está vazia depois de um tempo de uso, o tripwire do Gerente está funcionando. Aparece linha → reportar como bug e investigar como o caso passou pelo tripwire.
