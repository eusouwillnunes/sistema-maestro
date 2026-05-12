# Fluxo de Plano (2 gates)

Sub-skill lida pelo Maestro via `Read` quando o classificador retorna `tipo=Plano`. Substituiu o `EnterPlanMode` nativo por 2 gates explícitos com AUQs estruturados (Sessão 60, spec `2026-04-29-fluxo-plano-2-gates-design`).

Plano = conjunto de tarefas coordenadas (lançamento, campanha, funil, escada-de-valor, lead-magnet, calendário social, plano de tráfego, pesquisa multi-fonte, ou múltiplas entregas enumeradas). Cada tarefa-filha depois roda como `Entrega` com seu próprio fluxo.

> [!important] Defesa textual contra escrita direta em `planos/`
> Especialistas **NUNCA** chamam Write/Edit/MultiEdit em `planos/*.md`. Decisão registrada em `protocolo-decompor-plano.md` Regra invariante 1. Defesa é convencional (template + protocolo + agent files), NÃO via hook (PreToolUse libera tudo de subagent — `maestro-orquestra.py:105-106`). Final reviewer cross-grepa Write em `planos/` fora do Gerente em todo merge.

## Concorrência: 1 plano por vez

Maestro processa **um plano por vez**. Se segundo pedido de plano chegar antes do primeiro fechar (em qualquer gate), Maestro avisa:

> "Plano X aguardando no Gate Y. Aguarda fechar ou cancela pra seguir?"

`AskUserQuestion` com 2 opções: "Aguardar plano X fechar" / "Cancelar plano X e seguir com novo pedido".

**Recuperação após sessão fechada entre gates:** `/ola-maestro` detecta planos em `rascunho` com `data-aprovacao: ~` (Gate 2 pendente) e avisa o usuário ao retornar.

## TodoWrite obrigatório (8 itens fixos)

1. `Aviso de classificação implícita ao usuário (se aplicável)`
2. `Especialista executa Fase 1.5 (pré-validação de contexto)`
3. `Especialista produz overview no chat (Fase 1)`
4. `Gate 1 — usuário valida Objetivo / Contexto / Peças`
5. `Especialista produz bloco DECOMPOSICAO-PLANO (Fase 2)`
6. `Maestro valida bloco (Fase 2.5: raciocínio + tabela ≥1 + agentes válidos)`
7. `Gerente persiste plano.md em rascunho (Fluxo 4b)`
8. `Gate 2 — usuário valida plano escrito + materializa filhas (se aprovado)`

> [!warning] Gate 1 SEMPRE roda, sem exceção.
> Mesmo em pedidos detalhados ou repetidos, o overview no chat é obrigatório. Skip explícito ou heurístico abre zona de racionalização do modelo (D9 da spec).

## Detecção implícita de plano

Classificador detecta plano-worthy SEM o usuário precisar dizer "criar plano". Pedidos com **conceitos compostos** disparam automaticamente `tipo=Plano`.

| Pedido do usuário | Classificação | Especialista decompositor |
|---|---|---|
| "criar lançamento da Mentoria X" | Plano (composto) | Estrategista |
| "fazer campanha de Black Friday" | Plano (composto) | Estrategista |
| "montar funil de webinário" | Plano (composto) | Estrategista |
| "criar plano de tráfego" | Plano (composto) | Performance |
| "preencher identidade da empresa" | Plano (multi-entrega no mesmo domínio) | Marca |
| "criar 5 emails de aquecimento" | Plano (multi-entrega) | Copywriter |
| "calendário editorial do mês" | Plano (multi-entrega) | Mídias Sociais |
| "escrever uma headline" | Entrega (não-plano) | Copywriter via `fluxo-entrega.md` |
| "fazer 1 reel" | Entrega (não-plano) | Mídias Sociais via `fluxo-entrega.md` |

**Regra de fronteira:**
- 2+ artefatos coordenados → Plano.
- 1 artefato isolado → Entrega.
- Cross-domain (2+ domínios estratégicos) → Plano com Estrategista decompositor.

**Casos ambíguos:** "criar headline e subheadline" trata 2 elementos coordenados como Plano. Modificador permissivo do usuário ("é coisa simples, não precisa de plano") rebaixa pra Entrega.

## Aviso de classificação implícita

Quando classificador decide Plano automático em pedido onde usuário não disse "plano", Maestro avisa **antes de despachar especialista**:

> *"Certo! Vou estruturar isso como um plano (N peças coordenadas). Se você prefere entregas soltas sem estrutura formal, me avisa agora: 'não precisa de plano, só quero as N peças mesmo'."*

