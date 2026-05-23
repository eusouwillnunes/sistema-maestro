---
tipo: painel
status: ativo
titulo: Bloqueios do hook PreToolUse
---

# Bloqueios do hook PreToolUse

Eventos onde o hook impediu dispatch de `Agent(maestro:*)` fora do protocolo.
Origem: `memorias/auditoria/historico.md`.

## Últimos 30 dias

```dataview
TABLE WITHOUT ID
  data as "Data",
  evento as "Tipo",
  skill as "Skill",
  target as "Alvo"
FROM ""
WHERE file.name = "historico"
  AND contains(file.folder, "memorias/auditoria")
FLATTEN file.lists as linha
WHERE startswith(linha.text, "-")
  AND contains(linha.text, "agent-maestro-de-skill-bloqueado")
SORT linha.text DESC
LIMIT 30
```
