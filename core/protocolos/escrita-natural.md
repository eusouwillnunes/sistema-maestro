---
description: Protocolo compartilhado do Sistema Maestro para eliminar padrões artificiais de texto
tags:
  - "#maestro/protocolo"
---

# Protocolo de Escrita Natural

> [!info] Protocolo compartilhado do sistema MAESTRO.
> Este documento é referenciado pelo Agente Revisor e por todos os agentes que produzem saída textual.

## 1. Objetivo

Garantir que **todo texto produzido pelo sistema MAESTRO** pareça escrito por humano, respeitando a identidade de marca original. Se o leitor suspeitar que foi gerado por IA, o texto perdeu credibilidade.

Padrões IA modernos (estruturas que se popularizaram em 2024+) são frequentemente **técnicas legítimas de copy** quando usadas com propósito. O que separa técnica de muleta é **densidade + uso reflexo**, não a presença pontual.

---

## 2. Regra de Ouro: Preservação de Marca

> [!warning] Preservação de Marca
> **Antes de aplicar qualquer regra deste protocolo, verifique:**
>
> - O texto está vinculado a uma marca com identidade definida? → Consulte a identidade antes de mexer
> - O tom de voz é intencional (formal, provocativo, técnico, irreverente)? → Preserve
> - O vocabulário específico da marca (termos proprietários, slogans, expressões recorrentes)? → Não toque
> - O nível de formalidade (uso de "você" vs. "tu", contrações, gírias)? → Mantenha o que a marca definiu
> - Há override do projeto em `{projeto}/maestro/escrita-natural.md`? → Aplica suspensões e ajustes de limiar antes de avaliar

**Este protocolo corrige padrões de IA. Não reescreve a personalidade da marca.**

---

## 3. Padrões Bloqueantes (presença = REPROVA)

### 3.1 Travessão como muleta

#### B-01 — Travessão como muleta
**Severidade:** Bloqueante
**Descrição:** Uso de travessão (—) pra encaixar explicações, apartes ou comentários quando ponto, vírgula, dois-pontos ou parênteses resolvem.
**Exemplo problemático:** "Essa ferramenta — que foi criada pensando em você — vai mudar o jeito — sim, o jeito — como você trabalha."
**Direção de correção:** Reescrever sem travessão. Ponto final, vírgula, dois-pontos ou parênteses quase sempre funcionam.

### 3.2 Clichês prontos

#### B-02 — "É importante ressaltar que..."
**Severidade:** Bloqueante
**Descrição:** Abertura clichê de IA pra introduzir ideia.
**Direção de correção:** Eliminar. Ir direto ao ponto.

#### B-03 — "Vale destacar que..."
**Severidade:** Bloqueante
**Descrição:** Variante do mesmo padrão clichê.
**Direção de correção:** Eliminar. Apenas dizer.

#### B-04 — "Nesse sentido, podemos observar..."
**Severidade:** Bloqueante
**Descrição:** Conector clichê com observação genérica.
**Direção de correção:** Eliminar ou reescrever com ação direta.

#### B-05 — "Além disso, é fundamental..."
**Severidade:** Bloqueante
**Descrição:** Conector + reforço clichê.
**Direção de correção:** Cortar o conectivo. Começar nova frase.

### 3.3 Metáforas gastas

#### B-06 — "Mergulhar nesse universo"
**Severidade:** Bloqueante
**Descrição:** Metáfora oceânica IA-clássica.
**Direção de correção:** "entender como funciona", "explorar o assunto".

#### B-07 — "Navegar por essa jornada"
**Severidade:** Bloqueante
**Descrição:** Metáfora de viagem genérica.
**Direção de correção:** "passar por esse processo", descrever a etapa real.

#### B-08 — "Desvendar os segredos"
**Severidade:** Bloqueante
**Descrição:** Frase pronta de promessa misteriosa.
**Direção de correção:** "entender", "aprender", "descobrir" (com objeto específico).

### 3.4 Acentuação

