---
name: tchau-maestro
description: >
  Encerra a sessão de trabalho no Sistema Maestro. Registra progresso
  detalhado em arquivo individual na pasta `memorias/sessoes/`, apresenta
  passos baseados em impacto e dependências.
---

> [!important] Antes de executar, verifique se o Sistema Maestro está ativo neste projeto seguindo o `core/protocolos/protocolo-ativacao.md`.
> Aplica: [[protocolo-interacao]]
> Aplica: [[protocolo-timestamp]]
> Aplica: [[protocolo-biblioteca]] (seção "Wikilinks em frontmatter")

# Tchau, Maestro — Ritual de Fechamento

## 1. Escopo

Esta skill é acionada quando:

| Gatilho | Ação |
|---------|------|
| `/tchau-maestro`, encerrar sessão, fechar sessão, parar por hoje, chega por hoje | Ritual de fechamento — resumo e registro |

### O que esta skill NÃO faz

- **Não cria ou atualiza tarefas** — usa o Gerente de Projetos para isso
- **Não roteia pedidos** — isso é papel do Maestro hub
- **Não conduz entrevistas** — isso é papel do Entrevistador
- **Não toma decisões de execução** — isso é papel do Gerente de Projetos

---

## 2. Fluxo (mapa de turnos)

> **Disparar todas as tool calls de um turno como chamadas paralelas em um único bloco.** Não serializar.

Antes de tudo, detectar projeto ativo conforme `core/protocolos/protocolo-ativacao.md`. O mapa abaixo assume que `{projeto}` já está resolvido.

### Turno 1 — Descoberta paralela (5 calls num único bloco, sem dependências)

Dispare em **um único turno do modelo**:

- `Glob` `{projeto}/tarefas/*.md`
- `Glob` `{projeto}/planos/*.md`
- `Glob` `{projeto}/entrevistas/*.md`
- `Glob` `{projeto}/rascunhos/*.md`
- `Glob` `{projeto}/memorias/sessoes/*.md`

**Importante:** `_tarefas.md`, `_planos.md`, `_entrevistas.md`, `_rascunhos.md` são **painéis Dataview puros** desde o Grupo 6 (e v2.15.0 expande pras 9 áreas dinâmicas). `Read` direto retorna só o texto da query, não os dados renderizados (Dataview só executa dentro do Obsidian). Por isso o Turno 1 usa `Glob` direto na pasta dos artefatos individuais.

### Turno 2 — Extração paralela (1 call, depende do Turno 1)

Após o Turno 1 retornar, dispare 1 `Bash` com grep consolidado:

```bash
grep -HE "^(status|agente|titulo|parte-de|prioridade|resultado|bloqueada-por|data-conclusao|data-inicio|data-cancelamento|motivo-cancelamento|grupo|categoria|expira-em|tags-dominio|tipo|foco|parou-em|corrige|correcoes|regera):" \
  {projeto}/tarefas/*.md {projeto}/planos/*.md {projeto}/entrevistas/*.md {projeto}/rascunhos/*.md 2>/dev/null || true
```

- `-H` prefixa o nome do arquivo em cada linha pra permitir agrupamento posterior
- `2>/dev/null` suprime erros de "No such file or directory" quando alguma pasta não existe
- `|| true` evita que `set -e` aborte quando nenhum arquivo bate

Turno 2 escala **O(1) em tool calls**, não O(N).

### Turno 3 — Montagem e gravação (sequencial, sem mais I/O)

Aplicar na ordem:

1. **Verificar se projeto tem `sessoes.md` legado** — se o glob `memorias/sessoes/` retornou nada e o projeto tem o arquivo `sessoes.md` antigo com mais de 5 entradas, seguir pra Fluxo de Migração Opt-in (seção 7). Caso contrário, pular.

2. **Inferir foco da sessão** (ver seção 5) — usar dados do Turno 2 filtrando por `tipo = "plano" AND status = "em-andamento"` em vez de `Read` raw de `_planos.md`.

