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
| `NEEDS_DATA` | Faltam dados que não existem em lugar nenhum **OU** path do artefato/canário inválido **OU** token/MD5 do canário diverge do TAREFA | Cria entrevista(s)/pesquisa(s) **OU** Maestro investiga path/canário antes de re-despacho |
| `NEEDS_CONTEXT` | Precisa de informação que existe mas não foi passada | Re-despacha com mais contexto (sem criar entrevista) |
| `INSUFFICIENT_DATA` | Dado foi passado mas é insuficiente pra produzir com qualidade | Cria entrevista de aprofundamento e/ou pesquisa complementar |
| `NEEDS_DECISION` | Há ponto(s) de decisão estratégica ambíguo(s) que exigem escolha do usuário | Executa Fluxo 5.11 — monta AskUserQuestion com opções, re-despacha com bloco DECISOES |
| `BLOCKED` | Não consegue executar por outro motivo | Avalia: re-despacha com modelo mais capaz, quebra a tarefa, ou escala pro usuário |

### Diferenças-chave

- **NEEDS_DATA** → o dado **não existe em lugar nenhum** — precisa ser coletado do usuário ou pesquisado. **Ou** problema técnico de despacho de Revisor/QA: path do artefato ausente/inválido/vazio/timeout, path do canário ausente/inválido/malformado, token divergente, MD5 do artefato divergente. Maestro investiga sem criar entrevista.
- **NEEDS_CONTEXT** → o dado **provavelmente existe** (num template, memória ou arquivo) mas o agente não recebeu
- **INSUFFICIENT_DATA** → o dado **foi passado** mas não tem profundidade ou qualidade suficiente
- **PARTIAL** → a execução **começou**, mas não terminou. Parte das escritas foi feita; o resto não. Diferente de `NEEDS_CONTEXT`: `PARTIAL` reporta estado parcial após executar; `NEEDS_CONTEXT` reporta antes de executar, pedindo input
- **NEEDS_DECISION** → há ambiguidade **estratégica** em ponto canônico (formato de lançamento, arquétipo, etc.). Diferente de `NEEDS_DATA`/`NEEDS_CONTEXT`: contexto está completo, mas múltiplos caminhos são válidos — o usuário precisa escolher. Ver `protocolo-decisoes-estrategicas.md`

### Precedência de status

Se o agente detecta múltiplos problemas simultâneos, reporta **apenas um** status, obedecendo esta ordem:

`BLOCKED (dado cru ausente)` > `NEEDS_DATA` > `INSUFFICIENT_DATA` > `NEEDS_CONTEXT` > `NEEDS_DECISION`

Racional:
- **BLOCKED por dado cru ausente** vence quando o especialista (tipicamente Performance) precisa de input que não vive na Biblioteca (CSV, dashboard, prints). Sem o cru, cadastro de produto/identidade não resolve análise — não adianta perguntar dossiê quando faltam métricas pra analisar.
- **NEEDS_DATA** vence sobre os outros dentre dados-de-Biblioteca: dado objetivo faltando (entrevista/pesquisa) bloqueia tudo.
- **INSUFFICIENT_DATA** vem antes de NEEDS_CONTEXT porque dado parcial é problema mais urgente que contexto não-passado.
- **Decisão estratégica** só faz sentido com contexto completo. Ex: não adianta perguntar formato de lançamento se o ticket do produto é desconhecido.

**Sub-precedência interna ao especialista (Grupo 9):** antes de checar dependências da Tabela, especialista resolve ambiguidade de qual produto via `NEEDS_CONTEXT` (se o pedido menciona produto sem slug claro). Evita abrir cascata pra produto errado.

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

DECISOES_PENDENTES:
[Apenas se STATUS = NEEDS_DECISION. Formato delimitado por marcadores explícitos —
 ver seção 5 do protocolo-decisoes-estrategicas.md pra estrutura completa.]

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

[fim-opcoes]
recomendacao: <label>
justificativa: <por que>
---END-DECISOES-PENDENTES---

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
Caminho do canário: [{projeto}/memorias/auditoria/canarios-ativos/{slug}.md]
  # Apenas pra Revisor/QA em audit-on-file. Subagent lê artefato + canário.
  # Cita `[VERIF] {token} | MD5 {md5-esperado}` como 1a linha do RESULTADO.
  # Maestro grep pós-dispatch (Seção 9 deste protocolo).