#### B-09 — Acentuação pt-br faltando
**Severidade:** Bloqueante
**Descrição:** Palavras como "é", "não", "próximo", "fundação", "só", "já", "também", "você", "análise", "estratégia", "conteúdo" sem acento.
**Direção de correção:** Corrigir TODAS as ocorrências antes de prosseguir.

---

## 4. Padrões de Alerta (limiar excedido = REPROVA)

### 4.1 Superlativos genéricos

#### A-01 — "Transformar sua vida" / superlativo genérico
**Severidade:** Alerta
**Limiar:** ≥1 ocorrência sem prova específica no parágrafo seguinte
**Direção de correção:** Seja específico — o que muda exatamente?

#### A-02 — "Solução inovadora" / "experiência única"
**Severidade:** Alerta
**Limiar:** ≥1 ocorrência sem descrição concreta do que faz
**Direção de correção:** Descrever o que a solução FAZ ou o que torna diferente.

### 4.2 Conectivos sequenciais

#### A-04 — Conectivos em sequência
**Severidade:** Alerta
**Limiar:** ≥2 parágrafos consecutivos abertos com conectivos ("Além disso", "Portanto", "Dessa forma", "Nesse sentido", "Por outro lado")
**Direção de correção:** Variar ou eliminar.

### 4.3 Advérbios "-mente"

#### A-03 — Advérbios "-mente"
**Severidade:** Alerta
**Limiar:** ≥3 ocorrências em texto <500 palavras (ou densidade equivalente em texto maior — ≥1 por 200 palavras)
**Lista monitorada:** "extremamente", "absolutamente", "naturalmente", "certamente", "definitivamente", "realmente"
**Direção de correção:** Reescrever com verbos fortes.

### 4.4 Listas com paralelismo

#### A-05 — Superlativos vazios
**Severidade:** Alerta
**Limiar:** ≥1 ocorrência sem prova concreta no parágrafo
**Lista monitorada:** "incrível", "extraordinário", "revolucionário"
**Direção de correção:** Adicionar prova ou cortar superlativo.

#### A-06 — Paralelismo verbal em listas
**Severidade:** Alerta
**Limiar:** ≥80% dos bullets começam com mesmo verbo no imperativo
**Direção de correção:** Variar a estrutura. Nem todo item começa com verbo.

### 4.5 Padrões IA modernos

#### A-07 — "Não é X, é Y" (estrutura antitética)
**Severidade:** Alerta
**Limiar:** ≥3 ocorrências OU densidade >1 por 200 palavras
**Exemplo problemático:** "Não é só uma ferramenta, é um sistema. Não é só processo, é resultado. Não é só método, é caminho."
**Exceção por peça:** suspenso em headline; limiar ×3 em post/story.

#### A-08 — Pergunta retórica encadeada
**Severidade:** Alerta
**Limiar:** ≥3 perguntas em sequência sem texto entre
**Exemplo problemático:** "Já parou pra pensar? Já sentiu isso? Já viu acontecer com você?"
**Exceção por peça:** limiar ×2 em reels.

#### A-09 — Staccato-longo alternado
**Severidade:** Alerta
**Limiar:** ≥3 alternâncias frase-curta/frase-longa seguidas
**Direção de correção:** Variar ritmo de frases sem padrão fixo.
**Exceção por peça:** suspenso em headline, story, reels; limiar ×2 em vsl.

#### A-10 — Adjetivos em cadeia
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências de cadeia com 3+ adjetivos
**Exemplo problemático:** "rápido, simples, eficiente, direto"
**Direção de correção:** Escolher 1-2 adjetivos com peso real.

#### A-11 — "A verdade é que..." (abertura)
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências
**Direção de correção:** Cortar e ir direto à afirmação.

#### A-12 — "Aqui vai..." (abertura)
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências
**Direção de correção:** Cortar e apresentar o conteúdo direto.

#### A-13 — Inversão sintática abusiva
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências
**Exemplo problemático:** "Errar, todos erramos." / "Mudar, é preciso."
**Direção de correção:** Voltar pra ordem natural da frase.

#### A-14 — "E sabe por quê?" (ponte)
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências
**Direção de correção:** Conectar ideias sem ponte retórica.

