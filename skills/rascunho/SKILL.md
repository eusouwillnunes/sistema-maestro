---
name: rascunho
description: Cria rascunho rápido sem validação. Use /rascunho [pedido] para gerar conteúdo em rascunhos/ que pode ser promovido depois via /promover.
model: opus
tools: Agent, Read, Write, AskUserQuestion, TodoWrite
---

# Rascunho

Cria rascunho rápido. Funciona forçando `tipo=Rascunho` no Maestro.

## Uso

```
/rascunho cria 3 headlines pra consultoria da Automators
```

## Comportamento

1. Lê `plugin/skills/maestro/fluxo-rascunho.md` via Read
2. Segue o fluxo de Rascunho (3 itens do TodoWrite)
3. Cria arquivo em `rascunhos/YYYY-MM-DD-HHMM-slug.md`
4. Retorna link pro rascunho + aviso de expiração em 30 dias

## Limites

- Máximo 20 rascunhos abertos simultâneos no projeto
- Se limite atingido, AskUserQuestion força limpar antes de criar novo

## Promover depois

Pra transformar em entrega formal (com tarefa, QA, Revisor, grafo), usar:

```
/promover [[slug-do-rascunho]]
```
