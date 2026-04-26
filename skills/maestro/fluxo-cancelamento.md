# Fluxo de Cancelamento

> Aplica: [[protocolo-timestamp]]

Sub-skill lida pelo Maestro via `Read` quando o classificador retorna `tipo=Cancelamento`.

## TodoWrite obrigatório (5 itens fixos)

1. `Confirmar pedido + identificar escopo`
2. `Validar consistência (tarefa/plano existe, estado atual)`
3. `Executar cancelamento (status, frontmatter, cascata)`
4. `Atualizar índices afetados`
5. `Reportar ao usuário`

## Passo a passo — Cancelamento de tarefa

### Item 1 — Confirmar pedido + identificar escopo

1. Matching case/accent-insensitive, em ordem de tentativa:
   - **Por slug** (ex: "cancela headlines-automators") → grep em `tarefas/*.md` + `planos/*.md` + `rascunhos/*.md`. Se 1 match → segue pro passo 2. Se ≥2 → AUQ listando candidatos. Se 0 → tentar próximo tipo abaixo.
   - **Por tipo genérico** (ex: "esquece o plano", "cancela a tarefa", "abandonei a pesquisa") → glob da pasta do tipo + filtrar por `status` ativo (não `concluida`, não `cancelada`). Se 1 → confirma. Se N → AUQ. Se 0 → "não encontrei [tipo] ativo". Tipos aceitos: `plano`, `tarefa`, `rascunho`, `pesquisa`, e qualquer tipo listado em `plugin/core/templates/artefatos/`. Palavras ambíguas ("o projeto") não batem aqui — caem no próximo tipo.
   - **Meta** (ex: "esquece o que eu pedi", "cancela o último", "aquilo que falamos") → resolver em 3 origens, em ordem:
     - **(a) Memória da conversa atual do Maestro** — artefatos criados nos turnos recentes (dispatches executados, TodoWrite com wiki-links de output, arquivos escritos nesta interação). Tem precedência máxima.
     - **(b) Fallback pra última sessão salva** — se memória atual está vazia ou usuário referencia algo mais antigo ("aquilo de ontem"), ler última sessão em `memorias/sessoes/` + pegar wiki-link mais recente em "Em andamento" ou "Concluído".
     - **(c) AUQ se ambíguo** — se (a) e (b) dão resultados diferentes ou nenhum dá certeza, abrir `AskUserQuestion` com 2-3 candidatos mais prováveis.
   - **Sem referência** ("deixa pra lá" sozinho, "esquece isso" sozinho) → AUQ listando os 5 artefatos ativos mais recentes pra usuário escolher.
2. Se ≥2 matches, abrir `AskUserQuestion` listando os candidatos.
3. Se 0 matches, abrir `AskUserQuestion` oferecendo buscar por substring diferente ou cancelar operação.
4. Quando 1 match único, confirmar via `AskUserQuestion`. Wording varia conforme o trigger:
   - **Trigger explícito** ("cancela [[x]]"): `AskUserQuestion` binário — "Cancelar [[x]]? Sim/Não".
   - **Trigger implícito** ("deixa pra lá [[x]]", "esquece o [[x]]", "abandonei [[x]]" etc.): `AskUserQuestion` com 3 ações — "Parece que você quer parar com [[x]]. **Cancelar** (status cancelada + motivo), **arquivar** (deixa salvo sem andar, não cancela), ou **deixar pendente** (volta depois)?" Se usuário escolher arquivar/deixar pendente, NÃO prossegue pro Item 2-5 deste fluxo — faz a ação escolhida e encerra. Arquivar = mudar status pra `arquivada` + nota no frontmatter. Deixar pendente = sem mudança de status, Maestro registra na sessão atual que usuário quis pausar.
5. Capturar motivo via `AskUserQuestion` com 4 opções comuns (Duplicada / Escopo mudou / Bloqueada por dependência / Outro) + campo livre.
6. Marcar item 1 `completed`.

### Item 2 — Validar consistência

1. Ler tarefa alvo. Checar `status` atual.
2. Se já `cancelada`: checar consistência dos derivados (artefato tem `status: cancelado`? tabela "Canceladas" em `_tarefas.md` atualizada? pendências do plano-pai?).
3. Se inconsistente, despachar Gerente em modo recuperação (completa o que falta).
4. Se `status: concluida` e usuário insiste em cancelar, abrir `AskUserQuestion` forte: "Tarefa já concluída. Cancelar cria incoerência. Confirma?".
5. Marcar item 2 `completed`.

### Item 3 — Executar cancelamento

1. Despachar Gerente em modo cancelar-tarefa com `tarefa-id`, `motivo`, e `data-cancelamento` lido via `Bash date +"%Y-%m-%dT%H:%M:%S"` — **nunca chutar hora** (ver `protocolo-timestamp`).
2. Gerente atualiza frontmatter da tarefa: `status: cancelada`, `data-cancelamento`, `motivo-cancelamento`.
3. Se tarefa tinha artefato associado, Gerente atualiza artefato: `status: cancelado`.
4. Se tarefa é filha de plano, Gerente atualiza plano-pai (checkbox cancelado, nota em corpo).
5. Marcar item 3 `completed`.

### Item 4 — Atualizar índices

1. Queries Dataview em `_tarefas.md` e `_planos.md` recalculam automaticamente (desde Grupo 6).
2. Gerente confirma presença da tarefa cancelada na tabela "Canceladas (últimas 15)".
3. Marcar item 4 `completed`.

### Item 5 — Reportar

Apresentar ao usuário:
- Tarefa cancelada com link
- Motivo registrado
- Efeito cascata aplicado (artefato cancelado, plano atualizado)
- Item 5 `completed`. TodoWrite 5/5.

## Passo a passo — Cancelamento de plano

Mesma lógica, adaptada:

1. Matching em `planos/*.md`.
2. Validação de consistência inclui todas as tarefas-filhas (cada uma deve receber cascata).
3. Execução cancela plano + N tarefas-filhas + N artefatos (com `AskUserQuestion` de confirmação: "Cancelar X tarefas-filhas em cascata? Sim/Não/Selecionar").
4. Atualização de índices afetados (`_planos.md` e `_tarefas.md`).
5. Report mencionando escopo total do cancelamento.

## Protocolo de recuperação (cancelamento interrompido)

Se Fluxo 3 foi interrompido no meio:
- Gerente detecta inconsistência no Item 2 da próxima execução de cancelamento.
- Modo recuperação completa apenas os passos que faltaram (idempotente, não refaz do zero).

## Regras absolutas

1. Cancelamento sempre passa por confirmação explícita via `AskUserQuestion`.
2. Estado terminal (tarefa cancelada) não cancela novamente — vai direto pra validação de consistência em recuperação.
3. Cascata de plano → tarefas-filhas sempre pede confirmação.
