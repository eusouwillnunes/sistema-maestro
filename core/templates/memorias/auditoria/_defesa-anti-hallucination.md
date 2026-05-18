---
tipo: painel-dataview
descricao: Agrega disparos da defesa anti-hallucination (B-S59-1) pra rastreio longitudinal
---

# Defesa Anti-Hallucination — Histórico de Disparos

> Painel agregador. Fonte: `memorias/auditoria/historico.md`. Princípio Decisão 084 — painel mora junto da fonte que agrega.

## Últimos 30 dias

```dataview
TABLE WITHOUT ID
  data AS "Data",
  agente AS "Agente",
  causa AS "Causa",
  retry AS "Retry"
FROM ""
WHERE file.folder = this.file.folder AND evento = "defesa-anti-hallucination"
  AND data >= date(today) - dur(30 days)
SORT data DESC
```

## Resumo por agente (últimos 30 dias)

```dataview
TABLE WITHOUT ID
  agente AS "Agente",
  length(rows) AS "Disparos"
FROM ""
WHERE file.folder = this.file.folder AND evento = "defesa-anti-hallucination"
  AND data >= date(today) - dur(30 days)
GROUP BY agente
SORT length(rows) DESC
```

> **Como ler:** se contagem ≥3 em 7 dias, regressão possível — investigar.
