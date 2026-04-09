---
description: Templates reutilizáveis criados pelo usuário entre projetos
tags:
  - "#maestro/template"
---

# Biblioteca do Usuário

Esta pasta contém templates criados por você durante o uso do Sistema Maestro. Eles são reutilizáveis entre projetos.

## Estrutura

```
biblioteca/
  identidade/     ← Templates de identidade de marca
  produto/        ← Templates de produto
  referencia/     ← Templates de estratégia, funis, lançamentos
  custom/         ← Templates que não se encaixam nas categorias acima
```

## Como funciona

- Os agentes especialistas buscam aqui automaticamente (prioridade 2, depois da biblioteca do projeto)
- Templates são sugeridos pelos agentes e salvos aqui com sua aprovação
- Você pode criar e organizar templates manualmente também
- Nomenclatura: kebab-case (ex: `lancamento-semente-modelo.md`)
