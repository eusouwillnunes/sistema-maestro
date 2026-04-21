---
description: Template para arquivo individual de sessão de trabalho
tags:
  - "#maestro/template"
---

# Template de Sessão

Template usado pelo `/tchau-maestro` para criar cada arquivo individual em `{projeto}/memorias/sessoes/`.

## Nomenclatura do arquivo

Formato: `YYYY-MM-DD-HHMM-foco.md`

- `YYYY-MM-DD` — data da sessão
- `HHMM` — hora do fechamento (24h, sem dois-pontos)
- `foco` — slug normalizado (lowercase, hífens, sem acentos, max 40 chars)

Exemplo: `2026-04-20-1430-grupo-4-sessoes.md`

## Estrutura

```markdown
---
tipo: sessao
data: 2026-04-20
hora: "14:30"
foco: grupo-4-sessoes
parou-em: "implementar novo fluxo ola-maestro"
---

# Sessão 2026-04-20 14:30 — grupo-4-sessoes

## Concluído
- ✅ [[tarefa-x]] ([agente], modo Agent/Skill)

## Em andamento
- 🔄 [[tarefa-y]] — parou em: [detalhe específico]

## Bloqueado
- 🚫 [[tarefa-z]] — bloqueada por: [[bloqueador]]

## Entrevistas
- [[entrevista-x]] (concluída), [[entrevista-y]] (iniciada), [[entrevista-z]] (pendente)

## Pesquisas
- [[pesquisa-x]] — tema: [descrição]

## Pendências para próxima sessão
- ⏳ [[tarefa-pronta-1]], [[tarefa-pronta-2]]
- 📋 [[entrevista-pendente-1]]

## Parou em
[Frase curta — a "bússola" pro retorno na próxima sessão]

## Observações
[Padrões notados, preferências expressas, decisões tomadas]
```

## Frontmatter

### Campos obrigatórios
- `tipo: sessao` — filtro pra Dataview
- `data` — data da sessão (AAAA-MM-DD)
- `hora` — hora do fechamento ("HH:MM")
- `foco` — slug da sessão (mesma string do nome do arquivo)
- `parou-em` — frase curta descrevendo o ponto de retomada

### Campos opcionais
- `migrada-de-legado: true` — marcado apenas em arquivos gerados pela migração opt-in

### Campos que NÃO vão no frontmatter
Contadores agregados (tarefas-concluidas, modo-agent, etc.) **não** ficam aqui. Eles vivem como queries Dataview no `_sessoes.md` lendo os arquivos de tarefa. Single source of truth.

## Regras do corpo

### Wiki-links obrigatórios
Toda menção a tarefa, plano, entrevista ou pesquisa concluída na sessão deve ser `[[wiki-link]]`. O `tchau-maestro` resolve o nome real do arquivo consultando os indexes do projeto antes de escrever.

### Seções vazias
Omitir seções sem conteúdo. Se não há nada bloqueado, a seção "Bloqueado" inteira sai do arquivo.

### Modo de execução
Cada item em "Concluído" traz modo entre parênteses: `(agente, modo Agent)` ou `(agente, modo Skill)`. Isso alimenta o Dataview do `_sessoes.md` quando o usuário quiser agregar.

## Normalização do slug `foco`

1. Lowercase
2. Remover acentos (NFD + strip diacríticos)
3. Substituir espaços e pontuação por hífens
4. Remover hífens duplicados
5. Truncar em 40 caracteres
6. Remover hífens nas pontas

Exemplos:
- "Grupo 4 — Sessões Separadas" → `grupo-4-sessoes-separadas`
- "Refator do /ola-maestro" → `refator-do-ola-maestro`
- (vazio / caótico) → `sessao-geral` (fallback explícito)