#### A-15 — "Spoiler:" / "Plot twist:" (abertura)
**Severidade:** Alerta
**Limiar:** ≥1 ocorrência
**Nota:** Exceção à premissa "densidade > presença" — é clichê IA puro sem versão "técnica de copy" defensável. Loop de feedback pode afrouxar se aparecer falso positivo.

#### A-16 — "Pense comigo:" / "Imagina só:" / "Olha só:"
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências
**Direção de correção:** Apresentar a ideia sem chamada artificial.

#### A-17 — Auto-pergunta + auto-resposta no mesmo parágrafo
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências
**Exemplo problemático:** "Por que isso importa? Porque [resposta]."
**Direção de correção:** Afirmar direto sem auto-pergunta.

#### A-18 — "Vou te contar um segredo:" / "Aqui está o pulo do gato:"
**Severidade:** Alerta
**Limiar:** ≥1 ocorrência
**Nota:** Clichê IA puro (ver Nota do A-15).

#### A-19 — "Eis o ponto:" / "Eis a questão:"
**Severidade:** Alerta
**Limiar:** ≥1 ocorrência
**Nota:** Clichê IA puro (ver Nota do A-15).

#### A-20 — Negação dupla dramática
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências
**Exemplo problemático:** "Não é apenas X. É muito mais."
**Direção de correção:** Afirmar X com peso próprio.

#### A-21 — "Se você é X, isso é pra você"
**Severidade:** Alerta
**Limiar:** ≥1 ocorrência fora da primeira frase do artefato
**Direção de correção:** Segmentação artificial — descrever quem ganha o quê sem chamada genérica.

#### A-22 — Lista numerada de substantivos curtos
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências
**Exemplo problemático:** "1. Foco. 2. Disciplina. 3. Resultado."
**Direção de correção:** Frases descritivas com sentido próprio.

#### A-23 — Emoji decorativo sem função
**Severidade:** Alerta
**Limiar:** ≥3 ocorrências (✨🚀💡 entre frases sem função informacional)
**Direção de correção:** Cortar emojis decorativos. Manter só os que comunicam.

#### A-24 — Bullet único como desfecho dramático em **negrito**
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências
**Direção de correção:** Continuar o parágrafo sem bullet teatral.

#### A-25 — Frase de 2-3 palavras isolada como parágrafo
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências
**Exemplo problemático:** "É isso." / "Simples assim." / "Sem rodeios."
**Exceção por peça:** suspenso em headline e story; limiar ×2 em vsl.

#### A-26 — "P.S." artificial em texto não-email
**Severidade:** Alerta
**Limiar:** ≥1 ocorrência
**Nota:** Clichê IA puro (ver Nota do A-15).

#### A-27 — Triplete de imperativo
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências
**Exemplo problemático:** "Pare. Respire. Decida."
**Exceção por peça:** suspenso em headline e reels.

#### A-28 — Paralelismo de bullets começando com mesmo verbo (≥3 bullets)
**Severidade:** Alerta
**Limiar:** ≥1 ocorrência
**Exceção por peça:** suspenso em headline.

> Nota 1: A-06 (clássico) e A-28 (moderno) tratam paralelismo. A-06 mede proporção (≥80% dos bullets); A-28 mede absoluto (≥3 bullets seguidos com mesmo verbo). Mantidos separados porque disparam em contextos distintos.
>
> Nota 2: A-15, A-18, A-19, A-26 disparam com **≥1 ocorrência**. Exceção consciente à premissa "densidade > presença" — esses padrões são clichê IA puro sem versão "técnica de copy" defensável. Loop de feedback pode afrouxar se aparecer falso positivo.

---

## 5. Calibragem por Tipo de Peça

Peças curtas TÊM staccato, paralelismo, pergunta retórica e triplete como ferramentas centrais. Calibragem por formato:

