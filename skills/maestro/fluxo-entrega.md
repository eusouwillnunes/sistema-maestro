# Fluxo de Entrega

Sub-skill lida pelo Maestro via `Read` quando o classificador retorna `tipo=Entrega`.

## TodoWrite obrigatório (5 itens fixos)

Antes de qualquer dispatch, escrever `TodoWrite` com estes 5 itens. A ordem e o wording são fixos — não adaptar por pedido:

1. `Criar tarefa no Gerente com categoria [X]` — preencher [X] com categoria inferida (copy, pesquisa, estrategia, marca, midias, performance, biblioteca, identidade, geral)
2. `Despachar [especialista] com casca do artefato` — preencher [especialista] com nome do agente (copywriter, estrategista, marca, midias-sociais, performance, pesquisador)
3. `Executar QA do artefato`
4. `Executar Revisor do artefato`
5. `Fechar tarefa no Gerente (status concluida)`

Marcar item 1 como `in_progress` antes do primeiro dispatch. Nunca começar com item 2 ou posterior.

## Passo a passo

### Item 1 — Criar tarefa no Gerente

1. Preparar bloco de contexto com: resumo do pedido do usuário, categoria inferida, especialista destinado, artefato alvo (tipo + caminho).
2. Despachar Gerente em modo criar-tarefa via `Agent()`.
3. Aguardar retorno com `tarefa-id` e `caminho-da-casca-do-artefato`.
4. Se retorno vier sem `tarefa-id` → abortar pipeline e reportar falha (ver "Falha de Gerente" abaixo).
5. Marcar item 1 como `completed`. Marcar item 2 como `in_progress`.

### Item 2 — Despachar especialista

1. Preparar bloco CONTEXTO conforme `protocolo-contexto.md` (identidade, produto, memórias, artefatos relacionados).
2. Incluir no bloco CONTEXTO (instrução pro especialista, não campo de frontmatter): **tarefa relacionada** = `[[tarefas/<slug-id>]]` (do Gerente no Item 1) e **caminho da casca do artefato** = `[[<pasta-destino>/<slug>]]` onde o especialista deve escrever o resultado. O especialista atualiza o frontmatter do artefato com `origem-tarefa: "[[tarefas/<slug-id>]]"` quando escrever o conteúdo final (ver `protocolo-biblioteca` seção "Wikilinks em frontmatter").
3. Despachar especialista via `Agent()` (se Opus 4.7 ou Sonnet 4.6 — ver política em `docs/decisions.md`).
4. Tratar round-trips `NEEDS_*` lendo `fluxo-needs.md`. Durante round-trip, item 2 permanece `in_progress`.
5. Quando especialista retornar com `STATUS: DONE` e sem `NEEDS_*`, marcar item 2 `completed` e avançar.

### Itens 3 e 4 — QA e Revisor (paralelo)

1. Despachar QA e Revisor **em paralelo** via 2 `Agent()` simultâneos na mesma mensagem.
2. Aguardar ambos retornarem.
3. Ler os 2 reports:
   - **QA `STATUS: DONE`:** marcar item 3 `completed`.
   - **QA reprova:** executar protocolo "QA reprova" abaixo.
   - **Revisor `STATUS: DONE` APROVADO:** marcar item 4 `completed`.
   - **Revisor reprova:** executar protocolo "Revisor reprova" abaixo.
4. Só avança pro item 5 quando os dois estiverem `completed`.

### Item 5 — Fechar tarefa no Gerente

1. Despachar Gerente em modo concluir-tarefa com `tarefa-id` e `caminho-do-artefato-final`.
2. Aguardar retorno confirmando `status: concluida` e `data-conclusao` preenchida.
3. Marcar item 5 `completed`.
4. TodoWrite fica 5/5 completed.
5. Maestro apresenta entrega ao usuário (resumo + link pro artefato + link pra tarefa).

## Protocolos de falha

### QA reprova

1. Gerente cria tarefa de revisão filha (categoria = revisão).
2. Especialista original é re-despachado com feedback específico do QA.
3. QA roda de novo no novo resultado.
4. Contador local de rodadas: 1, 2, 3.
5. **Na 3a reprova, abortar pipeline e perguntar ao usuário via `AskUserQuestion`:**
   - **Revisar o pedido** (usuário reescreve)
   - **Ver o último rascunho** (entrega parcial pra inspeção)
   - **Forçar entrega com pendência** (loga `status: aprovado-com-pendencia` + seção "Pendências aceitas pelo usuário" + append em `memorias/pendencias-aceitas.md` — ver fluxo-needs.md seção governança)

### Revisor reprova

Mesma lógica. Na 3a reprova, oferecer também gravar preferência de estilo em `memorias/preferencias-estilo.md` pra não reincidir.

### Falha de Gerente ao criar tarefa

1. Item 1 fica `in_progress` (não marca completed).
2. Abortar pipeline antes de qualquer dispatch de especialista.
3. Reportar ao usuário com diagnóstico (arquivo afetado, erro recebido).
4. Nunca tentar "prosseguir sem tarefa" — princípio absoluto.

### Item travado (>2 min sem output)

Interromper Agent() travado. Abrir `AskUserQuestion` perguntando: continuar, abortar ou retry.

## Regras absolutas

1. Nunca marcar item `completed` sem o passo ter executado.
2. Nunca entregar ao usuário com TodoWrite incompleto.
3. Nunca pular itens — falha → protocolo de falha explícito.
4. `AskUserQuestion` em qualquer dúvida sobre classificação durante execução.