Formato de entrega: [Markdown Obsidian-first com frontmatter YAML e wiki-links]
Protocolo de report: Seguir o formato definido em protocolo-agent.md (seção 2)
---END-TAREFA---
```

### Campos adicionais no REPORT do Gerente (fluxos de plano)

Nos fluxos de plano (`persistir-plano-rascunho` Fluxo 4b, `criar-plano-correcao` Fluxo 8 e variantes 4-revisao/4-regerar/4-reativar), o REPORT do Gerente inclui campos específicos. Pra fluxos de criação:

```
PLANO-PERSISTIDO: [caminho absoluto do arquivo do plano criado]
TABELA-DE-TAREFAS: |
  [tabela transcrita literalmente do bloco DECOMPOSICAO-PLANO do especialista decompositor.
   Colunas: # | Tarefa | Agente | Tipo de artefato | Depende de]
```

Pra plano em revisão / regerado / reativado, ver formatos específicos em `gerente/SKILL.md` Seção 7.

### Prompt cache em chamadas múltiplas no Fluxo de Plano

No Fluxo de Plano (2 gates), o mesmo especialista é despachado **2x na mesma sessão**:
- Chamada 1 (Fase 1): overview no chat (`MODO: decompor-plano-fase-1`).
- Chamada 2 (Fase 2): bloco DECOMPOSICAO-PLANO completo (`MODO: decompor-plano-fase-2`).

Bloco CONTEXTO **idêntico** entre as 2 chamadas → **prompt cache hit ~80% redução**. Custo total fica ~1.2x de uma chamada Sonnet única.

Iteração em em-revisao (Gate 2 ajustar estratégico, `MODO: decompor-plano-em-revisao`) também reusa CONTEXTO → cache hit.

> **Enum de status do plano** (referência cruzada com `plano.md` template): `rascunho | em-revisao | aprovado | em-execucao | aguardando-validacao | concluido | rejeitado | cancelado`. O status `em-revisao` é alcançado quando usuário pede "Ajustar estratégico" no Gate 2.

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

Pra **Revisor e QA**, presença de `caminho-do-artefato:` E `caminho-do-canario:` dispara modo "audit-on-file" (Camadas 1 + 2 da defesa B-S59-1 — ver Seção 9). Quando ausentes, Revisor opera em "audit-on-text" (texto inline — `fluxo-refinamento.md`).

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

### Regra de invocação Agent() entre especialistas

Especialistas **criativos** em modo Skill() (Estrategista, Marca, Copywriter, Mídias Sociais, Performance) **NÃO invocam Agent() de outros especialistas criativos**. Se a sub-tarefa precisa de outro especialista criativo, retorna controle ao usuário com sugestão ("esse pedaço é da Marca, quer que eu te redirecione?").

Invocação de agentes **operacionais** (Gerente, Bibliotecário, Pesquisador, Entrevistador, QA, Revisor) via Agent() continua permitida — esses não reportam `NEEDS_DECISION`.

---

## 6. Modo Rascunho (sem report)

Despacho em modo rascunho (acionado via `/rascunho` ou quando o classificador do Maestro retorna `tipo=Rascunho`) usa contrato mais leve que os outros modos:

- **Sem `---REPORT---`:** especialista retorna conteúdo livre diretamente, sem bloco de report estruturado.
- **Sem QA, Revisor ou Gerente:** pipeline curto — Maestro despacha, especialista entrega, Maestro salva.
- **Bloco obrigatório de retorno:** ao final da resposta (após todo o conteúdo produzido), incluir:

      ---TAGS-RASCUNHO---
      - tema/<valor>
      - produto/<valor>   # omitir se não aplicável
      ---END-TAGS-RASCUNHO---

  Delimitadores literais. O Maestro parseia e escreve em `tags-dominio:` + espelha em `tags:`.

Ver `protocolo-tags-rascunho.md` pra matriz relaxada (tema obrigatório, produto opcional) e regras de validação.

Este modo aplica-se aos 5 especialistas criativos (Copywriter, Estrategista, Marca, Mídias Sociais, Performance) e ao Pesquisador. Entrevistador, Bibliotecário, Gerente e QA/Revisor não recebem despacho em modo rascunho.

---

## 7. Quando o Gerente NÃO entra no caminho

A regra "todo despacho de especialista passa pelo Gerente" se aplica a **conteúdo criativo** — copy, pesquisa salva no vault, plano editorial, qualquer texto autoral em pt-br que o usuário lerá depois. Operações mecânicas que não produzem conteúdo autoral ficam fora do pipeline:

| Operação | Despacho | Por quê fica fora do pipeline |
|---|---|---|
| Scaffold de biblioteca (criar pastas, copiar templates) | `Skill("maestro:bibliotecario")` direto | Sem texto criativo. QA + Revisor não têm o que validar. Rastreabilidade já vive em git. |
| Coleta de dados via Entrevistador, dentro de pipeline já ativo | `Skill("maestro:entrevistador")` invocado pelo especialista | Especialista já está dentro do pipeline (tarefa criada, dispatch via `Agent()`). Entrevistador preenche templates fechados via diálogo, não produz copy. Recursão pelo Gerente é desnecessária. |
| Validação descartável de API/conexão | Resposta direta na conversa | Sem artefato salvo no vault. |

**Critério decisor:** o resultado da operação fica salvo no vault como **entrega**? Tem texto autoral em pt-br que o usuário lerá depois? Então pipeline obrigatório (Gerente cria tarefa → especialista via `Agent()` → ciclo QA + Revisor → Gerente conclui). Senão, despacho direto via `Skill()` é aceitável.

**Pesquisa é conteúdo criativo, não operação mecânica.** Pesquisas vão pra `pesquisas/`, viram referência consultada depois e contêm texto autoral em pt-br. Toda pesquisa, inclusive a inicial do onboarding (step 2.9 / 2B.5 do `maestro-onboarding`), passa pelo pipeline completo via `fluxo-entrega.md`.

**Bibliotecário e Entrevistador como exceções formais.** Skills paralelas ao hub (como `maestro-onboarding`) podem invocá-los direto via `Skill()`. Esta é a única forma legítima de invocação fora do hub do Maestro.

---

## 8. Quem aplica correções pós-Revisor

**Regra absoluta:** toda correção pós-Revisor passa pelo especialista que produziu o artefato. Sem exceção, sem gradiente "menor". Origem: B-S55-47 da Sessão 56 (6 reincidências escaladas).

### Fluxo canônico (revisão necessária)

1. Especialista da tarefa pai produz artefato → DONE
2. Revisor reprova → reporta `NEEDS_REVISION` com lista de correções
3. Maestro despacha Gerente (`FLUXO: criar-revisao`) → cria **tarefa-filha** de categoria `revisao` com agente herdado (rodadas 1-2) ou `agente: usuario` (rodada 3, ver `fluxo-needs.md`)
4. Maestro despacha especialista da tarefa-filha via `Agent()` com bloco CONTEXTO incluindo correções do Revisor
5. Especialista aplica via `Edit` no `caminho-do-artefato` existente, re-DONE
6. Re-Revisor → APPROVED (ou novo ciclo, max 3 rodadas)
7. Maestro despacha Gerente (`FLUXO: concluir-tarefa`) com payload incluindo `_ultima-correcao-por: <slug-especialista>` — Gerente persiste no frontmatter da tarefa-filha

### Tripwire (Gerente Fluxo 2 — concluir-tarefa)

Quando a tarefa sendo fechada tem TODAS as condições:
- `categoria: revisao` **E**
- `agente != "usuario"` **E**
- `_ultima-correcao-por` no payload é `"maestro"` OU ausente OU `null` **E**
- `status` não é `aprovado-com-pendencia`

→ Gerente retorna `BLOCKED` com `referencia-tecnica: B-S55-47` + `hint-pro-maestro` pra traduzir pro usuário em linguagem natural (ver `plugin/skills/maestro/limites-maestro.md` seção 4).

Detalhes da implementação em `plugin/skills/gerente/SKILL.md` Fluxo 2.

### Caso fronteira: pendência aceita (rodada 3 do ciclo)

Quando o ciclo de revisão chega na rodada 3 sem aprovação, Maestro abre `AskUserQuestion` obrigatório:
- "Aceitar como está com pendência registrada"
- "Reescrever do zero"
- "Cancelar tarefa"

Se usuário escolhe "aceitar com pendência", a tarefa-filha de revisão recebe `status: aprovado-com-pendencia` (campo já existente em `fluxo-entrega.md`). Maestro confirma pro usuário: *"Salvei como está. Anotei no histórico de pendências aceitas pra você revisar depois."* Tripwire não dispara.

### Cobertura limitada

O tripwire cobre o **fluxo principal** (Entrega + Plano com tarefas-filhas). Refinamento não passa pelo Gerente (não cria tarefa) — defesa do refinamento é só texto + TodoWrite. **Não cobre** despachos sem tarefa: Bibliotecário em scaffold, Entrevistador invocado por especialista dentro de pipeline ativo, Pesquisador em validação descartável de API. Esses casos seguem a regra absoluta por convenção (texto no hub) — auditoria contínua via painel `_violacoes-maestro-index.md`.

### Por que essa regra existe

- **Voz autoral:** Maestro genérico não tem o contexto de marca/tom/persona que o especialista carrega — correções diretas dele despersonalizam o texto
- **Aprendizado:** ver "QA e Revisor como auditores; especialista original aplica correções" no CLAUDE.md

---

## 9. Despacho de Revisor/QA — defesa anti-hallucination (B-S59-1)

Defesa em camadas pra dispatch audit-on-file. Princípio: canário em arquivo separado + challenge MD5 prova matematicamente que subagent leu artefato e canário, sem violar princípio "Maestro nunca escreve no vault de conteúdo".

### 9.1 Lifecycle do canário (4 passos obrigatórios)

**Passo 1 — Pre-dispatch (gerar token + MD5 + escrever canário):**

```bash
# Lazy-init (vault antigo pode não ter — DE-19)
mkdir -p {projeto}/memorias/auditoria/canarios-ativos/

# Gerar token (DE-13)
TOKEN="VERIF-$(python -c "import secrets; print(secrets.token_hex(3).upper()[:6])")"
# Fallback se Python ausente:
# TOKEN="VERIF-$(printf '%06X' $((RANDOM*RANDOM % 16777216)))"

# Calcular MD5 do artefato
MD5=$(md5sum {path-artefato} | cut -d' ' -f1)
# Fallback Windows: MD5=$(certutil -hashfile {path-artefato} MD5 | sed -n 2p | tr -d ' ')

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SLUG={slug-tarefa}
CANARIO={projeto}/memorias/auditoria/canarios-ativos/${SLUG}.md

# Write canário
cat > "$CANARIO" <<EOF
---
tarefa: $SLUG
artefato: {path-artefato-relativo}
token: $TOKEN
timestamp: $TIMESTAMP
md5-esperado: $MD5
---
Canário de verificação ativo. Subagente cita: [VERIF] $TOKEN | MD5 $MD5 na 1ª linha do RESULTADO.
EOF
```

Se Write OU md5sum falhar (DE-18) → Maestro retorna `NEEDS_DATA` ao invocador, **não despacha**.

**Passo 2 — Dispatch:**

Bloco TAREFA inclui:

```
Caminho do artefato: {path-artefato}
Caminho do canário: {projeto}/memorias/auditoria/canarios-ativos/{slug}.md
```

Subagent (Revisor/QA) lê os 2 arquivos.

**Passo 3 — Validação (pós-dispatch):**

```bash
PRIMEIRA_LINHA=$(echo "$REPORT" | grep -m1 "^\[VERIF\]")
ESPERADO="[VERIF] $TOKEN | MD5 $MD5"
if [ "$PRIMEIRA_LINHA" != "$ESPERADO" ]; then
  SUSPEITO=1
fi
```

- Match exato → leu (token + MD5 ambos provados).
- Diferente, ausente ou só parcial → suspeito de hallucination.
- Status `NEEDS_DATA` no report → falha legítima. Maestro investiga path/canário. Se 2x NEEDS_DATA seguidos → AUQ pro usuário.

**Passo 4 — Cleanup (pós-validação, sempre):**

```bash
rm "$CANARIO"
```

Roda mesmo se suspeito (não deixa órfão). Se `rm` falhar, próximo `/ola-maestro` cleanup pega (filtro >5min — DE-17).

### 9.2 Retry em caso de suspeita

Re-despacha **só os suspeitos**, sequencial. Cada retry: novo TOKEN, novo MD5 (artefato pode ter mudado), novo Write canário, novo dispatch, nova validação, novo cleanup.

**Cap de retries: 1.** Calibrado na Fase 0 do plano com medida real de dispatch Revisor (p95 ≈102s — pior caso de 2 retries sequenciais excederia tolerância de espera). Reavaliar quando hardware/modelo melhorar.

Cap atingido sem sucesso → BLOCKED com `referencia-tecnica: B-S59-1`. Maestro traduz pelo `limites-maestro.md` Seção 7 e abre AUQ DE-7.

### 9.3 Log obrigatório

Toda vez que defesa dispara retry OU loud-fail retorna NEEDS_DATA, Maestro escreve em `memorias/auditoria/historico.md`:

```
- {YYYY-MM-DD HH:MM} — defesa-anti-hallucination | agente: {revisor|qa} | causa: {token|md5|path|canario} | retry: {sucesso|falha} | tarefa: [[{slug}]]
```

Timestamp via `date +"%Y-%m-%d %H:%M"` (ver `protocolo-timestamp.md`).

### 9.4 Aplicabilidade

- **Audit-on-file** (TAREFA tem `caminho-do-artefato:` E `caminho-do-canario:`): canário + loud-fail aplicam.
- **Audit-on-text** (refinamento — `fluxo-refinamento.md` despacha Revisor com texto inline, sem path): SEM canário. Cobertura só Camada 2 + 3. Gap documentado.

### 9.5 Modo de operação do Revisor/QA

`caminho-do-artefato:` E `caminho-do-canario:` no bloco TAREFA disparam audit-on-file. Ausência de qualquer um → modo audit-on-text (Revisor) ou `NEEDS_DATA` (QA — sempre opera audit-on-file).