| Peça | Padrões suspensos | Padrões com limiar afrouxado |
|---|---|---|
| `headline` (≤12 palavras) | A-06, A-09, A-25, A-27, A-28 | — |
| `post` | — | Padrões IA modernos com limiar ×3 |
| `story` | A-09, A-25 | Padrões IA modernos com limiar ×3 |
| `reels` | A-09, A-27 | A-08 com limiar ×2 |
| `vsl` | — | A-09, A-25 com limiar ×2 |
| `email` | — | Padrões IA modernos com limiar ×2 |
| `sequencia-email` | — | Padrões IA modernos com limiar ×2 |
| `copy-longa` | — | Limiares padrão (texto longo, regras valem cheias) |
| `pagina-de-vendas` | — | Limiares padrão |
| `carrossel` | — | Padrões IA modernos com limiar ×2 |

### Como o Revisor extrai a peça

1. Lê o frontmatter do artefato a revisar (caminho passado no bloco TAREFA do despacho).
2. Extrai valor `peca/*` do array `tags-dominio` (ex: `peca/headline`, `peca/email`).
3. Se há tag `peca/X`, aplica calibragem da tabela acima para `X`. Se não há, aplica limiares padrão do core.
4. Se há mais de uma tag `peca/*` (raro), aplica a mais restritiva (a que **menos** afrouxa) — proteção contra ambiguidade.

---

## 6. Teste de Naturalidade (Teste do WhatsApp)

> [!tip] Teste do WhatsApp
> **"Eu mandaria esse texto assim num áudio de WhatsApp pra um colega?"**
>
> Se a resposta for "não", reescreva até poder responder "sim" — mas mantendo o tom da marca.

### Como aplicar

1. Leia o texto em voz alta (ou mentalmente, como se fosse falar)
2. Se alguma frase travar na boca, é sinal de escrita artificial
3. Se você não diria aquilo numa conversa real com um colega, reescreva
4. O teste não exige informalidade — exige naturalidade. Um texto formal pode ser natural

---

## 7. Checklist Rápido

### 7.1 Bloqueantes (qualquer um presente → REPROVADO)

- [ ] Algum travessão (—) no corpo? (B-01)
- [ ] Algum clichê pronto (B-02 a B-05)?
- [ ] Alguma metáfora gasta (B-06 a B-08)?
- [ ] Acentuação pt-br completa? (B-09)

### 7.2 Alertas (limiar excedido → REPROVADO)

- [ ] Densidade de "-mente" (A-03)?
- [ ] Conectivos sequenciais (A-04)?
- [ ] Superlativos sem prova (A-01, A-02, A-05)?
- [ ] Paralelismo de listas (A-06, A-28)?
- [ ] Padrões IA modernos (A-07 a A-27) — verificar limiar de cada um, com calibragem da Seção 5 quando aplicável

### 7.3 Marca

- [ ] Tom de voz coerente com identidade?
- [ ] Vocabulário proprietário preservado?
- [ ] Nível de formalidade respeitado?
- [ ] Override do projeto carregado e aplicado?

---

## 8. Sintaxe de Override (referência rápida)

Override mora em 2 níveis acima do core:
- `~/.maestro/escrita-natural.md` (user — opcional, override pessoal)
- `{projeto}/maestro/escrita-natural.md` (projeto — opcional, override por marca/cliente)

### Adicionar padrão novo

Bullet novo na seção apropriada (Bloqueante ou Alerta) com mesmo formato do core. Recebe id local com prefixo `U-` (user) ou `P-` (projeto).

```markdown
#### P-01 — Linguagem corporativa demais
**Severidade:** Alerta
**Limiar:** ≥2 ocorrências de "sinergia", "alavancar", "deliverables"
**Direção de correção:** Trocar por palavra concreta.
```

### Desativar item core

```markdown
- DESATIVAR: A-08
  # Origem: feedback 2026-04-15 (3 falsos positivos consolidados — pergunta retórica é assinatura)
```

### Ajustar limiar de item core

```markdown
- LIMIAR: A-07 → ≥5 ocorrências OU densidade >1 por 100 palavras
  # Origem: feedback 2026-04-20 (limiar original muito apertado pra esta marca)
```

---

## 9. Acentuação obrigatória em português do Brasil

Todo texto produzido DEVE usar acentuação correta em português do Brasil. Esta regra é inegociável (vide B-09).
