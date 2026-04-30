---
tipo: index
area: planos
descricao: "Painel de gestão de planos do projeto"
tags:
  - "#maestro/index"
---

# Planos

> [!info] Painel de planos
> Atualizado automaticamente via Dataview. Painel vazio é normal em projeto novo. Requer o plugin Dataview do Obsidian instalado e habilitado.

## Estatísticas

```dataview
TABLE length(rows) as Quantidade
FROM ""
WHERE file.folder = this.file.folder AND tipo = "plano"
GROUP BY status
```

---

## ⚠️ Em revisão — ação necessária

> [!warning] Planos aguardando seu feedback (Gate 2)
> Responda no chat com **aprovar**, **ajustar**, **regerar** ou **cancelar**. Cap de 3 voltas em ajustes.

```dataview
TABLE solicitante, voltas-em-revisao as Voltas, data-criacao as Criação
FROM ""
WHERE file.folder = this.file.folder AND tipo = "plano" AND status = "em-revisao"
SORT data-criacao DESC
```

---

## Rascunho

```dataview
TABLE solicitante, voltas-em-revisao as Voltas, data-criacao as Criação
FROM ""
WHERE file.folder = this.file.folder AND tipo = "plano" AND status = "rascunho"
SORT data-criacao DESC
```

## Aprovado

```dataview
TABLE solicitante, data-aprovacao as Aprovação
FROM ""
WHERE file.folder = this.file.folder AND tipo = "plano" AND status = "aprovado"
SORT data-aprovacao DESC
```

## Em execução

```dataview
TABLE solicitante, data-aprovacao as Aprovação
FROM ""
WHERE file.folder = this.file.folder AND tipo = "plano" AND status = "em-execucao"
SORT data-aprovacao DESC
```

## Aguardando validação

```dataview
TABLE solicitante, data-aprovacao as Aprovação
FROM ""
WHERE file.folder = this.file.folder AND tipo = "plano" AND status = "aguardando-validacao"
```

## Concluído

```dataview
TABLE solicitante, data-conclusao as Conclusão
FROM ""
WHERE file.folder = this.file.folder AND tipo = "plano" AND status = "concluido"
SORT data-conclusao DESC
LIMIT 15
```

## Rejeitado

```dataview
TABLE solicitante, data-criacao as Criação
FROM ""
WHERE file.folder = this.file.folder AND tipo = "plano" AND status = "rejeitado"
SORT data-criacao DESC
```

## Cancelado

```dataview
TABLE solicitante, motivo-cancelamento as Motivo, data-cancelamento as Cancelamento
FROM ""
WHERE file.folder = this.file.folder AND tipo = "plano" AND status = "cancelado"
SORT data-cancelamento DESC
LIMIT 15
```

---

## Planos de correção vinculados

```dataview
TABLE corrige as "Corrige", status as "Status"
FROM ""
WHERE file.folder = this.file.folder AND corrige != null
SORT data-criacao DESC
```

---

> [!tip] 💡 Pesquisa rápida
>
> No Obsidian, use Quick Switcher (Cmd+K / Ctrl+K) ou Search com operadores:
> - `status:em-revisao` — planos esperando seu feedback
> - `status:rascunho` — planos aguardando primeira leitura
> - `voltas-em-revisao:3` — planos no limite do cap de voltas
> - `parte-de:[[planos/X]]` — todas tarefas do plano X