3. **Confirmar foco via `AskUserQuestion`:**
   - question: "Foco desta sessão: `{foco-inferido}`. Usar este nome?"
   - options:
     - label: "Sim, usar `{foco-inferido}`", description: "Nome gerado pela heurística"
     - label: "Editar o foco", description: "Abre prompt livre pra você digitar"
     - label: "Usar `sessao-geral`", description: "Fallback quando nenhum foco faz sentido"

   Se o usuário escolher "Editar o foco", perguntar o slug em texto livre. Normalizar conforme `plugin/core/templates/_sessao-template.md` seção "Normalização do slug".

4. **Gerar path do arquivo:**
   - `data` = hoje via `Bash date +%Y-%m-%d`
   - `hora` = via `Bash date +%H%M` (HHMM sem dois-pontos)
   - `foco` = slug aprovado normalizado
   - Path: `{projeto}/memorias/sessoes/{data}-{hora}-{foco}.md`

5. **Criar pasta `{projeto}/memorias/sessoes/` se não existir** — `mkdir -p` via Bash.

6. **Criar `_sessoes.md` se não existir** — copiar conteúdo do template `plugin/core/templates/_sessoes-index-template.md`. Só criar uma vez, não sobrescrever.

7. **Escrever wiki-links referenciando arquivos descobertos no Turno 1** — `file.name` do glob é o nome real do arquivo; a pasta é `tarefas/`, `planos/`, `entrevistas/`, `rascunhos/`. Formar wiki-link como `[[<pasta>/<file.name-sem-extensao>]]`. Não precisa `Read` adicional dos painéis Dataview.

8. **Escrever o arquivo de sessão** — frontmatter + corpo conforme seção 3 (Formato do registro). UTF-8 nativo, verificação pós-escrita (regra "UTF-8 nativo sem escape" em seção 6).

9. **Em caso de falha na escrita** — seguir Fluxo de Recuperação em Falha (seção 8).

10. **Apresentar resumo visual ao usuário** — conforme seção 4.

11. **Sugerir próximos passos com justificativa** — explicar por que aquela sugestão é a melhor (ex: "desbloqueia 3 tarefas").

12. **Oferecer resolver pendências antes de fechar** — se há entrevistas pendentes curtas, perguntar se quer resolver antes de encerrar.

---

## 3. Formato do registro

Cada sessão vira um arquivo individual em `{projeto}/memorias/sessoes/`, com nome `<YYYY-MM-DD-HHMM>-foco.md` onde o timestamp vem de `Bash date +"%Y-%m-%d-%H%M"` — **nunca chutar** (ver `protocolo-timestamp`).

### Frontmatter (mínimo)

Obter `data` via `Bash date +"%Y-%m-%d"` e `hora` via `Bash date +"%H:%M"` antes de gravar:

```yaml
---
tipo: sessao
data: <YYYY-MM-DD lido do sistema>
hora: "<HH:MM lido do sistema>"
foco: grupo-4-sessoes
parou-em: "frase curta descrevendo o ponto de retomada"
---
```

**Campos:**
- `tipo: sessao` — filtro obrigatório pra Dataview
- `data` — AAAA-MM-DD da sessão
- `hora` — string "HH:MM" (24h, com dois-pontos no frontmatter, apesar de o nome do arquivo usar HHMM sem dois-pontos)
- `foco` — slug normalizado (mesma string do nome do arquivo)
- `parou-em` — frase curta visível no dashboard do `/ola-maestro`

**NÃO adicionar contadores agregados** (tarefas-concluidas, modo-agent, etc.). Aprendizado do Grupo 3: "Dataview no corpo > contadores no frontmatter, evita desincronização." As estatísticas vivem no `_sessoes.md` via queries Dataview que leem os arquivos de tarefa reais.

### Corpo

