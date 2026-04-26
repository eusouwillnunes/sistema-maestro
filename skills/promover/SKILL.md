---
name: promover
description: Promove rascunho existente pra entrega formal. Roda pipeline completo (tarefa + QA + Revisor + grafo). Uso /promover [[slug-do-rascunho]].
model: opus
tools: Agent, Read, Write, Edit, AskUserQuestion, TodoWrite
---

# Promover

Transforma rascunho em entrega formal. Funciona forçando `tipo=Entrega` no Maestro, com pré-carregamento do conteúdo do rascunho.

## Uso

```
/promover [[slug-do-rascunho]]
```

## Comportamento

1. Lê o rascunho existente em `rascunhos/[slug].md`
2. Se rascunho não existe ou slug ambíguo, abre AskUserQuestion com opções
3. **Se rascunho tem `status: exploratorio`** — abre `AskUserQuestion` obrigatório antes de prosseguir:
   > "Este rascunho é exploratório — tem suposições declaradas no topo. Você revisou?"
   >
   > - **Sim, promover** (segue fluxo normal de promoção)
   > - **Não, deixa eu revisar primeiro** (aborta promoção com aviso: "Edite o arquivo e chame `/promover [[slug]]` de novo quando estiver pronto")
4. Lê `plugin/skills/maestro/fluxo-entrega.md` via Read
5. Segue o fluxo de Entrega com 5 itens do TodoWrite:
   - Cria tarefa no Gerente (categoria inferida do rascunho)
   - Despacha especialista com conteúdo do rascunho no bloco CONTEXTO (instrução: "este é um rascunho; revise pra entrega formal")
   - QA + Revisor em paralelo
   - Gerente fecha tarefa
6. Artefato final em `entregas/` (ou pasta adequada pelo tipo)
7. Rascunho original fica em `rascunhos/` como histórico (não é apagado automaticamente)
8. Atualiza `status: promovido` no frontmatter do rascunho + adiciona wiki-link pro artefato promovido

## Rascunho inexistente ou ambíguo

- Inexistente: AskUserQuestion "não achei [[x]]. Buscar por substring, listar rascunhos recentes, ou cancelar?"
- Ambíguo (match múltiplo): AskUserQuestion listando candidatos
