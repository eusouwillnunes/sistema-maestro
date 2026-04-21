---
description: Protocolo compartilhado para agentes executados via Agent() — status de retorno, formato de report, empacotamento de contexto e seleção de modelo
tags:
  - "#maestro/protocolo"
---

# Protocolo de Comunicação Agent()

> [!info] Protocolo compartilhado do sistema MAESTRO.
> Referenciado pelo Maestro e por todos os agentes que podem ser executados via Agent tool.

## Objetivo

Definir o contrato de comunicação entre o Maestro (orquestrador) e agentes executados via Agent() (subagentes isolados). Todo agente que roda como Agent() DEVE seguir este protocolo.

---

## 1. Status de Retorno

Todo agente rodando como Agent() DEVE reportar um destes status ao final da execução:

| Status | Significado | Ação do Maestro |
|--------|-------------|-----------------|
| `DONE` | Tarefa concluída com sucesso | Segue pro Ciclo de Validação (QA → Revisor) |
| `DONE_WITH_CONCERNS` | Concluído mas com ressalvas | Lê as ressalvas, decide se valida ou ajusta antes do Ciclo |
| `PARTIAL` | Operação executada com sucesso em parte das escritas planejadas, falhou antes de concluir o resto | Arquivos escritos seguem contrato normal; pendentes não foram tocados. Maestro instrui usuário a repetir o pedido pra finalizar. Em modo recuperação, agente completa só o que falta |
| `NEEDS_DATA` | Faltam dados que não existem em lugar nenhum | Cria entrevista(s) e/ou pesquisa(s), bloqueia a tarefa |
| `NEEDS_CONTEXT` | Precisa de informação que existe mas não foi passada | Re-despacha com mais contexto (sem criar entrevista) |
| `INSUFFICIENT_DATA` | Dado foi passado mas é insuficiente pra produzir com qualidade | Cria entrevista de aprofundamento e/ou pesquisa complementar |
| `BLOCKED` | Não consegue executar por outro motivo | Avalia: re-despacha com modelo mais capaz, quebra a tarefa, ou escala pro usuário |

### Diferenças-chave

- **NEEDS_DATA** → o dado **não existe em lugar nenhum** — precisa ser coletado do usuário ou pesquisado
- **NEEDS_CONTEXT** → o dado **provavelmente existe** (num template, memória ou arquivo) mas o agente não recebeu
- **INSUFFICIENT_DATA** → o dado **foi passado** mas não tem profundidade ou qualidade suficiente
- **PARTIAL** → a execução **começou**, mas não terminou. Parte das escritas foi feita; o resto não. Diferente de `NEEDS_CONTEXT`: `PARTIAL` reporta estado parcial após executar; `NEEDS_CONTEXT` reporta antes de executar, pedindo input

---

## 2. Formato de Report

Todo agente DEVE encerrar sua execução com um bloco de report neste formato:

```
---REPORT---
STATUS: [um dos 7 status da tabela acima]

RESULTADO:
[Conteúdo completo produzido, se houver. Se DONE ou DONE_WITH_CONCERNS, o resultado vai aqui.]

DADOS_FALTANTES:
[Apenas se STATUS = NEEDS_DATA. Lista do que precisa ser coletado.]
  - dado: "[descrição do dado faltante]"
    tipo: entrevista | pesquisa
    template-destino: [nome do template que será preenchido]
    perguntas-sugeridas:
      - "[pergunta 1]"
      - "[pergunta 2]"

DADOS_INSUFICIENTES:
[Apenas se STATUS = INSUFFICIENT_DATA. Lista do que está insuficiente.]
  - dado: "[nome do dado ou seção insuficiente]"
    problema: "[o que está faltando ou por que é insuficiente]"
    tipo: entrevista | pesquisa
    perguntas-sugeridas:
      - "[pergunta focada no gap]"

CONTEXTO_FALTANTE:
[Apenas se STATUS = NEEDS_CONTEXT. Lista do que provavelmente existe mas não foi passado.]
  - "[descrição do contexto necessário e onde provavelmente está]"

CONCERNS:
[Apenas se STATUS = DONE_WITH_CONCERNS. Ressalvas sobre o trabalho produzido.]
  - "[ressalva 1]"
  - "[ressalva 2]"

BLOCKER:
[Apenas se STATUS = BLOCKED. Descrição do bloqueio.]
  - motivo: "[o que impede a execução]"
  - tentativas: "[o que o agente tentou antes de reportar bloqueio]"
  - sugestao: "[o que o agente acha que resolveria]"

ARQUIVOS:
[Lista de arquivos gerados ou modificados]
  - criado: "[caminho do arquivo]"
  - modificado: "[caminho do arquivo]"
---END-REPORT---
```

