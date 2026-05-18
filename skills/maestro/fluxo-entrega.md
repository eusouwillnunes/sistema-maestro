# Fluxo de Entrega

Sub-skill lida pelo Maestro via `Read` quando o classificador retorna `tipo=Entrega`.

## TodoWrite obrigatório (5 itens fixos)

Antes de qualquer dispatch, escrever `TodoWrite` com estes 5 itens. A ordem e o wording são fixos — não adaptar por pedido:

1. `Criar tarefa no Gerente com categoria [X]` — preencher [X] com categoria inferida (copy, pesquisa, estrategia, marca, midias, performance, biblioteca, identidade, geral)
2. `Despachar [especialista] com casca do artefato` — preencher [especialista] com nome do agente (copywriter, estrategista, marca, midias-sociais, performance, pesquisador)
3. `Executar QA do artefato`
4. `Executar Revisor do artefato`
5. `Fechar tarefa no Gerente (status concluido)`

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
3. **Detecção de cadeia de identidade (CONTEXTO extra):** se a tarefa atual satisfaz TODAS as condições:
   - `parte-de:` aponta pra plano (`[[planos/<slug>]]`).
   - Plano tem `modo-cadeia: guiado` ou `modo-cadeia: automatico` no frontmatter.
   - `bloqueada-por:` tem ≥1 wikilink.
   - Cada wikilink em `bloqueada-por:` aponta pra tarefa com `status: concluido` ou `pendencias-aceitas` preenchido E `resultado:` preenchido.

   Então adicionar bloco `---ARTEFATOS-CADEIA---` no CONTEXTO conforme `protocolo-contexto.md` seção "Contexto para a Marca em tarefa-filha de cadeia de identidade". Listar caminhos absolutos dos artefatos das tarefas anteriores aprovadas em ordem cronológica.

   **Se alguma condição falha** (ex: tarefa de bloqueada-por sem `resultado:`): reportar erro técnico ao usuário ("Cadeia inconsistente — filha N depende de M, mas M não tem resultado. Investigando."), abortar item 2, NÃO despachar.

4. Despachar especialista via `Agent()` (se Opus 4.7 ou Sonnet 4.6 — ver política em `docs/decisions.md`).
5. Tratar round-trips `NEEDS_*` lendo `fluxo-needs.md`. Durante round-trip, item 2 permanece `in_progress`.
6. Quando especialista retornar com `STATUS: DONE` e sem `NEEDS_*`, marcar item 2 `completed` e avançar.

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

1. Despachar Gerente em modo `concluir-tarefa` com `tarefa-id` e `caminho-do-artefato-final`. **Se houve ciclo de validação** (tarefa-filha de categoria `revisao` foi fechada), incluir no payload `_ultima-correcao-por: <slug-especialista-que-aplicou>`. Se foi aprovação direta sem ciclo, omitir o campo.
2. Aguardar retorno confirmando `status: concluido` e `data-conclusao` preenchida. Se Gerente retornar `BLOCKED` com `referencia-tecnica: B-S55-47`, ler `plugin/skills/maestro/limites-maestro.md` seção 4 e traduzir pro usuário em linguagem natural — depois re-executar o passo certo (re-despachar especialista pra aplicar correção).
3. Marcar item 5 `completed`.
4. TodoWrite fica 5/5 completed.
5. Maestro apresenta entrega ao usuário (resumo + link pro artefato + link pra tarefa).

### Item 5.bis — Cadência da cadeia (apenas se plano tem `modo-cadeia` preenchido)

Após Item 5 fechar (tarefa concluída ou aprovada-com-pendência), checar se a tarefa é filha de plano com `modo-cadeia: guiado` ou `modo-cadeia: automatico`:

1. Ler frontmatter da tarefa atual: `parte-de: [[planos/<slug>]]`.
2. Ler frontmatter do plano: `modo-cadeia`.
3. Se `~`: cadência não se aplica; pular pra apresentação ao usuário (Item 5 passo 5).

**Se `modo-cadeia: automatico`:**

1. Identificar próxima filha pendente (mesmo plano, `bloqueada-por:` aponta pra tarefa que acabou de fechar).
2. Despachar Item 1 do `fluxo-entrega.md` pra essa próxima filha (Gerente já criou casca via Fluxo 5; agora roda pipeline completo: Marca → QA → Revisor → Gerente fecha).
3. Repetir até última filha do plano fechar.
4. Quando última filha fecha: apresentar ao usuário resumo final com 7 wikilinks + tabela de status (concluida vs aprovado-com-pendencia).

**Se `modo-cadeia: guiado`:**

