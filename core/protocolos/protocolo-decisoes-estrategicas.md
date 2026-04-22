---
description: Protocolo compartilhado do Sistema Maestro para decisões estratégicas canônicas em especialistas criativos
tags:
  - "#maestro/protocolo"
---

# Protocolo de Decisões Estratégicas

> [!info] Protocolo compartilhado do sistema MAESTRO.
> Referenciado pelos 5 especialistas criativos (Estrategista, Marca, Copywriter, Mídias Sociais, Performance) e pelo Maestro (Fluxo 5.11).

## Objetivo

Forçar especialistas criativos a apresentar opções canônicas ao usuário em pontos de decisão estratégica, em vez de decidir silenciosamente assumindo o "caminho mais comum" da persona. Mantém coerência entre entregas via memória persistente por projeto/produto.

---

## 1. Regra anti-padrão

**Nunca decidir silenciosamente em pontos canônicos.** Se há 2+ opções plausíveis pro contexto, o especialista pergunta ao usuário. "Caminho mais comum" da persona não é justificativa — é antipadrão documentado (Grupo 2, decisão D).

---

## 2. Camadas de decisão

### Camada 1 — Decisões canônicas (as 24 mapeadas na seção 9)

**SEMPRE avaliadas antes de escrever o artefato.** Não negociável.

Especialista lê contexto + `memorias/decisoes.md`, avalia cada ponto canônico aplicável à sub-skill, e:

- Se escopo `projeto`/`produto` e já registrada na memória aplicável → **reusa silenciosa**, origem `Herdado do projeto` ou `Herdado do produto`.
- Se contexto inequívoco → **infere**, origem `Inferido do contexto`.
- Se ambíguo (2+ opções plausíveis) → **pergunta** via `AskUserQuestion` (Skill) ou reporta `NEEDS_DECISION` (Agent). Após resposta, origem `Escolha do usuário`.

### Camada 2 — Decisões emergentes

Permitidas durante a escrita quando surge ambiguidade **não-canônica** (fora da lista de 24).

- **Em Skill():** `AskUserQuestion` no meio da conversa, pausa, pergunta, retoma.
- **Em Agent():** pausa, marca no artefato `[INTERROMPIDO — aguardando decisão sobre X]`, reporta `NEEDS_DECISION` com `emergente: true`.

---

## 3. Formato de apresentação de opções

Cada opção apresentada ao usuário tem:

- **label** — nome curto e claro (1-5 palavras)
- **description** — 1-2 frases explicando o que significa / quando se aplica
- **recomendado** — apenas uma opção marcada como recomendada (primeira da lista, com `(Recomendado)` no label)

A recomendação vem do especialista, baseada no contexto + framework da persona. Se contexto é genuinamente ambíguo, especialista escolhe a mais provável e justifica.

---

## 4. Critério de ambiguidade — exemplos de calibração

Exemplos concretos pra calibrar "claro vs ambíguo":

| Ponto (ID) | Contexto claro → infere | Contexto ambíguo → pergunta |
|---|---|---|
| `formato-lancamento` | "Curso R$5k B2B, sem base ao vivo, audiência LinkedIn" → PLF | "Curso R$1k B2C com base de 30k inscritos" (ao vivo? evergreen? challenge?) |
| `canal-aquisicao` | "Negócio 3 anos, listas e comunidade ativa de 10k pessoas" → Comunidade | "Negócio novo, sem audiência, orçamento limitado" |
| `arquetipo-central` | Manifesto + entrevistas repetem "transformação", "crescimento", "despertar" → Sábio | Manifesto genérico ou entrevistas contraditórias |
| `nivel-consciencia` | Pedido explícito "página pra quem já conhece o produto e hesita" → nível 4 | Pedido "página de vendas do curso X" sem info sobre audiência |
| `canal-principal` | Perfil-prospect cita "procura no Google por problema X" → Google Ads | Perfil cita múltiplas plataformas sem dominante |
| `plataforma-ancora` | Negócio visual (moda, arquitetura, comida) sem LinkedIn → IG ou TikTok | Negócio B2B de serviço genérico |
| `estrutura-pagina` | Ticket R$5k com VSL existente → Long-form + VSL embutida | Ticket low com múltiplas estratégias possíveis |

**Regra prática:** se 2+ opções passam plausíveis pelo dossiê/perfil/identidade, é ambíguo. Se só 1 passa sem forçar, é claro. Na dúvida, pergunta.

**Anti-padrão:** especialista inferir baseado em "persona default" (ex: Brunson sempre gosta de PLF) — isso viola a Camada 1.

