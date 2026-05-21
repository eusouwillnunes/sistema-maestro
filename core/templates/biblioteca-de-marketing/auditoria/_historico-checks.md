---
tipo: painel
escopo: historico-checks-ferramenta
---

# Histórico de checagens de ambiente

Cada linha é uma execução do `/maestro-onboarding` que rodou a verificação de ferramentas (Python, Pandoc, libs, Obsidian).

```dataview
TABLE
  data-execucao AS "Quando",
  os AS "SO",
  package-manager AS "Gerenciador",
  ferramentas-instaladas AS "Instaladas",
  duracao-segundos AS "Duração (s)"
FROM ""
WHERE (file.folder = "memorias/auditoria/checks-de-ferramenta" OR endswith(file.folder, "/checks-de-ferramenta")) AND tipo = "check-de-ferramenta"
SORT data-execucao DESC
LIMIT 20
```