```markdown
# Sessão 2026-04-20 14:30 — grupo-4-sessoes

## Concluído
- ✅ [[tarefas/tarefa-x]] ([agente], modo Agent/Skill)

## Em andamento
- 🔄 [[tarefas/tarefa-y]] — parou em: [detalhe específico]

## Bloqueado
- 🚫 [[tarefas/tarefa-z]] — bloqueada por: [[tarefas/bloqueador]]

## Entrevistas
- [[entrevistas/entrevista-x]] (concluída), [[entrevistas/entrevista-y]] (iniciada), [[entrevistas/entrevista-z]] (pendente)

## Pesquisas
- [[pesquisas/pesquisa-x]] — tema: [descrição]

## Pendências para próxima sessão
- ⏳ [[tarefas/tarefa-pronta-1]], [[tarefas/tarefa-pronta-2]]
- 📋 [[entrevistas/entrevista-pendente-1]]

## Parou em
[Frase curta — a "bússola" pro retorno na próxima sessão]

## Observações
[Padrões notados, preferências expressas, decisões tomadas]
```

### Regra obrigatória: wiki-links

Toda menção a tarefa, plano, entrevista ou pesquisa concluída na sessão deve ser `[[pasta/slug]]` (com path — ver `protocolo-biblioteca` seção "Wikilinks em frontmatter").

O nome real do arquivo já vem do **Turno 1** (`Glob` retorna `file.name`); a pasta vem do path do glob (`tarefas/`, `planos/`, `entrevistas/`, `rascunhos/`). **Não consultar os painéis Dataview** (`_tarefas.md` etc.) — eles são queries, não fontes de dados.

Sem wiki-links com path, o grafo do Obsidian pode resolver errado quando dois arquivos compartilham slug em pastas diferentes. Isso é rastreabilidade essencial do sistema.

### Seções vazias

Omitir seções sem conteúdo. Se não há nada bloqueado, a seção "Bloqueado" inteira sai do arquivo.

---

## 4. Resumo visual

Apresentar ao usuário após salvar o registro:

```markdown
Sessão encerrada! Resumo:

**Concluído hoje:**
- ✅ [lista com agente e modo de execução]

**Em andamento:**
- 🔄 [lista com detalhe de progresso — ex: "entrevista X: 3 de 5 perguntas"]

**Entrevistas:**
- 📋 [N] concluídas hoje, [N] pendentes na fila

**Pendências para próxima sessão:**
- ⏳ [N] tarefas prontas para executar
- 📋 [N] entrevistas pendentes [oferecer: "quer resolver alguma agora antes de fechar?"]
- 🚫 [N] tarefas bloqueadas

**Sugestão para próxima sessão:**
[O que faz mais sentido atacar primeiro, com base em:]
- Tarefas que desbloqueiam mais coisas (maior impacto)
- Entrevistas que desbloqueiam tarefas de alta prioridade
- Templates da biblioteca que são pré-requisito de outros
```

---

## 5. Inferência determinística do foco

O foco da sessão é inferido pelo `/tchau-maestro` por heurística simples e previsível. A ordem é:

1. **Plano ativo** — filtrar resultado do Turno 2 por `tipo = "plano" AND status = "em-andamento"`. Se houver match, usar o slug do plano como foco. **Não ler `_planos.md` raw** — o painel é Dataview puro e retornaria só texto da query.

2. **Última tarefa concluída na sessão** — se não há plano ativo, identificar a tarefa concluída mais recente da sessão. Extrair o slug do nome do arquivo da tarefa (ex: `2026-04-20-1200-refator-ola-maestro.md` → `refator-ola-maestro`).

3. **Grupo em progresso** — se não há nem plano nem tarefa com slug claro, abrir `tasks.md` e procurar pela primeira seção `## Em Progresso` ou `### P1 — Grupo X`. Usar o slug do grupo (ex: "Grupo 4: Sessões como arquivos separados" → `grupo-4-sessoes`).

4. **Fallback** — se nada acima retornar slug, usar `sessao-geral`.

### Por quê determinística

Evita improvisação do modelo. O usuário sempre sabe como o foco foi escolhido. Quando a heurística erra, o `AskUserQuestion` do fluxo (passo 4) dá a chance de editar.