---

## 5. Tratamento em Agent() — round-trip NEEDS_DECISION

### Passo a passo

1. Maestro despacha especialista com TAREFA + CONTEXTO + `caminho-do-artefato`.
2. Especialista lê contexto + memória, avalia decisões canônicas aplicáveis ANTES de gerar sub-tarefas ou escrever.
3. Se alguma é ambígua → reporta `STATUS: NEEDS_DECISION` com bloco `---DECISOES-PENDENTES---`.
4. Maestro filtra decisões independentes, monta `AskUserQuestion` (até 4 por chamada, lotes sequenciais se mais).
5. Usuário responde. Maestro re-despacha com bloco `---DECISOES---`.
6. Especialista re-executa: lê CONTEXTO + DECISOES, gera sub-tarefas, escreve artefato, grava memória, reporta DONE.
7. Se nova decisão dependente surge, novo round. Limite: 3 rodadas. Ultrapassou → BLOCKED.

### Formato do report NEEDS_DECISION

```
---REPORT---
STATUS: NEEDS_DECISION

---DECISOES-PENDENTES---
[decisao]
id: <id-canonico-ou-emergente>
ponto: <texto legível>
contexto: <1-2 frases justificando ambiguidade>
emergente: true|false

[opcao]
label: <nome curto>
description: <explicação>
recomendado: true|false

[opcao]
...

[fim-opcoes]
recomendacao: <label da opção recomendada>
justificativa: <por que>
---END-DECISOES-PENDENTES---

ARQUIVOS:
(nenhum — artefato continua em-andamento)
---END-REPORT---
```

Marcadores `[decisao]`/`[opcao]`/`[fim-opcoes]` são explícitos pra evitar malformação YAML.

### Bloco DECISOES no re-despacho

Formato **flat**: cada decisão vira 2 linhas (`<id>: <valor>` + `<id>-custom: <string ou null>`).

```
---DECISOES---
formato-lancamento: PLF
formato-lancamento-custom: null
---END-DECISOES---
```

Se usuário escolheu "Other":

```
---DECISOES---
formato-lancamento: other
formato-lancamento-custom: "Híbrido VSL gravado + ao-vivo semanal"
---END-DECISOES---
```

Especialista lê o par. Se `<id>` = other, usa `<id>-custom` como input. Se custom foge dos frameworks, reporta DONE_WITH_CONCERNS.

### Prompt caching entre rodadas

Maestro deve manter bloco CONTEXTO idêntico entre rodadas (mesma ordem, mesmo conteúdo, mesma formatação). Mudanças ficam restritas ao bloco DECISOES. Isso permite cache do Anthropic (TTL 5 min) e corta ~80% do custo das rodadas 2 e 3.

### Persistência para recuperação de sessão

Quando Maestro dispara `AskUserQuestion`, grava no frontmatter da tarefa:

```yaml
aguardando-decisoes: [formato-lancamento]
decisoes-pendentes-report: |
  [report completo acima como string multi-linha]
```

Após resposta do usuário, adiciona:

```yaml
decisoes-resolvidas:
  formato-lancamento: PLF
```

Três cenários cobertos:
1. **Sessão cai antes da resposta** — `/ola-maestro` detecta `aguardando-decisoes` + avisa. Re-dispara `AskUserQuestion` com report salvo.
2. **Cai entre resposta e re-despacho** — Maestro detecta `decisoes-resolvidas` sem report DONE recente → re-despacha automaticamente.
3. **Cai durante re-despacho** — artefato em-andamento + `decisoes-resolvidas` preenchido + sem report DONE recente (>15 min) → `/ola-maestro` oferece re-despachar; especialista lê conteúdo parcial e continua dali.

### Blindagem anti-gaming

1. Maestro mantém lista de IDs canônicos em memória (vem da seção 9 deste protocolo).
2. Ao receber `NEEDS_DECISION`, compara cada `id` contra a lista.
3. Se `id` bate com canônico **e** `emergente: true` → reject. Maestro re-despacha com mensagem no bloco TAREFA: "O ponto `<id>` é canônico. Deve ser avaliado na Camada 1 antes de escrever. Reporte como `emergente: false` ou resolva antes da escrita."
4. Contador: rejection conta como rodada. Mantém teto de 3.

---

## 6. Tratamento em Skill() — chamada direta

1. Especialista carrega contexto + memória.
2. Camada 1: reusa / infere / pergunta direto via `AskUserQuestion`.
3. Camada 2: `AskUserQuestion` no meio da produção quando surge ambiguidade não-canônica.
4. Escreve artefato + registra memória.

