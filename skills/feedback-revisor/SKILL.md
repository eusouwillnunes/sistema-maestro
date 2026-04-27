---
name: feedback-revisor
description: >
  Captura ativa de feedback sobre o Revisor Anti-IA. Permite registrar falsos
  negativos (texto IA que passou), falsos positivos (reprovação indevida) ou
  padrões novos não catalogados. Acionado via /feedback-revisor (Canal 2 do
  ciclo de feedback do Grupo 7).
---

> [!important] Antes de executar, verifique se o Sistema Maestro está ativo neste projeto seguindo o `core/protocolos/protocolo-ativacao.md`.

# /feedback-revisor

## 1. Papel

Capturar feedback do usuário sobre o Revisor Anti-IA de forma ativa e estruturada. Diferente do Canal 1 (frases-gatilho passivas), aqui o usuário **invoca explicitamente** quando quer registrar.

## 2. Fluxo

### Passo 1 — AUQ inicial: tipo de feedback

```
AskUserQuestion(
  question="Que tipo de feedback?",
  options=[
    "Falso negativo (Revisor aprovou texto problemático)",
    "Falso positivo (Revisor reprovou texto que tá ok)",
    "Padrão novo que o catálogo não tem ainda"
  ]
)
```

### Passo 2 — Coletar dados

Por tipo:

**Falso negativo:**
1. Pedir trecho do texto problemático (texto colado ou wikilink pro artefato).
2. Pedir padrão suspeito (lista ids do catálogo + opção "descrição livre").
3. Gravar em `{projeto}/memorias/feedback-revisor.md` na seção "Falsos negativos".

**Falso positivo:**
1. Pedir trecho do texto reprovado.
2. Pedir id do padrão que o Revisor sinalizou (do report do Revisor).
3. Pedir justificativa do usuário ("por que devia passar").
4. Gravar em `{projeto}/memorias/feedback-revisor.md` na seção "Falsos positivos".

**Padrão novo:**
1. Pedir descrição da estrutura.
2. Pedir 1-2 exemplos.
3. Gravar em `{projeto}/memorias/feedback-revisor.md` na seção "Padrões novos".

### Passo 3 — Confirmar registro

```
✓ Feedback registrado em [[feedback-revisor]] (seção: <Falsos negativos | Falsos positivos | Padrões novos>).

Quando rodar `/maestro-revisar-memorias`, esta entrada será considerada pra ajustar a calibragem do projeto. Padrão recorrente (≥3 entradas similares) vira proposta de override no `{projeto}/maestro/escrita-natural.md`.
```

## 3. Formato de cada entrada

```markdown
### YYYY-MM-DD — <Tipo> <Padrão> (<descrição curta>)

**Artefato:** [[wikilink]] (ou "texto colado abaixo")
**Trecho:**
> "<trecho do texto>"

**Padrão sinalizado:** <id ou descrição>
**Justificativa do usuário:** <quando aplicável>
**Origem da captura:** Canal 2 (slash command direto)
```

## 4. Restrições

- **Nunca grava sem confirmação do usuário** (cada AUQ é decisão consciente).
- **Nunca edita `plugin/core/`** — só escreve em `{projeto}/memorias/feedback-revisor.md`.
- **Sempre adiciona** ao arquivo (append) — nunca sobrescreve entradas existentes.
- **Sempre usa wikilink** quando o feedback se refere a artefato existente no vault.
- Se `feedback-revisor.md` não existe no projeto (raro — Bibliotecário cria no scaffold), criar com base no template `plugin/core/templates/_feedback-revisor-template.md` antes de adicionar a entrada.