### Regras do report

- Seções não aplicáveis ao status ficam vazias ou são omitidas
- O bloco `---REPORT---` / `---END-REPORT---` DEVE estar presente — é como o Maestro identifica o report
- RESULTADO deve conter o conteúdo completo, não resumido
- ARQUIVOS lista tudo que foi criado ou modificado pelo agente

---

## 3. Empacotamento de Contexto (Maestro → Agente)

Quando o Maestro despacha via Agent(), monta o prompt com estas seções, nesta ordem:

### Bloco 1 — Instruções do agente

Conteúdo completo da skill relevante (hub + sub-skill quando aplicável). Copiado literalmente do arquivo SKILL.md.

### Bloco 2 — Tarefa

```
---TAREFA---
FLUXO: [Apenas para o Gerente de Projetos — identifica qual dos 13 fluxos executar:
        criar-tarefa | concluir-tarefa | criar-revisao |
        criar-plano | materializar-plano | criar-tarefa-validacao |
        concluir-plano | criar-plano-correcao | adicionar-pos-aprovacao |
        criar-entrevista | consultar | cancelar-tarefa | cancelar-plano]
Objetivo: [o que executar]
Template: [qual template preencher, se aplicável]
Caminho do artefato: [caminho/absoluto/do/arquivo-a-editar.md]
  # Opcional. Quando presente, o agente DEVE editar esse arquivo em vez
  # de retornar texto no RESULTADO. O arquivo já tem frontmatter e
  # seções-base criadas pelo Gerente. O RESULTADO do report passa a
  # trazer apenas um resumo curto (1-3 frases) + o caminho.
Formato de entrega: [Markdown Obsidian-first com frontmatter YAML e wiki-links]
Protocolo de report: Seguir o formato definido em protocolo-agent.md (seção 2)
---END-TAREFA---
```

### Campos adicionais no REPORT do Gerente (fluxos criar-plano e criar-plano-correcao)

Nos fluxos `criar-plano` (Fluxo 4) e `criar-plano-correcao` (Fluxo 8), o REPORT do Gerente inclui dois campos adicionais:

```
PLANO-CRIADO: [caminho absoluto do arquivo do plano criado]
RESUMO-PRO-PLAN-MODE: |
  [conteúdo compacto pré-formatado pronto pro Maestro passar ao ExitPlanMode.
   Inclui: 3-5 linhas de raciocínio + tabela resumida das tarefas + wiki-link pro arquivo completo.]
```

O Maestro lê `RESUMO-PRO-PLAN-MODE` e passa diretamente pro `ExitPlanMode` nativo — sem reprocessar.

### Bloco 3 — Contexto coletado

```
---CONTEXTO---
Contexto de marca (LEIA estes arquivos antes de executar):
- [caminhos dos templates de identidade preenchidos — conforme protocolo-contexto.md]

Contexto complementar (leia se relevante pra tarefa):
- [caminhos dos templates do Mapa de Necessidades do agente]

Entrevistas concluídas:
- [caminhos das entrevistas relevantes]

PARTE-DE-PLANO: [[plano-xyz]]  # opcional — preenchido quando a tarefa faz parte de plano; ausente quando atômica

Pesquisas disponíveis:
- [caminhos das pesquisas relevantes]

Material de referência:
- [caminhos de documentos pertinentes]
---END-CONTEXTO---
```

### Bloco 4 — Memórias do agente

```
---MEMORIAS---
[Preferências do usuário para este agente]
[Feedbacks anteriores registrados]
---END-MEMORIAS---
```

### Bloco 5 — Regras

```
---REGRAS---
- Use acentuação correta em português do Brasil em toda a sua resposta
- Siga convenções Obsidian: frontmatter YAML, wiki-links [[...]], callouts (> [!tip]), tags #maestro/
- NUNCA invente dados. Se falta informação, reporte NEEDS_DATA ou INSUFFICIENT_DATA
- Use templates anteriormente preenchidos como base (preenchimento sequencial)
- Antes de executar, LEIA os arquivos listados no bloco CONTEXTO. Especialmente identidade de marca (tom de voz, personalidade, posicionamento). Esses arquivos contêm o contexto necessário pra produzir com qualidade e coerência.
- Ao concluir, reporte usando o formato ---REPORT--- definido no protocolo
---END-REGRAS---
```

### Quando `caminho-do-artefato` está presente no bloco TAREFA

Comportamento do agente:

1. **Ler o arquivo** apontado por `caminho-do-artefato`. Ele já contém frontmatter e seções-base vazias (a "casca").
2. **Ler a tarefa vinculada** (frontmatter `resultado:` da tarefa aponta pro mesmo arquivo). A seção "Descrição" da tarefa é o briefing real.
3. **Preencher as seções do artefato** via Edit/Write, mantendo o frontmatter.
4. **Ao concluir**, atualizar `status: concluido` no frontmatter do artefato.
5. **No report**, trazer apenas RESUMO (1-3 frases) + ARTEFATO (caminho). O conteúdo vive no arquivo.

Exemplo de RESULTADO quando edita artefato:

```
RESULTADO:
Funil de webinar para Curso X criado em 5 etapas (lead magnet → registro → confirmação → webinar → pitch).
Artefato: {projeto}/funis/funil-webinario-curso-x.md
```

**Exceção — Pesquisador:** não recebe `caminho-do-artefato`. Cria o próprio arquivo em `pesquisas/` e reporta o caminho. O Gerente atualiza `resultado:` da tarefa no Fluxo 3 (conclusão).

---

## 4. Seleção de Modelo

### Regra de modelo mínimo

**Sonnet é o modelo mínimo para qualquer conteúdo que o usuário vai ler** — templates preenchidos, documentos de pesquisa, entregas de especialistas, textos revisados. Haiku é permitido APENAS para operações mecânicas que não geram conteúdo textual (CRUD, validação de checklist, criação de estrutura de pastas).

### Defaults do sistema

| Agente | Modelo default | Justificativa |
|--------|---------------|---------------|
| QA | haiku | Verificação mecânica de checklist |
| Gerente de Projetos | haiku/sonnet | CRUD (haiku), decomposição e conclusão (sonnet) |
| Bibliotecário | haiku | Criação de estrutura de pastas |
| Pesquisador | sonnet | Síntese de dados, sem criação |
| Revisor | sonnet | Julgamento de qualidade textual |
| Copywriter | sonnet | Criação com frameworks estruturados |
| Estrategista | sonnet | Criação com frameworks estruturados |
| Marca | sonnet | Criação com frameworks estruturados |
| Mídias Sociais | sonnet | Criação com frameworks estruturados |
| Performance | sonnet | Criação com frameworks estruturados |
| Entrevistador | sonnet | Condução de sessões de coleta |

### Overrides do usuário

O Maestro lê `~/.maestro/config.md` antes de cada despacho Agent(). Se o campo do agente tem valor diferente de `~`, usa o override. Se é `~` ou não existe, usa o default acima.

### Lógica de resolução

```
1. Ler ~/.maestro/config.md → seção modelos → campo do agente
2. Se campo existe e valor ≠ ~ → usar o override
3. Se campo não existe ou valor = ~ → usar default da tabela acima
4. Passar o modelo resolvido no parâmetro model: do Agent()
```

---

## 5. Compatibilidade Agent() para Agentes

Todo agente que pode rodar como Agent() DEVE ter uma seção "Protocolo Agent()" com estas instruções:

```markdown
## Protocolo Agent()

Quando executado como Agent() (sem interação direta com o usuário), siga estas regras adicionais:

### Antes de executar
1. Leia o bloco ---TAREFA--- para entender o objetivo
2. Leia o bloco ---CONTEXTO--- e LEIA os arquivos referenciados nele (especialmente identidade de marca). O contexto vem como caminhos de arquivo — use Read pra carregar cada um antes de executar.
3. Leia o bloco ---MEMORIAS--- para aplicar preferências do usuário
4. Verifique se o contexto é suficiente para produzir com qualidade:
   - Se falta dado que não existe → reporte NEEDS_DATA
   - Se dado existe mas é insuficiente → reporte INSUFFICIENT_DATA
   - Se precisa de contexto não passado → reporte NEEDS_CONTEXT
5. Só execute se tiver o mínimo necessário para produzir com qualidade

### Durante a execução
- Siga os mesmos frameworks, personas e padrões do modo Skill()
- Use templates anteriormente preenchidos como base (preenchimento sequencial)
- NUNCA invente dados — use apenas o que foi fornecido no contexto
- Aplique as regras do bloco ---REGRAS---

### Ao concluir
- Reporte usando o formato ---REPORT--- / ---END-REPORT---
- Inclua o resultado completo (não resumido) no campo RESULTADO
- Liste todos os arquivos gerados ou modificados no campo ARQUIVOS
```

A seção específica de cada agente pode adicionar itens ao "Antes de executar" conforme suas necessidades (ex: Pesquisador verifica index de pesquisas, QA verifica checklists).