**Regra de orquestração:** especialistas **criativos** em Skill() **NÃO invocam Agent() de outros especialistas criativos**. Operacionais (Gerente, Bibliotecário, Pesquisador) podem ser invocados normalmente — esses não reportam NEEDS_DECISION.

### Enums com 5+ opções — agrupamento em 2 perguntas

`AskUserQuestion` aceita 2-4 opções. Enums maiores fazem agrupamento sequencial. Mapeamento:

| ID | N | Agrupamento |
|---|---|---|
| `arquitetura-funil` | 5 | P1: "Evento ao vivo" (Webinar) · "Asset gravado" · "Tripwire" · "Application" → P2 se "Asset gravado": "VSL" · "Challenge" |
| `canal-aquisicao` | 5 | P1: "Orgânico" · "Pago" · "Parcerias" · "Outra forma" → P2 se "Outra forma": "Comunidade" · "Outbound" |
| `formato-lancamento` | 5 | P1: "Ao vivo" · "Evergreen" · "VSL" · "Formato novo" → P2 se "Formato novo": "PLF" · "Challenge" |
| `tom-voz` | 5 | P1: "Autoritário" · "Relacional" · "Disruptivo" → P2 conforme categoria |
| `plataforma-ancora` | 5 | P1: "Short-form" (IG/TikTok) · "Long-form" (YouTube/LinkedIn) · "Microblog" (X) → P2 conforme |
| `canal-principal` | 5 | P1: "Meta" · "Google" · "Video" · "LinkedIn" → P2 se "Video": "YouTube" · "TikTok" |
| `objetivo-campanha` | 5 | P1: "Venda direta" · "Manutenção" · "Topo de funil" → P2 conforme |
| `eixo-teste` | 5 | P1: "Mensagem" · "Alvo" · "Landing page" → P2 se "Mensagem"/"Alvo" |
| `nivel-consciencia` | 5 ordinal | P1: "Início do funil" (1-2) · "Meio" (3) · "Fim" (4-5) → P2 conforme |
| `sofisticacao-mercado` | 5 ordinal | P1: "Mercado novo" (1-2) · "Maduro" (3) · "Saturado" (4-5) → P2 conforme |
| `tipo-nome` | 6 | P1: "Literal" · "Evocativo" · "Pessoal" → P2 conforme |
| `arquetipo-central` | 12 | P1: 4 categorias (Self · Order · World · Freedom) → P2: 3 arquétipos |

Agrupamento não consome rodada extra no teto de 3.

---

## 7. Memória persistente

### Arquivo

`{projeto}/memorias/decisoes.md` — criado pelo Gerente no Fluxo 1 (primeira tarefa de especialista criativo) se não existe.

### Escopo

Declarado no hub do especialista, imutável por decisão gravada:

- `projeto` — reusa silenciosa em tudo no projeto (arquétipo, tom de voz, posicionamento)
- `produto` — reusa se mesmo produto; pergunta se produto diferente (formato de lançamento, canal)
- `tarefa` — nunca reusa (nível de consciência, estrutura de página)

### Fluxo

1. **Carregamento:** especialista lê o arquivo ao iniciar (Mapa de Necessidades).
2. **Aplicação:** pra cada decisão canônica, busca registro aplicável conforme escopo.
3. **Gravação:** ao final da execução, escreve direto no arquivo.

### Override / Atualização

- Usuário pode editar o arquivo manualmente.
- Em feedback de correção ("muda o arquétipo pra Rebelde"), especialista move decisão antiga pra "Decisões sobrescritas" e registra nova como ativa.
- Decisões não expiram por data.

---

## 8. Exceção à regra 7.18 (grafo Obsidian)

`memorias/decisoes.md` fica **fora** do grafo do Obsidian. Bibliotecário não indexa na v1. Mesma regra dos outros arquivos em `memorias/` — memórias são estado persistente do sistema, não artefatos.

---

## 9. Lista das 24 decisões canônicas (tabela única)

### Estrategista

| ID | Sub-skill | Ponto | Opções | Escopo |
|---|---|---|---|---|
| `lente-diagnostico` | `diagnostico` | Lente de diagnóstico | Secret Formula · Value Equation · 80/20 Marshall · Combinadas | produto |
| `estrutura-oferta` | `oferta` | Estrutura (4 Core Offers) | Free content · Lead magnet · Low ticket · Evento/core | produto |
| `ancora-preco` | `oferta` | Âncora de preço | Premium · Mercado · Escada (tripwire→core→maximizer) | produto |
| `arquitetura-funil` | `funil` | Arquitetura de funil | Webinar · VSL · Tripwire · Challenge · Application | produto |
| `canal-aquisicao` | `aquisicao` | Canal principal | Orgânico · Pago · Parcerias · Comunidade · Outbound | produto |
| `formato-lancamento` | `webinario` | Formato de lançamento | Ao vivo · Evergreen · VSL · PLF · Challenge | produto |

