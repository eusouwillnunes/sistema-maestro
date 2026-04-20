---
description: Protocolo compartilhado para geração, execução, retomada e higiene das sub-tarefas dinâmicas pelos especialistas
tags:
  - "#maestro/protocolo"
---

# Protocolo de Sub-tarefas

> [!info] Protocolo compartilhado do sistema MAESTRO.
> Referenciado por todos os especialistas que produzem conteúdo (Copywriter, Estrategista, Marca, Mídias Sociais, Performance, Pesquisador).

## Objetivo

Definir como o especialista gera, executa, marca, retoma e limpa sub-tarefas durante a execução de uma tarefa do sistema. Sub-tarefas vivem em duas camadas: seção "Sub-tarefas" do arquivo da tarefa (persistente, fonte da verdade) e TodoWrite da sessão (view layer em tempo real).

---

## 1. Geração (up-front, antes de executar)

Ao receber uma tarefa do Maestro, ANTES de começar a produzir conteúdo:

1. **Carregue o contexto.** Siga o Mapa de Necessidades do seu skill — leia identidade de marca, templates de produto, entrevistas, pesquisas e material de referência referenciados no bloco CONTEXTO.

2. **Gere a lista de sub-tarefas dinâmicas.** Critérios:
   - Tipicamente **3-8 itens**. Permitido **1-2** quando o trabalho é genuinamente indivisível (ex: "me dê um título alternativo").
   - Sub-tarefas devem refletir o que é ESPECÍFICO deste pedido. Se sua sub-tarefa faria sentido em qualquer tarefa da mesma categoria, ela está genérica demais — refine.
   - Exemplo ruim: "escrever headline". Exemplo bom: "testar gancho de urgência vs curiosidade".

3. **Grave no arquivo da tarefa** via `Edit`. Adicione à seção "Sub-tarefas" do arquivo:

```markdown
## Sub-tarefas

- [ ] [Sub-tarefa 1 específica]
- [ ] [Sub-tarefa 2 específica]
- [ ] [Sub-tarefa 3 específica]
```

4. **Crie no TodoWrite** via `TaskCreate` uma task por sub-tarefa, com status inicial `pending`.

5. **Em modo Agent(), reporte brevemente ao Maestro** antes de executar: "Sub-tarefas geradas: [lista]. Começando." (em Skill(), o próprio TodoWrite no terminal já comunica).

---

## 2. Execução (marcação em tempo real)

Para cada sub-tarefa, na ordem do trabalho real:

1. `TaskUpdate(id, status=in_progress)` — marca que está trabalhando nela.
2. Execute o trabalho correspondente.
3. `Edit` do arquivo da tarefa — marca `[x]` no item correspondente (+ anotação opcional se houve decisão não-óbvia).
4. `TaskUpdate(id, status=completed)` — marca que terminou.

**ORDEM OBRIGATÓRIA:** o `Edit` do arquivo (passo 3) acontece ANTES de `TaskUpdate(completed)` (passo 4). O arquivo é fonte da verdade; o TodoWrite é view.

**Estados válidos:**

| Arquivo | TodoWrite | Significado |
|---------|-----------|-------------|
| `[ ]`   | pending   | não iniciada |
| `[ ]`   | in_progress | em execução |
| `[x]`   | completed | concluída |

**Estado proibido:** `[ ]` + completed. A ordem acima previne isso.

---

## 3. Anotação opcional

Ao marcar `[x]`, o especialista decide caso a caso se anota uma linha curta sobre o que foi feito. Critério: "outro especialista precisaria entender isso pra retomar?"

Exemplos:

```markdown
- [x] Testar gancho urgência vs curiosidade → escolhido urgência (ticket alto responde melhor)
- [x] Escrever variação A da headline → 3 versões produzidas, ver parágrafo 2
```

Anotação é opcional. Sub-tarefas mecânicas (ex: "salvar arquivo") marcam `[x]` direto.

---

## 4. Retomada de sessão

Se uma tarefa foi deixada pela metade (sessão caiu, especialista reportou bloqueio, etc.), o especialista que retoma deve:

1. **Ler o arquivo da tarefa** (fonte da verdade).
2. **Se a seção "Sub-tarefas" existe e tem itens:**
   - Itens `[x]` = já concluídos. Itens `[ ]` = pendentes.
   - Recriar o TodoWrite a partir do arquivo: `TaskCreate` com status derivado — `completed` pros `[x]`, `pending` pros `[ ]`.
   - Executar APENAS os pendentes, seguindo o ciclo do item 2.
3. **Se a seção "Sub-tarefas" não existe ou está vazia:** tratar como tarefa nova — voltar ao item 1 (Geração).

**Regra crítica:** NUNCA regenere sub-tarefas já marcadas. Regenerar perderia trabalho feito e mudaria o escopo silenciosamente.

---

## 5. Tratamento de falhas no meio da execução

Se, no meio das sub-tarefas, o especialista detecta que precisa reportar `NEEDS_DATA`, `NEEDS_CONTEXT` ou `BLOCKED`:

1. Deixa a sub-tarefa corrente em `in_progress` no TodoWrite (não marca completed, não marca [x] no arquivo).
2. Reporta o bloqueio ao Maestro com o status apropriado (protocolo-agent.md).
3. **NÃO limpa o TodoWrite.** Estado parcial preservado.
4. Maestro dispara entrevista/providencia contexto (ciclo existente — Fluxo 10 do Gerente).
5. Quando a tarefa é retomada, o Protocolo de Retomada (item 4) continua do ponto onde parou.

---

## 6. Higiene (ao finalizar)

Ao reportar o fim da execução da tarefa ao Maestro:

1. Confirme que todos os itens da seção "Sub-tarefas" estão marcados `[x]` no arquivo.
2. Para cada sub-tarefa ainda visível no TodoWrite, faça `TaskUpdate(id, status=deleted)`.
3. O arquivo mantém o rastro permanente das sub-tarefas concluídas; o TodoWrite fica limpo pro fluxo macro do Maestro continuar.
