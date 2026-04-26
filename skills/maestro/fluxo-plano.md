# Fluxo de Plano v2

Sub-skill lida pelo Maestro via `Read` quando o classificador retorna `tipo=Plano`.

Plano = conjunto de tarefas coordenadas (lançamento, campanha, funil, escada-de-valor, lead-magnet, calendário social, plano de tráfego, pesquisa multi-fonte, ou múltiplas entregas enumeradas). Cada tarefa-filha depois roda como `Entrega` com seu próprio fluxo.

## Concorrência: 1 plano por vez

Maestro processa **um plano por vez**. Se segundo pedido de plano chegar antes do primeiro fechar (em qualquer checkpoint), Maestro avisa:

> "Plano X aguardando no Checkpoint Y. Aguarde fechar ou cancele primeiro."

Oferece `AskUserQuestion` com 2 opções: "Aguardar plano X fechar" / "Cancelar plano X e seguir com novo pedido".

## TodoWrite obrigatório (6 itens fixos)

1. `Brainstorm de escopo com usuário`
2. `Especialista decompõe plano em memória`
3. `Checkpoint 1 — usuário valida overview`
4. `Gerente persiste plano.md (rascunho)`
5. `Checkpoint 2 — usuário valida plano escrito`
6. `Gerente materializa N tarefas-filhas + escolhe modo de execução`

## Roteamento por tipo de plano

Maestro classifica o tipo de plano no brainstorm da Fase 1 e despacha o especialista-dono via mapa fixo:

| Tipo de plano | Especialista-dono |
|---|---|
| Lançamento, funil, escada-de-valor, lead-magnet | Estrategista |
| Campanha de copy isolada, sequência email, VSL, página de vendas | Copywriter |
| Calendário editorial, mix social, conteúdo orgânico, série de posts | Mídias Sociais |
| Plataforma de marca, naming, identidade | Marca |
| Plano de tráfego isolado, otimização de campanha paga | Performance |
| Pesquisa multi-fonte (concorrente, audiência, mercado) | Pesquisador |
| **Plano composto / cross-domain** (toca 2+ domínios estratégicos — ex: lançamento com webinário + tráfego + email + posts) | **Estrategista** (decompositor universal) — cada filha aponta `Agente:` apropriado pra execução |
| **Verdadeiramente fora do mapa** (raríssimo — pedido sem componente estratégico claro) | Maestro pergunta via `AskUserQuestion` |

**Regra cross-domain:** quando o pedido toca 2+ domínios, default é Estrategista. Usuário não precisa escolher arquitetura.

## Passo a passo

### Fase 1 — Brainstorm de escopo

1. Identificar o tipo de plano a partir do pedido + dialogar com o usuário pra fechar:
   - Objetivo do plano
   - Prazo aproximado
   - Quantas "peças" ou "estágios"
   - Restrições (orçamento, canais, tom)
2. Usar `AskUserQuestion` quando houver opções finitas (ex: escolha de funil — VSL, webinar, escada).
3. Classificar o tipo de plano e identificar o especialista-dono via mapa.
4. Marcar item 1 `completed` quando escopo estiver claro o suficiente pro especialista decompor.

### Fase 2 — Decomposição em memória (Especialista-dono)

1. Despachar o especialista-dono via `Agent()` com:
   - Bloco CONTEXTO conforme `protocolo-contexto.md` rota "Decompor plano" (padrão dos 6 + extensões do especialista).
   - Bloco INSTRUÇÃO contendo `MODO: decompor-plano` + briefing do usuário + tipo de plano identificado.
2. Especialista segue `protocolo-decompor-plano.md` e devolve bloco `---RESUMO-PRO-PLAN-MODE---` com raciocínio + tabela + modo de execução inferido.
3. Maestro guarda o último report até a escolha do usuário no Checkpoint 1.
4. Marcar item 2 `completed` quando especialista retornou.

### Fase 3 — Checkpoint 1 (overview rápido)

**Canal de aprovação:**

- **Primário:** `EnterPlanMode` nativo do Claude Code, alimentado com o bloco `RESUMO-PRO-PLAN-MODE` formatado em Markdown. Detecção de capability em runtime.
- **Fallback:** se `EnterPlanMode` não disponível, `AskUserQuestion` com 3 opções:
  - **Seguir** — vai pra Fase 4
  - **Ajustar** — entra em loop conversacional (cap de 5 iterações)
  - **Cancelar** — encerra sem rastro no vault

**Loop "Ajustar" (cap de 5 iterações):**

1. Maestro pergunta "o que ajustar?" em texto livre.
2. Re-despachar mesmo especialista via `Agent()` com:
   - Bloco CONTEXTO idêntico ao despacho original (prompt cache hit ~80% redução).
   - Bloco INSTRUÇÃO contendo `MODO: decompor-plano` + `AJUSTE PEDIDO: [texto livre do usuário]` + última versão do `RESUMO-PRO-PLAN-MODE`.
3. Especialista re-decompõe, devolve nova versão.
4. Maestro reapresenta Checkpoint 1.
5. **Cap:** após 5 iterações, força `AskUserQuestion`: "Regerar / Cancelar / Continuar mesmo assim (custo nota)".

**Marcar item 3 `completed`** quando usuário escolher Seguir ou Cancelar.

### Fase 4 — Persistir plano.md (Gerente)

1. Despachar Gerente em **Fluxo 4b** via `Agent()` passando:
   - Briefing original do usuário (Pedido original).
   - Bloco `RESUMO-PRO-PLAN-MODE` aprovado.
   - Especialista decompositor (pra registrar no Histórico).
   - Solicitante (do contexto).
   - `regera: "[[planos/<slug-anterior>]]"` se este plano vem de "Regerar" no CK2 anterior; senão `~`.