### Marca

| ID | Sub-skill | Ponto | Opções | Escopo |
|---|---|---|---|---|
| `arquetipo-central` | `identidade` | Arquétipo central | 12 arquétipos em 4 categorias (Self/Order/World/Freedom) | projeto |
| `tom-voz` | `identidade` | Tom de voz dominante | Autoridade direta · Mentor empático · Provocador · Cúmplice · Técnico | projeto |
| `maturidade-marca` | `identidade` | Maturidade (5 Pillars Neumeier) | Diferenciação · Colaboração · Inovação · Validação · Cultivo | projeto |
| `estrategia-posicionamento` | `posicionamento` | Estratégia de posicionamento | Líder · Challenger · Nicho · Disruptor | projeto |
| `segmento-difusao` | `posicionamento` | Segmento de difusão (Moore/Sinek) | Innovators · Early Adopters · Early Majority · Late Majority | projeto |
| `tipo-nome` | `naming` | Tipo de nome | Descritivo · Inventado · Metafórico · Abstrato · Composto · Fundador | projeto |

### Copywriter

| ID | Sub-skill | Ponto | Opções | Escopo |
|---|---|---|---|---|
| `sofisticacao-mercado` | `headlines` | Sofisticação de mercado (Schwartz) | 1-novo · 2-emergente · 3-estabelecido · 4-saturado · 5-ultracompetitivo | tarefa |
| `nivel-consciencia` | `pagina-de-vendas` | Nível de consciência (Schwartz) | 1-Inconsciente · 2-Problema · 3-Solução · 4-Produto · 5-Pronto | tarefa |
| `estrutura-pagina` | `pagina-de-vendas` | Estrutura da página | Long-form · VSL · Short+bullets · Híbrida | tarefa |

### Mídias Sociais

| ID | Sub-skill | Ponto | Opções | Escopo |
|---|---|---|---|---|
| `pillar-content` | `estrategia` | Pillar Content Model | Pillar único semanal · Múltiplos pillars · Story-driven · Autoridade pura | projeto |
| `plataforma-ancora` | `estrategia` | Plataforma-âncora | IG · TikTok · YouTube · LinkedIn · X | projeto |
| `estagio-criador` | `estrategia` | Estágio do criador | Iniciante · Crescimento · Maturidade | projeto |
| `performance-driver` | `conteudo` | Performance driver prioritário (Kane) | Hook/Pattern-interrupt · Storytelling · Pacing · Conexão/Empatia | projeto |

### Performance

| ID | Sub-skill | Ponto | Opções | Escopo |
|---|---|---|---|---|
| `canal-principal` | `canais` | Canal principal | Meta · Google · YouTube · TikTok · LinkedIn | produto |
| `objetivo-campanha` | `canais` | Objetivo de campanha | Conversão · Leads · Remarketing · Awareness · Tráfego | produto |
| `estagio-negocio` | `testes` | Estágio do negócio | Validação (70% no principal) · Crescimento (60%) · Maturidade (50%) | produto |
| `eixo-teste` | `testes` | Eixo de teste prioritário | Criativo · Copy · Público · Oferta · LP | produto |
| `estagio-funil` | `diagnostico` | Estágio do funil | Awareness · Consideração · Conversão · Retenção | produto |

---

## 10. Registro no artefato

Todo artefato produzido por especialista criativo ganha seção `## Decisões estratégicas` com:

```markdown
## Decisões estratégicas

| Ponto | Escolha | Origem |
|---|---|---|
| Formato de lançamento | PLF | Escolha do usuário |
```

Colunas:
- **Ponto** — nome legível do ponto canônico
- **Escolha** — opção selecionada (ou texto custom se "Other")
- **Origem** — `Escolha do usuário` · `Inferido do contexto` · `Herdado do projeto` · `Herdado do produto`

Se tarefa não toca nenhum ponto canônico: **sem tabela**, só a frase "Nenhuma decisão estratégica canônica nesta tarefa." O cabeçalho `## Decisões estratégicas` continua presente pro QA conseguir validar a existência.

Exemplo para caso vazio:

```markdown
## Decisões estratégicas

Nenhuma decisão estratégica canônica nesta tarefa.
```
