---
titulo: Defesa Anti-Hallucination
tipo: doc-sistema
area: auditoria
---

# Defesa Anti-Hallucination

> [!info] Pasta do sistema — não editar manualmente
> Esta pasta é gerenciada pelo Sistema Maestro. Os arquivos aqui provam matematicamente que o Revisor leu o seu artefato (e não inventou conteúdo).

## Como funciona

Quando o Maestro despacha um Revisor, ele cria um **canário** em `canarios-ativos/<slug>.md` com:

- **Token aleatório** (ex: `VERIF-A3F9C2`)
- **MD5 esperado** do artefato sendo revisado

O Revisor precisa começar o report com `[VERIF] <token> | MD5 <md5>` — provando que leu os 2 arquivos.

Se o token ou o MD5 não baterem, o Maestro descarta o report e re-despacha.

## Por que isso existe

Bug B-S59-1 (Sessão 59): Revisores em paralelo retornaram reports completamente alucinados (textos sobre lugares aleatórios, não relacionados aos artefatos reais). Smoking gun: `tool_uses: 0` — subagent não chamou nenhuma ferramenta, inferiu o report direto.

A defesa por canário + MD5 garante que o Revisor de fato leu o artefato antes de produzir o report.

## Arquivos nesta pasta

- `historico.md` — log longitudinal de canários emitidos.
- `canarios-ativos/` — canários pendentes de validação. Limpos automaticamente após validação ou >5min.