2. Gerente cria `plano.md` em rascunho com tabela textual de tarefas previstas no corpo. **Não materializa filhas ainda.**
3. Marcar item 4 `completed` quando Gerente retorna `PLANO-PERSISTIDO: [caminho]`.

### Fase 5 — Checkpoint 2 (revisão do plano persistido)

**Mensagem do Maestro pro usuário:**

```
✅ Plano pronto pra revisão.

📄 [[planos/<slug>]]
   Dá uma lida no plano. Quando voltar, me diz o que prefere.

Estado:
- Plano em rascunho, ainda sem tarefas-filhas materializadas
- N tarefas previstas no documento
- M dependências detectadas

💡 Recomendação de execução: [MODO]
   Razão: [justificativa em linguagem simples]
```

**`AskUserQuestion` #1 — 4 opções:**

- **Aprovar** → vai pra Fase 6 + AUQ #2 (modo de execução)
- **Ajustar** → loop conversacional com mapa "quem aplica"
- **Regerar** → cancela plano.md (sem cascata, filhas não existem) + cria novo com `regera: "[[planos/<slug-anterior>]]"`. Volta pra Fase 2.
- **Cancelar** → cancela plano.md, encerra

**Mapa "quem aplica" no loop Ajustar:**

| Tipo de ajuste | Quem o Maestro despacha |
|---|---|
| Renomear título da tarefa-filha N | Gerente — Fluxo 4c |
| Trocar agente responsável | Gerente — Fluxo 4c |
| Adicionar tarefa nova | Gerente — Fluxo 4d |
| Remover tarefa | Gerente — Fluxo 4e |
| Reordenar / mexer em `Depende de` | Gerente — Fluxo 4c |
| Mudar campo operacional do plano | Gerente — Fluxo 4c |
| Mudar `tipo:` do plano (estrutural) | Gerente — Fluxo 4f → reporta NEEDS_CONTEXT → Maestro pergunta refazer decomposição |
| "Repensa essa abordagem" / "muda a estratégia da tarefa N" | Especialista-dono em modo decompor-plano (re-roda Fase 2) |
| Edição manual no Obsidian + "ajustei à mão, revalida" | Gerente — Fluxo 4f |

Após cada ajuste, reapresentar Checkpoint 2. Sai do loop só com Aprovar / Regerar / Cancelar. Sem cap duro (cada iter é Sonnet barato), mas após 5 ciclos sugerir "talvez seja melhor Regerar?".

**Marcar item 5 `completed`** quando usuário escolher Aprovar / Regerar / Cancelar.

### Fase 6 — Materializar tarefas-filhas (Gerente) + modo de execução

1. Despachar Gerente em **Fluxo 5** via `Agent()` passando caminho do plano aprovado.
2. Gerente materializa N tarefas-filhas + N cascas (com campos operacionais conforme tabela), substitui seção textual por Dataview, arquiva tabela no Histórico.
3. Maestro mostra: `✅ Tarefas criadas.`
4. **AskUserQuestion #2 — modo de execução (4 opções):**
   - **Paralelo** — todas em paralelo simultâneo
   - **Paralelo com batches** — independentes em batch 1; dependentes esperam
   - **Sequencial** — uma por vez, na ordem de dependência
   - **Sob demanda** — usuário dispara tarefa por tarefa
5. **Recomendação destacada** com justificativa, conforme regra de inferência:

   | Situação | Recomendação |
   |---|---|
   | Zero dependências cruzando filhas | **Paralelo** |
   | 1+ dependência mas a maioria das filhas independentes (≥60% sem `depende-de`) | **Paralelo com batches** |
   | Dependências cobrem ≥60% das filhas (cadeia longa) | **Sequencial** |
   | Não inferível | Apresentar sem destacar; usuário escolhe |

   "Sob demanda" **nunca** é recomendação automática.

6. Conforme escolha, executar:
   - **Paralelo:** abrir múltiplos `Agent()` simultâneos pra todas as filhas
   - **Paralelo com batches:** abrir Agent() concorrentes pras filhas independentes; bloquear dependentes até batch 1 fechar
   - **Sequencial:** Agent() pra 1ª filha; próxima só depois de fechar
   - **Sob demanda:** sair do plano; usuário dispara tarefa por tarefa quando quiser

7. Cada tarefa-filha **roda como Entrega completa** — TodoWrite próprio de 5 itens, pipeline completo. Ver `fluxo-entrega.md`.

8. Tracking do plano continua em `plano.md` (Gerente atualiza checkbox de cada tarefa via Fluxo 2 conforme completam).

9. Marcar item 6 `completed` após escolha do modo de execução.

## Regras absolutas

1. **Plano NÃO passa por QA nem Revisor no nível do plano** — validação acontece em cada tarefa-filha quando executa.
2. **Plano sem tarefas no `RESUMO-PRO-PLAN-MODE`** = inválido; Maestro deve abortar Fase 2 e pedir novo briefing.
3. **Aprovação do usuário é explícita** via `EnterPlanMode` (CK1) ou `AskUserQuestion` (CK1 fallback + CK2) — nunca prosseguir sem.
4. **Checkpoint 1 é em memória** — zero rastro no vault se rejeitar.
5. **Checkpoint 2 cancela só plano.md** — filhas não existem ainda, sem cascata.
6. **Tarefa-filha cancelada não invalida o plano**; tarefa-filha bloqueada (NEEDS_*) pausa o plano.
7. **Cross-domain → Estrategista** (decompositor universal). Usuário não escolhe arquitetura.
8. **Cap de 5 iterações no loop Ajustar do CK1** — após 5, força AUQ Regerar/Cancelar/Continuar.