### Normalização do slug

Aplicar sempre depois de decidir o foco:

1. Lowercase
2. Remover acentos (NFD + strip diacríticos)
3. Substituir espaços e pontuação por hífens
4. Remover hífens duplicados
5. Truncar em 40 caracteres
6. Remover hífens nas pontas

---

## 6. Regras do fechamento

- **Seja factual.** Registre o que aconteceu, não o que deveria ter acontecido.
- **Registre progresso detalhado.** "[[entrevistas/entrevista-x]]: 3 de 5 perguntas respondidas" é melhor que "entrevista em andamento".
- **Use wiki-links com path em toda menção a artefato.** Tarefas, planos, entrevistas e pesquisas sempre como `[[<pasta>/<slug>]]` (ver `protocolo-biblioteca` seção "Wikilinks em frontmatter"). Resolve pelo `Glob` do Turno 1, não pelos painéis Dataview.
- **Sugira próximos passos com justificativa.** Explique por que aquela sugestão é a melhor (ex: "desbloqueia 3 tarefas").
- **Ofereça resolver pendências antes de fechar.** Se há entrevistas pendentes curtas, pergunte se quer resolver.
- **Não force fechamento.** Se o usuário quer continuar, não insista.
- **Crie `sessoes/` e `_sessoes.md` se não existem.** Pasta com `mkdir -p`; índice copiado do template.
- **UTF-8 nativo sem escape.** Ao gravar, escreva `ç`, `ã`, `é`, `—` de forma nativa. Nunca emita `\u00e7`, `\u00e3`, `\u2014`.
- **Verificação pós-escrita.** Após o `Write`, releia o arquivo. Se encontrar o padrão `\uXXXX`, faça nova `Write` substituindo cada ocorrência pelo caractere nativo correspondente. Não considere o fechamento concluído enquanto houver Unicode escapado.

---

## 7. Migração opt-in de `sessoes.md` legado

Executado apenas quando o projeto tem `{projeto}/memorias/sessoes.md` com mais de 5 entradas (cabeçalhos `### [AAAA-`).

### Fluxo

1. **Perguntar via `AskUserQuestion`:**
   - question: "Detectei `sessoes.md` com [N] entradas antigas. Quer que eu migre as 5 mais recentes pra pasta nova `sessoes/`?"
   - options:
     - label: "Sim, migrar 5 últimas", description: "Cria 5 arquivos individuais em sessoes/ com data original"
     - label: "Não, deixar como está", description: "sessoes.md permanece; novas sessões vão pra sessoes/"
     - label: "Perguntar depois", description: "Ignora por esta sessão; tchau-maestro pergunta de novo no próximo fechamento"

2. **Se aceitar migração:**
   - Parsear as 5 entradas mais recentes de `sessoes.md` (cabeçalhos `### [AAAA-MM-DD]` em ordem descendente)
   - Pra cada entrada, criar arquivo em `sessoes/{data}-0000-sessao-legada.md` com:
     - `data` = extraída do cabeçalho
     - `hora` = `"00:00"` (não havia hora no legado)
     - `foco` = `sessao-legada`
     - `parou-em` = extrair do bloco da entrada se houver "Parou em:" ou primeira linha de "Em andamento"; senão, deixar vazio
     - Corpo = converter o conteúdo da entrada pros campos novos quando possível; campos sem equivalência ficam em "Observações"
     - `migrada-de-legado: true` no frontmatter

3. **Preservar `sessoes.md` legado intocado.** A migração copia, não move. O arquivo original continua existindo.

4. **Se recusar ou "Perguntar depois":** não faz nada. Próximo `/tchau-maestro` pergunta de novo se ainda houver condição.

### Por quê opt-in e não automático

Inferir HHMM e slug retroativamente tem taxa de erro alta. Deixar o usuário decidir reduz risco de degradar o histórico. O arquivo legado fica intocado como garantia.

---

## 7.1 Backup emergencial de TodoWrite ativo

