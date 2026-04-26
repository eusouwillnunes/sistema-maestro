---
description: Protocolo do modo "Decompor plano" para os 6 especialistas que decompõem planos compostos no Grupo B
tags:
  - "#maestro/protocolo"
---

# Protocolo de Decomposição de Plano

> [!info] Protocolo compartilhado do Sistema MAESTRO.
> Este documento é referenciado via `Aplica:` por todos os especialistas que podem ser despachados como decompositores de plano (Fase 2 do Fluxo de Plano v2).

## Objetivo

Definir como o especialista-dono de um tipo de plano decompõe um pedido em tarefas atômicas e devolve o resultado em memória pro Maestro alimentar o Checkpoint 1.

---

## Quando este modo é acionado

O Maestro despacha o especialista em modo "Decompor plano" quando:
- Classifica o pedido como **plano** (composto — 2+ tarefas ou dependências) na Fase 1.
- Identifica o tipo de plano via mapa de roteamento do `fluxo-plano.md`.
- Despacha o especialista-dono via `Agent()` com bloco CONTEXTO específico (ver `protocolo-contexto.md`, rota "Decompor plano") + instrução `MODO: decompor-plano`.

---

## Formato do retorno: bloco RESUMO-PRO-PLAN-MODE

O especialista devolve dentro do report do Agent() um bloco delimitado:

```
---RESUMO-PRO-PLAN-MODE---
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
---END-RESUMO-PRO-PLAN-MODE---
```

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

`sob-demanda` **nunca** é recomendação automática — só aparece como opção pro usuário no AUQ #2 do CK2.

---

## Regras invariantes

1. **Não escrever arquivo nenhum.** Decomposição é em memória. Persistência é responsabilidade do Gerente em Fluxo 4b (despachado depois pelo Maestro se usuário aprovar no CK1).
2. **Não tocar cascas.** Cascas só nascem na Fase 6 (Gerente Fluxo 5). Especialista não cria, não preenche, não referencia path de casca.
3. **Reportar `NEEDS_CONTEXT` se faltar informação crítica.** Exemplos:
   - Identidade de marca vazia e o tipo de plano depende dela (lançamento, funil).
   - Produto referenciado não existe no vault.
   - Pesquisa de audiência ausente quando o pedido pede tom específico.
4. **Devolver tudo em memória dentro do report.** Maestro guarda o último report até a escolha do usuário no CK1.
5. **Especialista pode oferecer alternativas.** Se houver 2+ decomposições válidas (ex: lançamento semente vs meteórico), reportar a recomendada na tabela e mencionar as alternativas no raciocínio. Maestro pode oferecer escolha via AUQ no CK1 se o usuário ajustar.

---

## Política de modelo

Modo "Decompor plano" usa **Sonnet** (não Opus).

Razão: trabalho estruturado por frameworks (Brunson/Hormozi pra Estrategista, Schwartz pra Copywriter, Sinek/Neumeier pra Marca, Vaynerchuk/Kane pra Mídias Sociais, Marshall pra Performance). Não é criação de copy de alta variância — é decomposição metódica seguindo padrões conhecidos. Sonnet entrega qualidade adequada com 5x menos custo.

Modos "Entrega" e "Rascunho" do mesmo especialista continuam em Opus (criação de conteúdo final, alta variância).

---

## Iteração no Checkpoint 1

Se o usuário escolher "Ajustar" no CK1, Maestro despacha o mesmo especialista de novo com:
- Bloco CONTEXTO idêntico (prompt cache hit espera ~80% redução de custo).
- Bloco `INSTRUÇÃO DO USUÁRIO:` com o ajuste pedido em texto livre.
- Última versão do `RESUMO-PRO-PLAN-MODE` pra contexto.

Especialista re-decompõe e devolve nova versão. Loop tem cap de 5 iterações (decisão do hub do Maestro, não do protocolo) — após 5, Maestro força AUQ "Regerar / Cancelar / Continuar mesmo assim".

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
