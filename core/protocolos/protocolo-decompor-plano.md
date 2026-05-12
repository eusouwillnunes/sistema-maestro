---
description: Protocolo do modo "Decompor plano" para os 6 especialistas que decompõem planos compostos no Grupo B
tags:
  - "#maestro/protocolo"
---

# Protocolo de Decomposição de Plano

> [!info] Protocolo compartilhado do Sistema MAESTRO.
> Este documento é referenciado via `Aplica:` por todos os especialistas que podem ser despachados como decompositores de plano (Fase 2 do Fluxo de Plano v2).

## Objetivo

Definir como o especialista-dono de um tipo de plano decompõe um pedido em tarefas atômicas e devolve o resultado em memória pro Maestro alimentar o Gate 1 (overview no chat) e, após aprovação, o Gate 2 (plano escrito no vault).

---

## Quando este modo é acionado

O Maestro despacha o especialista em uma de **três variantes** do modo Decompor plano:

| MODO | Quando | Saída esperada |
|---|---|---|
| `decompor-plano-fase-1` | Classificação como Plano + identificação do especialista (Fase 1 do `fluxo-plano.md`) | Overview no chat (Objetivo / Contexto / Peças) |
| `decompor-plano-fase-2` | Após Gate 1 aprovado pelo usuário | Bloco `DECOMPOSICAO-PLANO` completo (raciocínio + tabela + modo de execução) |
| `decompor-plano-em-revisao` | Após Gate 2 com escolha "Ajustar estratégico" pelo usuário | Bloco `DECOMPOSICAO-PLANO` revisto incorporando feedback |

Em todos os 3 modos:
- Bloco CONTEXTO segue `protocolo-contexto.md` rota "Decompor plano".
- Chamadas 1 e 2 do mesmo plano usam **CONTEXTO idêntico** — prompt cache hit ~80%.
- Iteração em Gate 1 ("Ajustar") = nova chamada de fase-1 com `INSTRUÇÃO: AJUSTE PEDIDO: [texto]` + última versão do overview. Cache hit também.

---

## Fase 1 — Overview no chat (`MODO: decompor-plano-fase-1`)

Especialista produz no chat (não em arquivo) uma resposta com 3 campos fixos:

```markdown
**Objetivo:** [1-3 frases — o que o usuário quer atingir com o plano]

**Contexto utilizado:**
- [[area/wikilink-1]]
- [[area/wikilink-2]]
- [[memorias/decisoes]] (decisões 044, 052)

**Peças do plano:**
1. [slug-da-peca-1] (Agente: Marca)
2. [slug-da-peca-2] (Agente: Copywriter)

Antes de eu gravar o plano completo no Obsidian, deixa eu confirmar:
- O **objetivo** está certo?
- O **contexto** que vou usar está certo? (faltou algum arquivo importante?)
- As **peças** que vou criar fazem sentido?
```

**Regras:**
- Termo "Peças do plano" (não "Entregáveis").
- Cada peça mostra o agente entre parênteses (transparência pro usuário).
- Especialista NÃO escreve em `planos/*.md` na Fase 1 — só responde no chat.
- Maestro conduz Gate 1 (AUQ separado em mensagem 2). Iteração "Ajustar" = nova chamada fase-1 com `INSTRUÇÃO: AJUSTE PEDIDO: [texto]`.

---

## Fase 1.5 — Pré-validação de contexto (bloqueante)

Antes de produzir overview, especialista verifica critérios críticos por tipo de plano:

| Tipo de plano | Critérios críticos |
|---|---|
| Lançamento, funil, escada-de-valor, lead-magnet | Identidade preenchida (círculo-dourado + posicionamento mínimo) · produto referenciado existe |
| Campanha de copy, sequência email, VSL, página de vendas | Identidade preenchida · produto referenciado · pesquisa de público (recomendado) |
| Calendário editorial, mix social | Identidade preenchida · pesquisa de público |
| Plataforma de marca, naming, identidade | Briefing claro · pesquisa de mercado/concorrentes (se aplicável) |
| Plano de tráfego | Identidade preenchida · produto referenciado · pixel/contas verificadas |
| Pesquisa multi-fonte | Briefing claro · escopo definido (mercado / audiência / concorrente) |

**Se algum critério crítico falta:**
- Especialista reporta `NEEDS_CONTEXT` (info do usuário direto) ou `NEEDS_DATA` (info via entrevista/pesquisa) conforme `protocolo-agent.md`.
- Maestro encaminha conforme protocolo padrão.
- **Não conta como volta de em-revisao** — bloqueio pré-fluxo.

**Se contexto OK:** especialista segue pra produzir overview.

---

## Formato do retorno: bloco DECOMPOSICAO-PLANO (Fase 2)

O especialista devolve dentro do report do Agent() um bloco delimitado quando rodando `MODO: decompor-plano-fase-2` ou `decompor-plano-em-revisao`:

```
---DECOMPOSICAO-PLANO---
## Raciocínio da decomposição

[3-5 linhas explicando: por que essa decomposição, qual modelo/funil/campanha foi assumido,
dependências-chave entre tarefas. Linguagem natural, sem formatação extra.]

## Tarefas

| # | Tarefa | Agente | Tipo de artefato | Depende de |
|---|--------|--------|------------------|------------|
| 1 | [título da tarefa] | [especialista] | [tipo do artefato] | — ou [# da pai] |
| 2 | ... | ... | ... | ... |

## Modo de execução inferido

[paralelo | paralelo-com-batches | sequencial | sob-demanda]

Razão: [linguagem simples explicando a inferência]

## Cadeia de identidade

[sim | não]
---END-DECOMPOSICAO-PLANO---
```

A seção "Cadeia de identidade" com valor `sim` é declarada **apenas** pela Marca quando decompõe pedido "preencher identidade da empresa" seguindo a tabela canônica de 7 templates encadeados (ver seção "Decomposição da identidade" abaixo). Para qualquer outro plano, o valor é `não` ou a seção pode ser omitida (Gerente trata ambos como `~` no frontmatter do plano).

### Colunas obrigatórias da tabela

- **#** — número sequencial (1, 2, 3, ...)
- **Tarefa** — título imperativo curto da tarefa-filha
- **Agente** — um de: Estrategista, Copywriter, Marca, Mídias Sociais, Performance, Pesquisador
- **Tipo de artefato** — um de: lancamento, funil, campanha, escada-de-valor, lead-magnet, analise-performance, entrega-generica, pesquisa
- **Depende de** — `—` (independente) ou `[# da filha-pai]` (dependência simples) ou `[# A, # B]` (múltiplas)

### Colunas opcionais por especialista (extensões de domínio)

Cada especialista pode adicionar 1-2 colunas opcionais quando relevantes:
- **Mídias Sociais:** `Formato` (reels, carrossel, story, etc.)
- **Performance:** `Canal` (Meta, Google, TikTok, etc.)
- **Pesquisador:** `Fonte-tipo` (concorrente, audiência, mercado, etc.)

Estrategista, Copywriter e Marca não têm colunas opcionais por contrato — extensões viram texto no raciocínio quando aplicável.

### Regra de inferência do modo de execução

| Situação | Recomendação |
|---|---|
| Zero dependências cruzando filhas | **paralelo** |
| 1+ dependência mas a maioria das filhas independentes (≥60% sem `Depende de`) | **paralelo-com-batches** |
| Dependências cobrem ≥60% das filhas (cadeia longa) | **sequencial** |
| Não inferível | omitir o campo "Modo de execução inferido"; Maestro decide com base no estado |

`sob-demanda` **nunca** é recomendação automática — só aparece como opção pro usuário no AUQ #2 da Fase 4 (materialização pós-Gate 2).

---

## Regras invariantes

1. **NUNCA chamar Write/Edit/MultiEdit em `planos/*.md`.** Decomposição é em memória. Persistência é responsabilidade do Gerente (Fluxo 4b). Hook PreToolUse libera tudo de subagent — esta convenção é a defesa principal contra escrita não-orquestrada. Cross-grep do final reviewer verifica violações.
2. **Não tocar cascas.** Cascas só nascem na Fase 4 (Gerente Fluxo 5, após Gate 2 aprovado). Especialista não cria, não preenche, não referencia path de casca.
3. **Reportar `NEEDS_CONTEXT` ou `NEEDS_DATA` se faltar informação crítica** (Fase 1.5 acima). Exemplos:
   - Identidade de marca vazia e o tipo de plano depende dela (lançamento, funil).
   - Produto referenciado não existe no vault.
   - Pesquisa de audiência ausente quando o pedido pede tom específico.
4. **Devolver tudo em memória dentro do report.** Fase 1 retorna overview no chat; Fase 2 retorna bloco `DECOMPOSICAO-PLANO`. Maestro guarda último report até decisão do usuário no Gate correspondente.
5. **Especialista pode oferecer alternativas no raciocínio.** Se houver 2+ decomposições válidas (ex: lançamento semente vs meteórico), reportar a recomendada na tabela e mencionar alternativas. Maestro pode oferecer escolha via AUQ.
6. **Plano sem tarefas no bloco `DECOMPOSICAO-PLANO` é inválido.** Maestro rejeita na Fase 2.5 e re-despacha (não conta como volta de em-revisao).
7. **Pré-validação Fase 1.5 é obrigatória.** Antes do overview, especialista checa critérios críticos do tipo de plano. Faltou crítico → reporta NEEDS_CONTEXT/NEEDS_DATA, sem produzir overview.
8. **Alternativas no raciocínio são bem-vindas, não obrigatórias.** Quando aplicável, registrar na seção `## Alternativas consideradas` do bloco — Maestro pode oferecer escolha ao usuário no Gate 2.

---

## Política de modelo

Modo "Decompor plano" usa **Sonnet** (não Opus).

