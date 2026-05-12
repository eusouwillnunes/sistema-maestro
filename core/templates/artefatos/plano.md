---
tipo: plano
pasta-destino: planos/
naming: cronologico
descricao: Plano agregador de tarefas relacionadas. Cobre plano normal (corrige/regera vazios), plano de correção (corrige preenchido), plano regerado pré-execução (regera preenchido).
---

> Aplica: [[protocolo-biblioteca]] (seção "Wikilinks em frontmatter")

## Frontmatter do artefato

```yaml
# === 🤖 Operacional (Gerente preenche) ===
# Plano é caso especial: especialista decompositor decide o conteúdo (objetivo, contexto,
# peças, raciocínio, tarefas) e o Gerente transcreve mecanicamente no vault.
# Especialista NUNCA chama Write/Edit em plano.md — sempre via bloco DECOMPOSICAO-PLANO
# pro Gerente. Esta convenção é a defesa principal contra escrita não-orquestrada
# (hook PreToolUse libera tudo de subagent — confiamos no contrato textual).

titulo: "[Título do plano]"
tipo: plano
status: rascunho                      # rascunho | em-revisao | aprovado | em-execucao | aguardando-validacao | concluido | rejeitado | cancelado
grupo: "[slug-do-grupo]"
solicitante: "[nome]"
data-criacao: "[timestamp ISO 8601]"
data-aprovacao: ~
data-conclusao: ~
data-cancelamento: ~                  # timestamp ISO 8601 | ~ (preenchido só em status=cancelado)
motivo-cancelamento: ~                # enum (mesmo da tarefa) | ~
corrige: ~                            # ~ em plano normal; "[[planos/<slug-original>]]" em plano de correção pós-validação final
correcoes: []                         # lista de "[[planos/<slug-correcao>]]" vinculados
regera: ~                             # ~ em plano normal; "[[planos/<slug-anterior>]]" em plano regerado pré-execução (Gate 2 Regerar). Mutuamente exclusivo com corrige.
agente-decompositor: ~                # nome do especialista que decompôs (estrategista | copywriter | marca | midias-sociais | performance | pesquisador)
modo-execucao: ~                      # paralelo | sequencial | paralelo-com-batches | sob-demanda — definido pelo especialista no bloco DECOMPOSICAO-PLANO
data-inicio: ~                        # timestamp ISO 8601 quando 1ª tarefa-filha vira em-andamento
voltas-em-revisao: 0                  # contador 0..3 do cap de voltas no Gate 2. Maestro recalcula via grep do Histórico antes de usar (anti-burla manual).
modo-cadeia: ~                        # ~ = não é cadeia | pendente = aguardando AUQ guiado/automático | guiado | automatico. Preenchido pelo Gerente quando bloco DECOMPOSICAO-PLANO declara "Cadeia de identidade: sim".
status-cadeia: ~                      # ~ = ativa | pausado — preenchido pelo Gerente quando usuário escolhe "Pausar cadeia" no AUQ entre filhas. Só relevante quando modo-cadeia preenchido.
contexto-utilizado:                   # lista YAML de wikilinks consumidos pelo decompositor (espelha seção do corpo). Habilita Graph View do Obsidian.
  - ""
tags:
  - "#maestro/plano"
```

> [!info] 🤖 Casca operacional (Gerente preenche todo o conteúdo abaixo)
> Plano é caso especial. Gerente preenche todo o frontmatter e todo o corpo, transcrevendo o bloco `DECOMPOSICAO-PLANO` que o especialista decompositor produziu na Fase 2 do Fluxo de Plano (2 gates). Especialista nunca chama Write/Edit em plano.md.

# [Título]

## Objetivo

[1-3 frases registrando o que o usuário quer atingir, transcritas do overview aprovado no Gate 1]

## Contexto utilizado

> Lista mantida sincronizada com frontmatter `contexto-utilizado`. Frontmatter é a fonte de verdade pra Graph View / Dataview; corpo é pra leitura humana.

- [[area/wikilink-1]]
- [[area/wikilink-2]]

## Peças do plano

1. [slug-da-peca-1] (Agente: [Especialista])
2. [slug-da-peca-2] (Agente: [Especialista])

## Pedido original

[Briefing literal do usuário]

## Raciocínio da decomposição

[3-5 linhas vindas do bloco DECOMPOSICAO-PLANO retornado pelo especialista — Gerente transcreve literalmente]

## Tarefas previstas (rascunho — edite aqui pra ajustar)

> Esta seção existe enquanto o plano está em rascunho ou em-revisao (pré-materialização). É a fonte de verdade pré-materialização — pode ser editada manualmente no Obsidian e reconciliada via Gerente Fluxo 4f. Após Aprovar no Gate 2, o Gerente (Fluxo 5) substitui esta seção por `## Tarefas` com query Dataview e arquiva esta tabela no Histórico.

| # | Tarefa | Agente | Tipo de artefato | Depende de |
|---|--------|--------|------------------|------------|
|   |        |        |                  |            |

## Histórico de alterações

| Data | Evento | Solicitante | Detalhe |
|------|--------|-------------|---------|
|      |        |             |         |

## Feedback da validação final

[Preenchido apenas em plano de correção (`corrige` preenchido) — contém feedback consolidado do usuário que motivou a correção]

---

<!--
=== 🎨 Configuração recomendada de Properties no Obsidian ===
Settings > Custom Properties > status > Type: Select
Mapping de cores sugerido:
  🔲 rascunho               — gray
  🟠 em-revisao             — orange
  ✅ aprovado               — green
  🔵 em-execucao            — blue
  ⏳ aguardando-validacao    — yellow
  🏁 concluido              — dark-green
  ❌ rejeitado              — red
  ⭕ cancelado              — dark-gray

=== 💡 Pesquisa rápida no Obsidian ===
Use Quick Switcher (Cmd+K / Ctrl+K) ou Search com operadores:
  status:em-revisao         — planos esperando seu feedback
  status:rascunho           — planos aguardando primeira leitura
  voltas-em-revisao:3       — planos no limite do cap
  parte-de:[[planos/X]]     — todas tarefas do plano X
-->

