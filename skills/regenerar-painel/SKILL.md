---
name: regenerar-painel
description: Atualiza os painéis da Área de Trabalho (`_painel/*.md`) quando a lista de projetos não bate com a realidade. Geralmente NÃO precisa rodar — o painel se atualiza sozinho quando você cria projeto pelo Maestro. Use SE você apagou ou renomeou pasta de projeto direto no Obsidian e o painel ficou listando projeto que não existe mais.
model: sonnet
tools: Read, Glob, Bash, Agent
---

# Regenerar Painel

> Aplica: [[protocolo-ativacao]]

## 1. Papel

Re-sincroniza os painéis Dataview da workspace (`<workspace>/_painel/tarefas.md`, `index.md`, `grafo.md`) com a lista real de projetos detectados via Glob. Operacional, sem produção criativa. Idempotente — roda sem efeito quando a lista já está correta.

## 2. Quando usar

| Situação | Precisa rodar? |
|---|---|
| Criou projeto pelo `/maestro:onboarding` | ❌ Não — Fluxo de Novo Projeto já invoca REGENERATE PAINEL |
| Apagou pasta de projeto direto no Obsidian | ✅ Sim |
| Renomeou pasta de projeto direto no Obsidian | ✅ Sim |
| Mudou `maestro-ativo: true` → `false` no `config.md` | ✅ Sim — projeto sai dos painéis |
| Painel não está renderizando | ❌ Não — provavelmente Dataview desabilitado (ver `[!warning]` no painel) |

## 3. Comportamento

1. **Resolver `{workspace}` e `{projeto}` via `protocolo-ativacao.md` Sub-fluxo 1.**
   - Se STATUS=CWD-INVALIDO → mensagem orientada padrão e parar.
   - Se workspace não existe (sem marker `<workspace>/.maestro-workspace`) → reportar:
     > "Não há Área de Trabalho nesta pasta — o comando só faz sentido dentro de uma workspace do Maestro."
   - E parar.

2. **Despachar Bibliotecário via `Agent()`:**

   ```
   Agent(
     subagent_type="maestro:bibliotecario",
     prompt="""
     CONTEXTO:
     workspace: {workspace}

     FLUXO: REGENERATE PAINEL
     """
   )
   ```

3. **Reportar resultado em linguagem simples** (traduzir do report técnico do Bibliotecário):
   - Se DONE com mudanças → "Painéis atualizados — agora listam N projetos: A, B, C."
   - Se DONE sem mudanças → "Tudo em dia — os painéis já listavam todos os projetos ativos."
   - Se BLOCKED → traduzir motivo do report em linguagem natural (ex: "Marker da workspace não foi encontrado — você está numa pasta que não é uma Área de Trabalho do Maestro.").

## 4. Despacho via hub

Exceção legítima ao "todo dispatch passa pelo Gerente" via critério decisor da seção 7 do `protocolo-agent.md` (operação técnica, não autoral). REGENERATE PAINEL atualiza sintaxe Dataview em arquivos gerados, não produz entrega criativa em pt-br.

## 5. Não-objetivos

- Renderizar painel manualmente — Dataview faz isso sozinho quando o Obsidian abre.
- Criar painéis na 1ª vez — fluxo de scaffold é `SCAFFOLD WORKSPACE` (acionado pelo onboarding).
- Mudar conteúdo das queries Dataview — pra modificar template, edita `plugin/core/templates/workspace/_painel/*.md` e re-publica.