**Quando exibir:**
- ✅ Pedidos com conceitos compostos ("lançamento", "campanha", "calendário", "funil", "identidade")
- ✅ Pedidos com cardinalidade explícita ≥2 ("3 emails", "5 posts")
- ❌ Pedidos com palavra "plano" explícita (usuário sabe)
- ❌ Cross-domain óbvios (lançamento + tráfego + email — sempre plano)

Após o aviso, Maestro aguarda 1 turno do usuário. Sem objeção → segue com Plano. Modificador permissivo → rebaixa pra Entrega.

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

### Fase 1.5 — Pré-validação de contexto (especialista)

1. Despachar especialista-dono via `Agent()` em `MODO: decompor-plano-fase-1`:
   - Bloco CONTEXTO completo (5 templates de identidade + decisões + pesquisas) conforme `protocolo-contexto.md` rota "Decompor plano".
   - Bloco INSTRUÇÃO: `MODO: decompor-plano-fase-1` + briefing do usuário + tipo de plano identificado.
2. Especialista checa critérios críticos por tipo (tabela em `protocolo-decompor-plano.md` Fase 1.5).
3. **Se critério crítico falta:** especialista reporta `NEEDS_CONTEXT` ou `NEEDS_DATA`. Maestro encaminha conforme `fluxo-needs.md`. **Não conta como volta de em-revisao.** Quando contexto for resolvido, voltar pro passo 1.
4. **Se contexto OK:** especialista segue pra Fase 1.

### Fase 1 — Especialista produz overview no chat

1. Mesma chamada da Fase 1.5 (especialista já está rodando).
2. Especialista produz no chat (não em arquivo) resposta com 3 campos fixos: Objetivo / Contexto utilizado / Peças do plano. Formato canônico em `protocolo-decompor-plano.md` Fase 1.
3. Maestro guarda overview em memória até Gate 1.
4. Marcar item 3 do TodoWrite `completed`.

### Gate 1 — Maestro valida overview com usuário

**Mensagem 1 (recap):** Maestro repete overview do especialista no chat (mesmo conteúdo, sem reformatar).

**Mensagem 2 (AUQ separada):**

`AskUserQuestion` com 3 sub-perguntas + 3 opções:

| Pergunta | Opção 1 | Opção 2 | Opção 3 |
|---|---|---|---|
| O **objetivo** está certo? | sim | ajustar | cancelar |
| O **contexto** está certo? | sim | ajustar | cancelar |
| As **peças** fazem sentido? | sim | ajustar | cancelar |

(Se Claude Code não suporta 3 perguntas independentes, usar AUQ única "Aprovar tudo / Ajustar / Cancelar" + texto livre se Ajustar.)

**Cancelar no Gate 1:** plano ainda não existe no vault. Encerra sem rastro.

**Ajustar:** texto livre do usuário. Maestro re-despacha especialista em `MODO: decompor-plano-fase-1` com `INSTRUÇÃO: AJUSTE PEDIDO: [texto]` + último overview. Cache hit ~80%. Volta pro Gate 1.

**Aprovar:** marcar item 4 do TodoWrite `completed`. Avança pra Fase 2.

### Fase 2 — Especialista produz bloco DECOMPOSICAO-PLANO

1. **Segunda chamada do especialista** via `Agent()` em `MODO: decompor-plano-fase-2`:
   - Bloco CONTEXTO **idêntico** ao da Fase 1 → prompt cache hit ~80% redução.
   - Bloco INSTRUÇÃO: `MODO: decompor-plano-fase-2` + overview aprovado (pra especialista lembrar promessas) + briefing original.
2. Especialista produz bloco delimitado `---DECOMPOSICAO-PLANO--- ... ---END-DECOMPOSICAO-PLANO---` com raciocínio + tabela + modo de execução.
3. Maestro guarda bloco em memória até Fase 2.5.
4. Marcar item 5 do TodoWrite `completed`.

### Fase 2.5 — Maestro valida bloco

Maestro checa programaticamente:

- Raciocínio preenchido (não-vazio).
- Tabela tem ≥1 linha de tarefa.
- Cada tarefa tem agente válido (estrategista | copywriter | marca | midias-sociais | performance | pesquisador).
- Cada tarefa tem tipo de artefato válido (existe em `plugin/core/templates/artefatos/`).
- Modo de execução é um de: paralelo | paralelo-com-batches | sequencial | sob-demanda.

**Falha em qualquer:** Maestro re-despacha especialista pra refazer com `INSTRUÇÃO: bloco inválido — corrigir [item]`. **Não conta como volta de em-revisao** — é validação técnica.

