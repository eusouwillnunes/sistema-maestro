---
tipo: index
area: planos
descricao: "Painel de gestão de planos do projeto"
tags:
  - "#maestro/index"
---

# Planos

> [!info] Painel de planos
> Mantido automaticamente pelo Gerente de Projetos. Consultável no Obsidian.

## Estatísticas

```dataview
TABLE length(rows) as Quantidade
FROM "planos"
WHERE tipo = "plano"
GROUP BY status
```

---

## Rascunho

| Plano | Solicitante | Criação |
|-------|-------------|---------|
| (nenhum) | — | — |

## Aprovado

| Plano | Solicitante | Aprovação |
|-------|-------------|-----------|
| (nenhum) | — | — |

## Em execução

| Plano | Solicitante | Aprovação | Tarefas pendentes |
|-------|-------------|-----------|-------------------|
| (nenhum) | — | — | — |

## Aguardando validação

| Plano | Solicitante | Aprovação |
|-------|-------------|-----------|
| (nenhum) | — | — |

## Concluído

| Plano | Solicitante | Conclusão |
|-------|-------------|-----------|
| (nenhum) | — | — |

## Rejeitado

| Plano | Solicitante | Data |
|-------|-------------|------|
| (nenhum) | — | — |

---

## Planos de correção vinculados

```dataview
TABLE corrige as "Corrige", status as "Status"
FROM "planos"
WHERE corrige != null
SORT data-criacao DESC
```
