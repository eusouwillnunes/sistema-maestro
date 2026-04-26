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
# Plano é caso especial: frontmatter 100% operacional + corpo preenchido pelo Gerente
# transcrevendo o RESUMO-PRO-PLAN-MODE do especialista. Especialista NÃO entra em plano.md.

titulo: "[Título do plano]"
tipo: plano
status: rascunho                      # rascunho | aprovado | em-execucao | aguardando-validacao | concluido | rejeitado | cancelado
grupo: "[slug-do-grupo]"
solicitante: "[nome]"
data-criacao: "[timestamp ISO 8601]"
data-aprovacao: ~
data-conclusao: ~
data-cancelamento: ~                  # timestamp ISO 8601 | ~ (preenchido só em status=cancelado)
motivo-cancelamento: ~                # enum (mesmo da tarefa) | ~
corrige: ~                            # ~ em plano normal; "[[planos/<slug-original>]]" em plano de correção pós-validação final
correcoes: []                         # lista de "[[planos/<slug-correcao>]]" vinculados
regera: ~                             # ~ em plano normal; "[[planos/<slug-anterior>]]" em plano regerado pré-execução (CK2 Regerar). Mutuamente exclusivo com corrige.
tags:
  - "#maestro/plano"
```

> [!info] 🤖 Casca operacional (Gerente preenche todo o conteúdo abaixo)
> Plano é caso especial. Gerente preenche todo o frontmatter e todo o corpo, transcrevendo o `RESUMO-PRO-PLAN-MODE` que o especialista decompositor produziu na Fase 2. Especialista nunca entra em plano.md.

# [Título]

## Pedido original

[Briefing do usuário capturado no brainstorm da Fase 1]

## Raciocínio da decomposição

[3-5 linhas vindas do bloco RESUMO-PRO-PLAN-MODE retornado pelo especialista — Gerente transcreve literalmente]

## Tarefas previstas (rascunho — edite aqui pra ajustar)

> Esta seção existe na Fase 4 (plano em rascunho, pré-materialização). É a fonte de verdade pré-materialização — pode ser editada manualmente no Obsidian e reconciliada via Gerente Fluxo 4f. Na Fase 6 (após Aprovar no CK2), Gerente substitui esta seção por `## Tarefas` com query Dataview e arquiva esta tabela no Histórico.

| # | Tarefa | Agente | Tipo de artefato | Depende de |
|---|--------|--------|------------------|------------|
|   |        |        |                  |            |

## Histórico de alterações

| Data | Evento | Detalhe |
|------|--------|---------|
|      |        |         |

## Feedback da validação final

[Preenchido apenas em plano de correção (`corrige` preenchido) — contém feedback consolidado do usuário que motivou a correção]