**Sucesso:** marcar item 6 `completed`. Avança pra Fase 3.

### Fase 3 — Gerente persiste plano.md em rascunho

1. Despachar Gerente em **Fluxo 4b** via `Agent()` passando:
   - Briefing original.
   - Overview aprovado no Gate 1.
   - Bloco `DECOMPOSICAO-PLANO` validado.
   - Especialista decompositor (pra registrar).
   - Solicitante (do contexto).
   - `regera: "[[planos/<slug-anterior>]]"` se este plano vem de "Regerar" no Gate 2 anterior; senão `~`.
2. Gerente captura `Bash date` ANTES da escrita, escreve plano.md alinhado com template canônico, registra `gate-1-aprovado` no Histórico.
3. Marcar item 7 `completed` quando Gerente retorna `PLANO-PERSISTIDO: [caminho]`.

### Gate 2 — Maestro convida usuário pra revisar plano escrito

**Mensagem 1 (convite com wikilink + slug literal):**

```
Plano pronto pra revisão em [[planos/<slug>]] ({projeto}/planos/<slug>.md).
Abre no Obsidian (leva 2-5 min). Quando voltar, me diz: aprova, quer ajustar, regerar, ou cancela?
```

**Mensagem 2 (AUQ separada — 4 opções):**

| Opção | Resultado |
|---|---|
| **Aprovar** | Maestro despacha Fluxo 5 (materializa filhas), `status: aprovado`, Histórico: `gate-2-aprovado` |
| **Ajustar** | AUQ secundária com mapa "quem aplica" — mecânico (Gerente direto) ou estratégico (re-despacha especialista) |
| **Regerar** | Cancela plano atual (`status: cancelado`, `motivo: regerado`) + cria novo via Fluxo 4-regerar com `regera:` apontando pro anterior. **Não conta como volta.** |
| **Cancelar** | Plano vira `cancelado`, `motivo-cancelamento` preenchido, Histórico: `gate-2-cancelado`. Encerra. |

**AUQ secundária do "Ajustar" — mapa "quem aplica":**

| Tipo de ajuste | Quem aplica | Conta como volta? |
|---|---|---|
| Renomear tarefa | Gerente Fluxo 4c (mecânico) | ❌ |
| Trocar agente | Gerente Fluxo 4c (mecânico) | ❌ |
| Adicionar tarefa | Gerente Fluxo 4d (mecânico) | ❌ |
| Remover tarefa | Gerente Fluxo 4e (mecânico) | ❌ |
| Reordenar `Depende de` | Gerente Fluxo 4c (mecânico) | ❌ |
| Mudar campo operacional do plano | Gerente Fluxo 4c (mecânico) | ❌ |
| "Repensa essa abordagem" / "muda estratégia da peça N" | Especialista re-decompõe (Fluxo 4-revisao) | ✅ +1 |
| Editou plano à mão e pediu revalidar | Gerente Fluxo 4f (mecânico) | ❌ |

**Cap de 3 voltas em-revisao** (apenas ajuste estratégico):

- Volta 1-3: AUQ Gate 2 mostra "Ajustar (volta N de 3)".
- Tentativa de volta 4: AUQ extra:
  > "Você já ajustou 3 vezes. Continuar (regera plano novo do zero) / Aprovar como está / Cancelar?"

**Maestro recalcula contador via grep do Histórico** (anti-burla):
- Antes de cada AUQ Gate 2, rodar `grep -c "gate-2-feedback" {caminho-do-plano}`.
- Usar o maior valor entre o frontmatter `voltas-em-revisao` e o count do Histórico.

### Fase 4 — Materializar tarefas-filhas (Aprovar no Gate 2)

1. Despachar Gerente em Fluxo 5 via `Agent()` passando caminho do plano aprovado.
2. Gerente materializa N tarefas-filhas + cascas, escreve `data-aprovacao` + `status: aprovado` + `gate-2-aprovado` no Histórico.
3. Maestro mostra: `✅ Tarefas criadas.`
4. **Detecção de cadeia de identidade:** se `plano.md` tem `modo-cadeia: pendente` no frontmatter, **pular** o AUQ #2 padrão (passos 5-6) e ir direto pra **Fase 4.5**. Modo Sequencial é forçado por contrato (ver `protocolo-decompor-plano.md` seção "Decomposição da identidade").
5. **AskUserQuestion #2 — modo de execução (4 opções):**
   - **Paralelo** — todas em paralelo simultâneo
   - **Paralelo com batches** — independentes em batch 1; dependentes esperam
   - **Sequencial** — uma por vez, na ordem de dependência
   - **Sob demanda** — usuário dispara tarefa por tarefa
