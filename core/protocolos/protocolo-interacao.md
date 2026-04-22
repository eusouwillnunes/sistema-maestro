---
description: Protocolo compartilhado do Sistema Maestro para interação propositiva com o usuário
tags:
  - "#maestro/protocolo"
---

# Protocolo de Interação Propositiva

> [!info] Protocolo compartilhado do sistema MAESTRO.
> Este documento é referenciado por toda skill que faz perguntas de decisão ao usuário.

## Objetivo

O Maestro é propositivo, não reativo. Sempre que houver opções finitas, o sistema oferece escolhas claras em vez de esperar o usuário adivinhar o que digitar. O usuário decide com um clique, mas sempre pode digitar algo diferente (opção "Other" nativa).

---

## Regra Principal

Sempre que uma pergunta tiver **2 a 4 respostas possíveis**, use a ferramenta `AskUserQuestion` com:

- **label**: Nome curto e claro (1-5 palavras)
- **description**: Uma frase explicando o que acontece se escolher essa opção
- **multiSelect**: `true` quando as opções não são mutuamente exclusivas

O sistema oferece opções. O usuário escolhe. Simples.

---

## Quando NÃO usar

- **Perguntas abertas** — entrevistas, diagnósticos, coleta de contexto sobre o negócio do usuário
- **Confirmações simples** — "Podemos continuar?" (basta aguardar resposta em texto)
- **Respostas que dependem 100% do contexto do usuário** — nome, URL, descrição de produto
- **Entrevistador** — toda a skill de entrevista é conversa aberta por natureza

---

## Decisões estratégicas emergentes em modo Skill()

Especialistas criativos em Skill() podem chamar `AskUserQuestion` **durante a escrita** quando surge ambiguidade não-canônica. Pausa produção, pergunta, retoma. Exemplo: ao estruturar webinário PLF, descobre que o mecanismo do produto tem duas abordagens válidas pro Segredo #2.

**Em modo Agent(), não use AskUserQuestion** — reporte `NEEDS_DECISION` com flag `emergente: true` e aguarde re-despacho do Maestro com a resposta.

Decisões **canônicas** (as 24 listadas no protocolo-decisoes-estrategicas.md, seção 9) DEVEM ser avaliadas antes de começar a escrever (Camada 1). Classificar uma canônica como emergente é antipadrão documentado — o Maestro rejeita.

---

## Teto de perguntas por chamada

O teto de 4 opções do `AskUserQuestion` é **por chamada**, não por tarefa. Especialista pode fazer múltiplas chamadas sequenciais ao longo da execução (ex: 3 chamadas seguidas, cada uma com 3-4 opções).

Quando uma decisão canônica tem 5+ opções (ver `protocolo-decisoes-estrategicas.md`, seção 6), o agrupamento em 2 perguntas sequenciais é feito automaticamente pelo especialista — P1 escolhe categoria, P2 refina.

---

## Agrupamento (mais de 4 opções)

Quando as opções passam de 4:

1. **Primeira pergunta:** categorias (2-4 grupos)
2. **Segunda pergunta:** opções dentro da categoria escolhida (2-4 opções)

Exemplo: 10 agentes → "Qual área?" (Conteúdo / Estratégia / Dados / Sistema) → "Qual agente?"

Duas perguntas claras são melhores que uma lista enorme em texto.

---

## multiSelect

Ativar quando as opções **não são mutuamente exclusivas**:

- "Quais áreas quer reconfigurar?" → pode marcar várias
- "Quais plataformas?" → pode escolher múltiplas
- "Quais formatos de conteúdo?" → pode selecionar vários

---

## Opção Recomendada

Quando houver uma opção claramente melhor pro contexto:

- Colocá-la como **primeira** da lista
- Adicionar `(Recomendado)` no final do label

O sistema sugere, o usuário decide.

---

## Checklist Rápido

Antes de fazer uma pergunta ao usuário:

- [ ] A pergunta tem opções finitas (2-4)? → Use `AskUserQuestion`
- [ ] Tem mais de 4 opções? → Agrupe em categorias primeiro
- [ ] As opções são complementares (não exclusivas)? → Use `multiSelect: true`
- [ ] Existe uma opção claramente melhor? → Marque como "(Recomendado)"
- [ ] A pergunta é aberta (contexto, nome, URL)? → Use texto livre normal
- [ ] É uma confirmação simples? → Use texto normal
