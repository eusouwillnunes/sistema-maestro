---
name: feedback
description: >
  Revisão de entregas pendentes do usuário. Lista tarefas com status: entregue,
  apresenta cada uma, captura decisão (Aprovar / Aceitar com ressalva / Reprovar
  e pedir refação / Pular). Despacha Gerente Fluxos 14/15 conforme escolha.
  Acionado via /feedback (sem argumento abre fila) ou /feedback <slug>.
---

> [!important] Antes de executar, verifique se o Sistema Maestro está ativo neste projeto seguindo o `core/protocolos/protocolo-ativacao.md`.

# /feedback — Revisão de entregas

## 1. Especialidade

Skill top-level invocada pelo usuário ou pelo Maestro quando há entregas em `status: entregue` aguardando avaliação. Fecha o ciclo da F-Status: agente entrega → Gerente transita para `entregue` → usuário avalia via `/feedback` → Gerente transita para `concluido` ou `reprovado`.

## 2. Fluxo principal

### Sem argumento — abrir fila

1. **Glob** tarefas com `status: entregue` no projeto ativo:

```bash
grep -rln "^status: entregue" "{projeto}/tarefas/" | head -10
```

2. Ler frontmatter de cada uma (`titulo`, `resultado`, `data-entregue`).
3. Apresentar **máximo 10 por vez**. Se houver mais, fechar com "Você tem N entregas pendentes; mostrando as 10 mais antigas".
4. `AskUserQuestion`:
   - Pergunta: "Qual entrega você quer revisar primeiro?"
   - Opções: até 4 títulos curtos + (se houver >4) "Ver lista completa" (abre painel `[[_painel/tarefas#Entregues — aguardando seu feedback]]` em vez de despachar).

### Com argumento `/feedback <slug>`

Vai direto pra Seção 3 (apresentar tarefa).

## 3. Apresentar tarefa

Para cada tarefa selecionada:

1. Renderizar resumo:
   - **Título:** [titulo]
   - **Briefing:** [briefing — 1-2 linhas do corpo da tarefa]
   - **Artefato:** `[[<wikilink-do-resultado>]]`
   - **Entregue há:** [diff entre `data-entregue` e agora, em pt-br: "2 dias", "1 hora"]
2. `AskUserQuestion`:
   - Pergunta: "O que você quer fazer com essa entrega?"
   - Opções fixas:
     - **Aprovar** — fecha tarefa + artefato em `concluido`
     - **Aceitar com ressalva** — fecha em `concluido` + grava nota em `pendencias-aceitas`
     - **Reprovar e pedir refação** — abre revisão em `reprovado` + grava `motivo-reprovacao`
     - **Pular pra próxima** — não fecha, volta pra fila

## 4. Captura de texto livre (Aceitar com ressalva / Reprovar)

Após AUQ, se escolha é "Aceitar com ressalva" ou "Reprovar e pedir refação":

1. Prompt direto no chat (não AUQ — AUQ não aceita texto livre):
   - **Aceitar com ressalva:** "O que ficou pendente? (1-2 linhas)"
   - **Reprovar e pedir refação:** "O que precisa mudar? Quanto mais específico, melhor pro especialista que vai refazer."
2. Aguardar resposta do usuário no chat.
3. **Se resposta vazia ou só whitespace:** abortar a transição. Mensagem: "Texto vazio detectado, escolha outra opção ou digite o motivo." Volta para AUQ da Seção 3.

## 5. Dispatch Gerente

Conforme escolha:

- **Aprovar** → `Agent(maestro:gerente)` com:
  ```
  FLUXO: aprovar-entregue
  CONTEXTO:
    tarefa-slug: <slug>
    decisao: aprovado
  ```
- **Aceitar com ressalva** → `Agent(maestro:gerente)` com:
  ```
  FLUXO: aprovar-entregue
  CONTEXTO:
    tarefa-slug: <slug>
    decisao: pendencia-aceita
    pendencia: <texto>
  ```
- **Reprovar e pedir refação** → `Agent(maestro:gerente)` com:
  ```
  FLUXO: reprovar-entregue
  CONTEXTO:
    tarefa-slug: <slug>
    motivo: <texto>
  ```
- **Pular pra próxima** → continuar loop (não despacha).

**Importante (aprendizado #61):** despacha Gerente via `Agent(maestro:gerente)` direto, NÃO via hub Maestro. Não passa pelo classificador do hub — evita que sub-dispatches de QA/Revisor virem `Skill()` em vez de `Agent()`.

## 6. Loop

Após cada decisão, voltar para Seção 2 (re-listar fila). Sair quando:
- Fila zerar.
- Usuário responder "parar" ou "depois" ao próximo AUQ.

## 7. Mensagem final

Pluralização explícita:

- **Fila zerada (N entregas fechadas, N >= 1):**
  - N == 1: "Tudo revisado. **1 entrega fechada** nesta sessão."
  - N >= 2: "Tudo revisado. **{N} entregas fechadas** nesta sessão."
- **Usuário parou (M ainda pendentes):**
  - M == 1: "Pausado. Você ainda tem **1 entrega** pendente. Rode `/feedback` quando quiser retomar."
  - M >= 2: "Pausado. Você ainda tem **{M} entregas** pendentes. Rode `/feedback` quando quiser retomar."