6. **Recomendação destacada** com justificativa, conforme regra de inferência:

   | Situação | Recomendação |
   |---|---|
   | Zero dependências cruzando filhas | **Paralelo** |
   | 1+ dependência mas a maioria das filhas independentes (≥60% sem `depende-de`) | **Paralelo com batches** |
   | Dependências cobrem ≥60% das filhas (cadeia longa) | **Sequencial** |
   | Não inferível | Apresentar sem destacar; usuário escolhe |

   "Sob demanda" **nunca** é recomendação automática.

7. Conforme escolha, executar:
   - **Paralelo:** abrir múltiplos `Agent()` simultâneos pra todas as filhas
   - **Paralelo com batches:** abrir Agent() concorrentes pras filhas independentes; bloquear dependentes até batch 1 fechar
   - **Sequencial:** Agent() pra 1ª filha; próxima só depois de fechar
   - **Sob demanda:** sair do plano; usuário dispara tarefa por tarefa quando quiser

8. Cada tarefa-filha **roda como Entrega completa** via `fluxo-entrega.md`.

9. Tracking continua em `plano.md` (Gerente atualiza via Fluxo 2 conforme completam).

10. Marcar item 8 `completed` após escolha do modo de execução.

### Fase 4.5 — AUQ extra de cadência (só identidade, modo-cadeia: pendente)

Quando `plano.md` tem `modo-cadeia: pendente`, Maestro abre AUQ específico **antes** de despachar a 1ª filha:

**Mensagem 1 (preâmbulo):**

> A identidade vai ser preenchida em cadeia sequencial — cada template alimenta o próximo (Círculo Dourado → História → Posicionamento → Perfil → Personalidade → Tom → Manifesto).

**Mensagem 2 (AUQ separada):**

| Opção | Resultado |
|---|---|
| **Guiado** | Após cada template aprovado, paro pra você revisar antes de liberar o próximo. 7 pausas. Erro num template não contamina os 6 seguintes. |
| **Automático** | Rodo os 7 em sequência sem pausar. Você revisa no fim. Mais rápido, mas erro de tom no Círculo Dourado reverbera nos 6 seguintes. |

**Após escolha:**

1. Despachar Gerente em `FLUXO: gravar-modo-cadeia` com a escolha (`guiado` ou `automatico`).
2. Aguardar retorno `MODO-CADEIA-GRAVADO`.
3. Avançar pra Fase 4 passo 7+ com modo Sequencial forçado: Agent() pra 1ª filha; próxima só depois de fechar.

**Cancelamento mid-AUQ:** se usuário responde "cancela", marcar plano como `status: cancelado, motivo-cancelamento: cancelado-pelo-usuario` via Gerente Fluxo 13 (cancelar plano) e não despachar nenhuma filha.

## Regras absolutas

1. **Plano NÃO passa por QA nem Revisor no nível do plano** — validação acontece em cada tarefa-filha quando executa.
2. **Plano sem tarefas no `DECOMPOSICAO-PLANO`** = inválido (regra 6 do `protocolo-decompor-plano.md`). Maestro rejeita na Fase 2.5 e re-despacha. **Não conta como volta.**
3. **Aprovação do usuário é explícita** via `AskUserQuestion` em ambos os gates — nunca prosseguir sem.
4. **Gate 1 é em memória** — zero rastro no vault se cancelar.
5. **Gate 2 cancela só plano.md** — filhas não existem ainda, sem cascata.
6. **Tarefa-filha cancelada não invalida o plano**; tarefa-filha bloqueada (NEEDS_*) pausa o plano.
7. **Cross-domain → Estrategista** (decompositor universal). Usuário não escolhe arquitetura.
8. **Cap de 3 voltas em em-revisao** — após 3, AUQ extra (Continuar regera / Aprovar / Cancelar). Maestro recalcula contador via grep do Histórico (anti-burla via Properties).
9. **Gate 1 SEMPRE roda**, sem skip explícito ou heurístico (D9 da spec).
10. **Especialista NUNCA chama Write/Edit em `planos/*.md`** — defesa textual (D13 da spec). Final reviewer cross-grepa.
11. **Cadeia de identidade força modo Sequencial.** AUQ #2 padrão é pulado quando `modo-cadeia: pendente`. Em vez disso, AUQ extra (Fase 4.5) coleta `guiado` ou `automatico`. Não há override pra rodar cadeia em paralelo.