Antes de escrever a sessão e finalizar, checar se há pipeline incompleto:

1. **Checar se há `TodoWrite` ativo** — algum item com status `in_progress` ou `pending` sem todos os anteriores `completed`.
2. **Se sim:**
   - Extrair o conteúdo do TodoWrite (itens + status de cada)
   - Extrair o contexto do pedido original do usuário que iniciou o fluxo
   - Obter timestamp via `Bash date +"%Y-%m-%d-%H%M"` (nome) e `date +"%Y-%m-%d %H:%M"` (campo `sessao-encerrada`) — **nunca chutar** (ver `protocolo-timestamp`).
   - Salvar em `~/.maestro/sessoes-emergencia/todowrite-<YYYY-MM-DD-HHMM>.md`
   - Formato:
     ```yaml
     ---
     tipo: backup-todowrite
     sessao-encerrada: <YYYY-MM-DD HH:MM lido do sistema>
     pedido-original: [texto do usuário]
     tipo-classificado: [Entrega/Refinamento/Rascunho/Plano/Cancelamento]
     ---

     ## TodoWrite no momento do encerramento

     - [x] Item 1 — concluído
     - [ ] Item 2 — in_progress (parou aqui)
     - [ ] Item 3 — pending
     ...
     ```
3. **No próximo `/ola-maestro`**, Maestro detecta o arquivo na pasta de emergência e oferece retomada (ver `ola-maestro/SKILL.md` seção 6.1).
4. **Após retomada bem-sucedida**, o backup é apagado automaticamente.

Essa camada complementa o fluxo 8 (recuperação em falha de escrita) — a diferença é que aqui estamos encerrando sessão com pipeline incompleto deliberadamente, sem erro de escrita.

---

## 8. Fluxo de recuperação em falha de escrita

Se a escrita do arquivo de sessão falhar (permissões, disco cheio, etc.):

1. **Apresentar erro explícito ao usuário** com o caminho tentado e a mensagem de erro do sistema.

2. **Dump do conteúdo no terminal** — mostrar o conteúdo completo (frontmatter + corpo) em bloco de código Markdown, com aviso:
   > "A escrita falhou. Copie o conteúdo abaixo e salve manualmente em `{caminho}`. Também vou tentar salvar em backup de emergência."

3. **Segunda tentativa em path alternativo** — tentar gravar em `~/.maestro/sessoes-emergencia/{mesmo-nome-do-arquivo}.md`. Criar a pasta com `mkdir -p ~/.maestro/sessoes-emergencia/` se necessário.

4. **Avisar o usuário sobre a recuperação pendente:**
   > "Backup salvo em `~/.maestro/sessoes-emergencia/{nome}.md`. Na próxima execução de `/ola-maestro`, o sistema vai detectar o backup e oferecer recuperação."

5. **Registrar a falha como memória temporária** — opcional, mas útil: deixar comentário em `~/.maestro/sessoes-emergencia/_log-falhas.md` com data, caminho tentado, e motivo do erro.

### Por quê explícito

O modelo não tem "estado em memória" garantido entre turnos. O dump no terminal + backup em path alternativo são mecanismos concretos — funcionam mesmo se a conversa for encerrada antes da recuperação.

---

## 9. Restrições

- **Nunca crie ou atualize tarefas diretamente.** Use o Gerente de Projetos.
- **Nunca roteia pedidos.** Isso é papel do Maestro hub.
- **Nunca bloqueie o usuário.** O ritual é opt-in. Se o usuário pedir algo direto, o Maestro segue o fluxo normal.
- **Nunca toque no `sessoes.md` legado.** Mesmo na migração opt-in, o legado é preservado; a migração copia conteúdo, não move.
- **Nunca pule a confirmação de foco.** Mesmo quando a heurística é óbvia, o `AskUserQuestion` é obrigatório.
- **Sempre salve o registro de fechamento.** Mesmo que a sessão tenha sido curta. Se falhar, use o fluxo de recuperação da seção 8.
