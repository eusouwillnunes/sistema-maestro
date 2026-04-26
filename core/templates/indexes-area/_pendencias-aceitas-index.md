---
tipo: index
area: qa
descricao: Histórico longitudinal de pendências aceitas pelo usuário (overrides do QA)
---

# Pendências Aceitas (histórico)

> [!info] O que aparece aqui
> Cada vez que você forçou uma entrega após 3 reprovações do QA, fica registrado em `memorias/pendencias-aceitas.md`. Este painel agrupa por item de checklist pra você ver padrões emergentes — se um item reprova sempre, talvez seja melhor ajustar o critério.

## Por item de checklist

```dataview
TABLE artefato AS "Artefato", motivo AS "Motivo", data AS "Quando"
FROM ""
WHERE (startswith(file.folder, this.file.folder + "/memorias") OR file.folder = this.file.folder + "/memorias")
  AND file.name = "pendencias-aceitas"
SORT data DESC
GROUP BY item-checklist
```

> Padrão recorrente? Considere ajustar o item via `/maestro-revisar-memorias` ou editando direto em `{projeto}/maestro/checklists/`.