1. Apresentar artefato resumido ao usuário (1-2 frases) + wikilink + atalho pra abrir no Obsidian.
2. **AskUserQuestion** com 3 opções:

   | Opção | Resultado |
   |---|---|
   | **Aprovar e seguir** | Liberar próxima filha. Maestro despacha Item 1 do fluxo-entrega.md pra próxima. |
   | **Pedir ajuste** | Entra em refinamento da filha atual via `fluxo-refinamento.md` (já existente). Após refinamento aprovado, AUQ retorna automaticamente. |
   | **Pausar cadeia** | Despacha Gerente `FLUXO: pausar-cadeia` com caminho do plano + última filha concluída. Plano grava `status-cadeia: pausado`. Maestro avisa: "Cadeia pausada. `/ola-maestro` na próxima sessão lembra de retomar." Encerra fluxo. |

3. Se "Aprovar e seguir": despachar próxima filha (igual modo automático passo 1-2).
4. Se "Pausar cadeia": encerrar sem despachar.
5. Se "Pedir ajuste": fluxo-refinamento.md cuida; após aprovar, voltar pro AUQ neste passo.

**Quando última filha fecha (modo guiado):** mostrar resumo final ao usuário + wikilinks + tabela.

**Cap de pausas:** sem cap. Usuário pode pausar quantas vezes quiser entre filhas.

## Protocolos de falha

### QA reprova

1. Despachar Gerente com `FLUXO: criar-revisao` — Gerente cria tarefa-filha de categoria `revisao` com agente herdado da tarefa pai (rodadas 1-2) ou `agente: usuario` (rodada 3) e inicializa `_ultima-correcao-por: ~` no frontmatter da filha.
2. **Especialista da tarefa-filha** é re-despachado via `Agent()` com feedback específico do QA. Especialista aplica via `Edit` no `caminho-do-artefato` existente. **Maestro NUNCA Edit em corpo** (ver `plugin/skills/maestro/limites-maestro.md` — toda correção pós-Revisor passa pelo especialista, sem exceção pra "menor", sem gradiente "estrutural"; B-S55-47 escala recursivamente quando "concern menor" vira exceção).
3. QA roda de novo no novo resultado da tarefa-filha.
4. **Contador visível pro usuário** (rodadas 1, 2, 3 — ver `limites-maestro.md` seção 3):
   - Rodada 1: "QA pediu ajuste. Voltando pra [especialista]."
   - Rodada 2: "QA pediu mais um ajuste. Voltando pra [especialista] (rodada 2 de 3 antes de te perguntar o que fazer)."
5. **Na 3a reprova, abortar pipeline e perguntar ao usuário via `AskUserQuestion`:**
   - **Revisar o pedido** (usuário reescreve)
   - **Ver o último rascunho** (entrega parcial pra inspeção)
   - **Forçar entrega com pendência** (loga `pendencias-aceitas` preenchido + seção "Pendências aceitas pelo usuário" + append em `memorias/pendencias-aceitas/historico.md` — ver fluxo-needs.md seção governança). Maestro confirma: "Salvei como está. Anotei no histórico de pendências aceitas pra você revisar depois."
6. Quando QA aprova a tarefa-filha, despachar Gerente `concluir-tarefa` da filha com payload `_ultima-correcao-por: <slug-especialista>`. Tripwire do Gerente (ver `protocolo-agent.md` §8) valida autoria — retorna BLOCKED se autoria errada.

### Revisor reprova

Mesma lógica do "QA reprova" — `criar-revisao` → especialista da filha aplica via Edit → Maestro NUNCA Edit em corpo → contador 1/3, 2/3, 3/3 → AUQ na rodada 3 → `_ultima-correcao-por` no payload de conclusão. Na 3a reprova, oferecer também gravar preferência de estilo em `memorias/preferencias-estilo.md` pra não reincidir.

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
5. **Maestro NUNCA `Edit` em corpo de artefato existente** — toda correção pós-QA/Revisor passa pelo especialista da tarefa-filha de revisão (ver `plugin/skills/maestro/limites-maestro.md`). Tripwire do Gerente no `concluir-tarefa` valida e retorna BLOCKED se autoria errada (B-S55-47).
6. **Item 5.bis preserva pipeline completo das filhas seguintes.** Modo automático NÃO encurta o pipeline interno de cada filha — todas continuam rodando os 5 itens (Gerente cria → especialista → QA + Revisor → Gerente fecha) via `Agent()` isolado. "Automático" só elimina o gate humano entre filhas, nunca os agentes (D8 da spec, aprendizado #61).
