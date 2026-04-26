---
tipo: memoria
area: pendencias
escopo: qualidade
---

# Pendências aceitas pelo usuário

Registro longitudinal de usos da opção "forçar entrega com pendência" em QA/Revisor. Após 3 usos no mesmo projeto sem mudança de checklist, Maestro bloqueia a opção e força revisão estrutural.

## Formato

```
- YYYY-MM-DD HH:MM — [[artefato]]
  - Gate que reprovou: QA | Revisor
  - Item do checklist: [texto do item]
  - Motivo do override: [campo livre do usuário]
  - Rodadas até override: 3/3
```

## Registro

(vazio no início — Maestro popula)

## Contador de intervenção

- Usos totais no projeto: 0
- Checklist já ajustados: (nenhum)
- Próxima intervenção quando contador atingir: 3