Razão: trabalho estruturado por frameworks (Brunson/Hormozi pra Estrategista, Schwartz pra Copywriter, Sinek/Neumeier pra Marca, Vaynerchuk/Kane pra Mídias Sociais, Marshall pra Performance). Não é criação de copy de alta variância — é decomposição metódica seguindo padrões conhecidos. Sonnet entrega qualidade adequada com 5x menos custo.

Modos "Entrega" e "Rascunho" do mesmo especialista continuam em Opus (criação de conteúdo final, alta variância).

---

## Iteração nos gates

**Gate 1 — "Ajustar" no overview:** Maestro re-despacha em `MODO: decompor-plano-fase-1` com:
- Bloco CONTEXTO idêntico (prompt cache hit ~80%).
- `INSTRUÇÃO DO USUÁRIO:` com ajuste em texto livre.
- Última versão do overview pra contexto.

Especialista re-decompõe overview. Sem cap formal aqui (cada iter é Sonnet barato + cache hit). Maestro decide quando escalar pra "Regerar?" (heurística do hub).

**Gate 2 — "Ajustar estratégico" pós-decomposição:** Maestro re-despacha em `MODO: decompor-plano-em-revisao` com:
- Bloco CONTEXTO idêntico.
- `INSTRUÇÃO DO USUÁRIO: FEEDBACK: [texto]` + plano atual + overview original.
- Especialista produz novo bloco `DECOMPOSICAO-PLANO` incorporando feedback.

Cap de 3 voltas (D7 da spec). Maestro recalcula contador via grep do Histórico antes de cada AUQ — recurso anti-burla via edit manual no Properties. Após 3, AUQ extra: "Continuar (regera) / Aprovar como está / Cancelar".

**Ajuste mecânico no Gate 2** (renomear, trocar agente, +/- tarefa, reordenar) NÃO despacha especialista — vai direto pro Gerente (Fluxo 4-ajuste-mecanico). NÃO conta como volta.

---

## Cross-domain (Estrategista decompositor universal)

Quando o pedido toca 2+ domínios estratégicos (ex: lançamento + tráfego pago + sequência de email + posts no IG), o Maestro despacha **Estrategista** (não pergunta ao usuário qual especialista). Estrategista vê o todo (Brunson + Hormozi olham o lançamento inteiro) e decompõe; cada tarefa-filha aponta `Agente:` apropriado pra execução.

Exemplo de decomposição cross-domain:

```
| # | Tarefa | Agente | Tipo de artefato | Depende de |
|---|--------|--------|------------------|------------|
| 1 | Posicionamento da oferta | Marca | identidade | — |
| 2 | Escada de valor do lançamento | Estrategista | escada-de-valor | 1 |
| 3 | Funil do webinário | Estrategista | funil | 2 |
| 4 | Copy da página de inscrição | Copywriter | entrega-generica | 3 |
| 5 | Sequência de email pré-webinário | Copywriter | campanha | 3 |
| 6 | Posts de IG do pré-lançamento | Mídias Sociais | entrega-generica | 1 |
| 7 | Anúncios de tráfego pra inscrição | Performance | analise-performance | 4 |
```

---

## Decomposição da identidade (Marca decompositora, modo cadeia)

Quando o pedido do usuário é "preencher identidade da empresa" sem especificar template único (ver `marca/SKILL.md` para detecção), Marca decompõe **sempre na ordem fixa abaixo**, com `Depende de` encadeada:

| # | Tarefa | Agente | Tipo de artefato | Depende de |
|---|--------|--------|------------------|------------|
| 1 | Círculo Dourado de [empresa] | Marca | identidade | — |
| 2 | História dos fundadores de [empresa] | Marca | identidade | 1 |
| 3 | Posicionamento de [empresa] | Marca | identidade | 2 |
| 4 | Perfil do público de [empresa] | Marca | identidade | 3 |
| 5 | Personalidade de marca de [empresa] | Marca | identidade | 4 |
| 6 | Tom de voz de [empresa] | Marca | identidade | 5 |
| 7 | Manifesto de [empresa] | Marca | identidade | 6 |

**identidade-visual** entra na cadeia só quando o usuário pedir explicitamente ("incluindo a visual" / "com identidade visual"). Quando entra, vira filha 8 com `Depende de: 7`. Sem pedido explícito, fica fora.

**Modo de execução:** sempre `sequencial` por contrato (densidade 100% de dependência cobre o critério ≥60% da regra de inferência geral).

**Flag obrigatória:** Marca declara `Cadeia de identidade: sim` no bloco DECOMPOSICAO-PLANO. Gerente Fluxo 4b lê a flag e preenche `modo-cadeia: pendente` no plano.md (gatilho pra AUQ extra do Maestro na Fase 4.5 do `fluxo-plano.md`).

**Substituição literal de `[empresa]`:** Marca substitui pelo nome do projeto/empresa do CONTEXTO. Slug do artefato deriva do título do template (`circulo-dourado`, `historia-fundadores`, etc.) — não do nome da empresa.
