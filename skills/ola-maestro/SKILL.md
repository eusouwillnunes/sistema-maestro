---
name: ola-maestro
description: >
  Abre a sessão de trabalho no Sistema Maestro. Apresenta dashboard completo
  com estado de tarefas, entrevistas, biblioteca e memórias. Adapta o nível
  de detalhe ao intervalo desde a última sessão.
---

> [!important] Antes de executar, verifique se o Sistema Maestro está ativo neste projeto seguindo o `core/protocolos/protocolo-ativacao.md`.
> Aplica: [[protocolo-interacao]]

> [!info] **Path resolution.** Toda escrita e Glob em pasta de vault usa `{projeto}/` resolvido pelo Maestro (via `protocolo-ativacao.md` Sub-fluxo 1). Nunca CWD direto nem path relativo.

# Olá, Maestro — Ritual de Abertura

## 1. Escopo

Esta skill é acionada quando:

| Gatilho | Ação |
|---------|------|
| `/ola-maestro`, iniciar sessão, abrir sessão, começar trabalho, bom dia, bom dia maestro | Ritual de abertura — dashboard |

### O que esta skill NÃO faz

- **Não cria ou atualiza tarefas** — usa o Gerente de Projetos para isso
- **Não roteia pedidos** — isso é papel do Maestro hub
- **Não conduz entrevistas** — isso é papel do Entrevistador
- **Não toma decisões de execução** — isso é papel do Gerente de Projetos
- **Não encerra sessão** — ritual de fechamento é skill separada

---

## 2. Fluxo (mapa de turnos)

> **Disparar todas as tool calls de um turno como chamadas paralelas em um único bloco.** Não serializar. Turnos adjacentes têm dependência de dados — não misturar turnos.

Antes de tudo, detectar projeto ativo conforme `core/protocolos/protocolo-ativacao.md`. O mapa abaixo assume que `{projeto}` já está resolvido.

### Turno 1 — Descoberta e leitura consolidada (paralelo, sem dependências)

Dispare as 7 tool calls abaixo em um **único bloco**:

- `Read` `~/.maestro/config.md`
- `Read` `{projeto}/{index-do-projeto}.md` (arquivo da raiz do projeto com `tipo: index` + `empresa:`; contém a tabela de status da biblioteca). Se o arquivo não existir, o dashboard omite a linha "Biblioteca" e mostra "Biblioteca: não configurada"
- `Glob` `{projeto}/memorias/sessoes/*.md`
- `Glob` `~/.maestro/sessoes-emergencia/*.md`
- `Glob` `{projeto}/tarefas/*.md`
- `Glob` `{projeto}/entrevistas/*.md`
- `Glob` `{projeto}/rascunhos/*.md`

**Importante:** `_tarefas.md`, `_entrevistas.md` e `_planos.md` são **painéis Dataview puros** desde o Grupo 6. Ler o arquivo via `Read` devolve só o texto da query, não os dados renderizados (Dataview só executa dentro do Obsidian). Por isso o Turno 1 não os inclui; a extração de contadores e metadados acontece no Turno 2 via `Bash grep` nos arquivos individuais.

**Exemplo canônico do Turno 1 (formato correto):** em **um único turno do modelo**, emitir as 7 chamadas paralelamente:

```
Read    ~/.maestro/config.md
Read    {projeto}/{index-do-projeto}.md
Glob    {projeto}/memorias/sessoes/*.md
Glob    ~/.maestro/sessoes-emergencia/*.md
Glob    {projeto}/tarefas/*.md
Glob    {projeto}/entrevistas/*.md
Glob    {projeto}/rascunhos/*.md
```

**Errado:** emitir uma chamada, esperar o retorno, emitir a próxima, esperar o retorno, etc. Isso serializa e anula o ganho do mapa de turnos.

### Turno 2 — Extração consolidada (paralelo, depende do Turno 1)

Dispare em um **único bloco** após o Turno 1 concluir:

- `Read` da sessão mais recente (primeiro arquivo da lista ordenada descendente retornada pelo glob em `memorias/sessoes/`) — precisa do corpo do arquivo
- `Bash` com grep consolidado extraindo frontmatters em lote de tarefas + entrevistas + rascunhos em uma única chamada:

  ```bash
  grep -HE "^(status|agente|titulo|objetivo|parte-de|prioridade|resultado|bloqueada-por|data-conclusao|data-inicio|data-cancelamento|motivo-cancelamento|template-destino|agente-solicitante|solicitante|grupo|categoria|expira-em|tags-dominio|tipo):" \
    {projeto}/tarefas/*.md {projeto}/entrevistas/*.md {projeto}/rascunhos/*.md 2>/dev/null || true
  ```

  - `-H` prefixa o nome do arquivo em cada linha pra permitir agrupamento posterior
  - `2>/dev/null` suprime erros de "No such file or directory" quando alguma pasta não existe
  - `|| true` evita que `set -e` aborte quando nenhum arquivo bate

- `Bash` adicional pra contar entradas pendentes em `feedback-revisor.md` (Grupo 7 — não processadas):

  ```bash
  # Conta cabeçalhos ### nas seções "Falsos negativos", "Falsos positivos" e "Padrões novos"
  # (exclui a seção "Processado" — última do arquivo)
  awk '/^## Processado/{exit} /^### /{c++} END{print c+0}' \
    {projeto}/memorias/feedback-revisor.md 2>/dev/null || echo 0
  ```

Turno 2 tem **3 tool calls** (1 Read + 2 Bash), independente do tamanho do vault — escala O(1) em tool calls, não O(N).

### Turno 3 — Montagem e interação (sequencial, sem mais I/O)

Sem novas leituras. Aplicar na ordem:

1. Cálculo de intervalo usando `data` do frontmatter da sessão mais recente (Seção 3)
2. Aviso de backup de emergência (se glob `sessoes-emergencia/` retornou arquivos) — oferecer cópia via `AskUserQuestion`
3. Recuperação de tarefa interrompida → Seção 6 (um `AskUserQuestion` por caso detectado no grep)
4. Higiene de rascunho → Seção 7 (um `AskUserQuestion` por expirado detectado no grep)
5. Montar dashboard (Seção 4)
6. `AskUserQuestion` final de opções (conforme [[protocolo-interacao]])

---

## 3. Cálculo de intervalo e leitura de sessões

Após o Turno 1 retornar a lista de arquivos em `memorias/sessoes/`, calcular quantos dias se passaram desde a última sessão e aplicar a tabela abaixo.

### Como calcular

1. Da lista retornada pelo glob `{projeto}/memorias/sessoes/*.md`, excluir `_sessoes.md` e pegar o primeiro arquivo (ordem descendente por nome — o prefixo `YYYY-MM-DD-HHMM` garante ordem cronológica natural).
2. No Turno 2 esse arquivo já foi lido — extrair `data` do frontmatter.
3. Calcular a diferença em dias entre `data` e a data atual.
4. Aplicar a tabela de comportamento.
5. Se a lista está vazia, é primeira sessão.

### Tabela de comportamento

| Intervalo | Frase no topo do dashboard | Quantidade carregada | Seção "Última sessão" |
|-----------|---------------------------|----------------------|------------------------|
| Primeira sessão | "Primeira sessão registrada!" | 0 | Omitir |
| 0-2 dias | "Última sessão: hoje / ontem / anteontem" | `max(N, 1)` | Resumo enxuto (1-2 linhas, só "parou em") |
| 3-7 dias | "Faz [X] dias desde a última sessão" | `max(N, 1)` | Resumo padrão (concluído + parou em + observações) |
| > 7 dias | "Faz [X] dias desde a última sessão — resumo mais completo" | `max(N, 3)` | Resumo expandido (últimas 2-3 sessões + recap geral) |

`N` = valor de `sessoes-ao-iniciar` no `~/.maestro/config.md` (default 1). Se ausente ou inválido (não-inteiro, ou negativo diferente de zero), avisar no dashboard ("config `sessoes-ao-iniciar` inválida, usando default `1`") e usar `1`.

### Decisão de fonte

| Situação | Fonte |
|----------|-------|
| `memorias/sessoes/` tem 1+ arquivo | Arquivos individuais |
| `memorias/sessoes/` vazio | Primeira sessão registrada |

### Detecção de backup de emergência

Se o glob `~/.maestro/sessoes-emergencia/*.md` retornou arquivos, antes de montar o dashboard avisar:

> "Detectei sessão(ões) em backup de emergência: [lista]. Quer copiar pra `{projeto}/memorias/sessoes/`? [Sim / Não agora]"

Se sim, copiar e remover do backup. Se não, continuar normalmente.

---

## 4. Dashboard

### Dashboard com tarefas

```markdown
[FRASE DO INTERVALO ADAPTATIVO — ex: "Faz 5 dias desde a última sessão"]

Bom dia! Aqui o estado do projeto **[Nome da Empresa]**:

## Resumo
- Tarefas: [N] concluídas, [N] em andamento, [N] bloqueadas, [N] pendentes, [N] canceladas
- Entrevistas: [N] pendentes, [N] em andamento, [N] concluídas
- Biblioteca: [N] templates preenchidos de [M] total
[Se feedback_pendentes ≥ 1: linha condicional]
- 📝 Revisor: [feedback_pendentes] feedbacks pendentes — rode `/maestro-revisar-memorias` quando quiser

[Se feedback_pendentes ≥ 10: bloco proativo após o resumo]

> 💡 Você tem [feedback_pendentes] feedbacks de Revisor parados. Vale rodar `/maestro-revisar-memorias` antes do próximo dispatch criativo — a calibragem do projeto pode estar saindo do alinhamento.

[Se pendencias_qualidade ≥ 1, renderizar bloco abaixo. pendencias_qualidade = contagem no grep do Turno 2 de tarefas com `status: aprovado-com-pendencia` OU (`categoria: revisao` E status diferente de `concluida`/`cancelada`). Se pendencias_qualidade == 0: omitir o bloco.]

> [!warning] Pendências de qualidade: [pendencias_qualidade] tarefa(s) com pendência aceita ou em revisão.
> Abrir `_qa-reprovacoes.md` pra revisar.

## O que pode ser feito agora
[Lista de tarefas pendentes (não bloqueadas), ordenadas por prioridade]
- **[Título]** ([Agente]) — [prioridade], grupo: [grupo]
[Se não há tarefas pendentes:] Nenhuma tarefa pronta pra executar.

## O que depende de você
[Lista detalhada de entrevistas — cada uma com nome, objetivo e prioridade]
- **[[entrevista-1]]** (prioridade: alta) — [objetivo resumido]
  Solicitada pelo agente de [nome]. Template destino: [[template]]
- **[[entrevista-2]]** (prioridade: média) — [objetivo resumido]
[Se há entrevista em andamento:]
- 🔄 **[[entrevista-em-andamento]]** — iniciada em [data], incompleta
[Se há entrevistas pendentes, oferecer:]
Quer resolver agora? Posso acionar o Entrevistador.

## O que está rodando
[Lista de tarefas/pesquisas em execução via Agent() em background]
- **[Título]** ([Agente]) — iniciada na sessão atual/anterior
[Se nada está rodando:] Nenhuma tarefa em background no momento.

## O que está bloqueado
[Lista de tarefas bloqueadas com motivo específico]
- **[Título]** — bloqueada por: [[bloqueador]] ([status do bloqueador])

## Última sessão ([data] [hora])
[Conteúdo varia conforme intervalo adaptativo — ver Seção 3:]

[0-2 dias — resumo enxuto:]
- **Parou em:** [ler `parou-em` do frontmatter do arquivo mais recente]

[3-7 dias — resumo padrão:]
- **Foco:** [foco do frontmatter]
- **Concluído:** [lista de tarefas/entregas concluídas — ler da seção "Concluído" do corpo]
- **Parou em:** [`parou-em` do frontmatter]
- **Observações:** [última seção "Observações" do corpo]

[Mais de 7 dias — resumo expandido: mostrar as últimas 2-3 entradas carregadas]
## Últimas sessões
- **[data-1] ([foco-1]):** [parou-em]
- **[data-2] ([foco-2]):** [parou-em]
- **[data-3] ([foco-3]):** [parou-em]
- **Recap geral:** [estado atual do projeto em 2-3 frases]
```

Após apresentar o dashboard, usar `AskUserQuestion` (conforme [[protocolo-interacao]]) com opções baseadas no estado atual. Montar as opções dinamicamente:

- Se há entrevistas pendentes: incluir opção "Resolver entrevistas" com description = "Tem [N] pendente(s): [nomes]"
- Se há tarefas prontas (não bloqueadas): incluir opção "Executar tarefa" com description = "[título da tarefa mais prioritária]"
- Se há tarefas bloqueadas por entrevista: incluir opção "Desbloquear tarefas" com description = "Resolver o que trava [N] tarefa(s)"
- Sempre incluir: "Outra coisa" com description = "Pedir algo novo ou diferente"

Máximo 4 opções. Priorizar: entrevistas pendentes > tarefas desbloqueáveis > tarefas prontas > outro.

### Dashboard sem tarefas

Se o glob `{projeto}/tarefas/*.md` do Turno 1 retornou vazio ou só contém `_tarefas.md` (nenhuma tarefa criada):

```markdown
[FRASE DO INTERVALO ADAPTATIVO]

Bom dia! Projeto **[Nome da Empresa]** — sem tarefas registradas.

**Biblioteca:**
[Resumo rápido — scaffold existe? Quantos templates preenchidos de quantos total?]
```

Após apresentar o dashboard, usar `AskUserQuestion` (conforme [[protocolo-interacao]]):
- question: "Por onde quer começar?"
- options:
  - label: "Preencher identidade (Recomendado)", description: "Começa pela fundação: propósito, público, diferencial"
  - label: "Criar uma campanha", description: "Se já tem identidade pronta, vai direto pra ação"
  - label: "Pesquisar concorrentes", description: "Coleta dados de mercado antes de decidir"

### Dashboard sem projeto

Se não há projeto ativo detectado:

```markdown
Bom dia! Nenhum projeto ativo detectado.

Quer criar um novo projeto? Posso chamar o Bibliotecário pra montar a estrutura.
Ou se já tem um projeto, me diz o nome da empresa.
```

### Aviso rodapé: formato antigo

Se existir arquivo `{projeto}/memorias/sessoes.md` (formato antigo, único), adicionar no **rodapé** do dashboard (uma linha só, após todas as outras seções):

> ℹ Formato antigo `memorias/sessoes.md` detectado — não entra no dashboard. O `/tchau-maestro` oferece migração automática ao fechar a sessão (`tchau-maestro/SKILL.md` seção 7).

Sem parser do conteúdo, sem fallback, sem branch condicional adicional. A migração real fica a cargo do `/tchau-maestro` (comportamento pré-existente).

---

## 5. Regras do dashboard

- **Priorize o que o usuário pode resolver.** Entrevistas pendentes e tarefas prontas aparecem primeiro.
- **Mostre o que pode rodar autônomo.** Tarefas pendentes sem bloqueio que poderiam ser despachadas via Agent().
- **Ofereça ações concretas.** Quando há entrevistas pendentes, ofereça acionar o Entrevistador. Quando há tarefas prontas, ofereça executar.
- **Recupere contexto.** Use o `parou-em` do frontmatter da última sessão pra dar continuidade. Se ausente, use a primeira linha da seção "Em andamento" do corpo.
- **Seja conciso.** Não liste tarefas concluídas antigas. Só o que mudou no intervalo carregado.
- **Seções vazias podem ser omitidas.** Se não há nada rodando em background, omita "O que está rodando". Se não há bloqueios, omita "O que está bloqueado".
- **Adapte o nível de detalhe ao intervalo.** Quem voltou ontem não precisa do mesmo contexto de quem sumiu por 2 semanas.
- **Use wiki-links do corpo da sessão pra popular links do dashboard.** Tarefas, planos, entrevistas listados na sessão já são `[[wiki-link]]` — basta repetir.

---

## 6. Recuperação de tarefa interrompida

Usar os dados extraídos no **Turno 2** (Bash grep de `{projeto}/tarefas/*.md`) pra checar estado de pipelines incompletos. Também usar o glob de `~/.maestro/sessoes-emergencia/` do Turno 1 pra detectar backups órfãos.

1. **Filtrar** do resultado do Bash grep: tarefas com `status: em-andamento` que **não** têm `data-conclusao` preenchida no frontmatter.
2. **Verificar** se há backups de `TodoWrite` órfãos em `~/.maestro/sessoes-emergencia/` (situação em que o TodoWrite foi escrito mas o Gerente não chegou a criar a tarefa antes da sessão fechar).
3. **Pra cada caso detectado**, abrir `AskUserQuestion`:
   > "Tarefa [[x]] ficou aberta em DATA. Retomar de onde parou, cancelar ou forçar conclusão?"
4. **Se "retomar":** carregar o TodoWrite de onde parou (o próprio Maestro hub despacha a sub-skill correspondente e continua da etapa pendente).
5. **Se "cancelar":** disparar fluxo de cancelamento (sub-skill `fluxo-cancelamento.md`).
6. **Se "forçar conclusão":** Gerente fecha a tarefa com flag `conclusao: forcada-pelo-usuario` no frontmatter (rastreável).
7. Após retomada bem-sucedida, apagar o backup emergencial correspondente.

Essa checagem é defesa em profundidade — pega o caso em que a sessão fechou entre item 1 e item 2 do TodoWrite de Entrega (tarefa ainda não existia em `tarefas/`).

---

## 7. Política de rascunho

Ao final do dashboard, aplicar higiene dos rascunhos usando os dados extraídos no **Turno 2** (Bash grep de `{projeto}/rascunhos/*.md`):

1. **Filtrar** do resultado do grep: rascunhos com `expira-em < hoje` (ignorar rascunhos em subpasta `rascunhos/arquivados/` — se o glob do Turno 1 já os excluiu, ótimo; senão, filtrar aqui pelo caminho).
2. **Pra cada expirado**, abrir `AskUserQuestion`:
   > "Rascunho [[x]] venceu em YYYY-MM-DD. Promover, arquivar ou apagar?"
3. **Aplicar escolha imediatamente:**
   - **Promover:** dispara `/promover [[x]]` (fluxo completo de Entrega)
   - **Arquivar:** move pra `rascunhos/arquivados/`, atualiza `status: arquivado`
   - **Apagar:** remove arquivo
4. **Contar ativos** (fora de `arquivados/`) — também a partir do mesmo resultado do grep:
   - **Se ≥20:** avisar no dashboard: "Você tem N rascunhos abertos (limite 20). Recomendo limpar 1-2 antes de criar novos."
   - **Se 4-19:** agrupar por `tema/*` dominante lendo `tags-dominio` do frontmatter (campo já extraído pelo Bash grep). Exibir sumário: `Ativos: N rascunhos → tema/autoridade (3), tema/vendas (2), sem tema (1)`. Bucket `sem tema` cobre rascunhos sem `tags-dominio` preenchido (caso "especialista não sugeriu" ou legado pré-Grupo D).
   - **Se ≤3:** manter listagem plana de arquivos (comportamento atual).

Política inegociável: rascunho vencido bloqueia criação de novos até o usuário decidir.

---

## 8. Restrições

- **Nunca crie ou atualize tarefas diretamente.** Use o Gerente de Projetos.
- **Nunca roteia pedidos.** Isso é papel do Maestro hub.
- **Nunca bloqueie o usuário.** O ritual é opt-in. Se o usuário pedir algo direto, o Maestro segue o fluxo normal.
- **Nunca invente dados de sessões anteriores.** Se `sessoes/` está vazio, diga "Primeira sessão registrada!".
- **Nunca modifique arquivos de sessão.** Leitura apenas. A escrita é papel do `/tchau-maestro`.

---

### Cascatas em andamento (Grupo 9)

No Turno 2 (Bash grep consolidado de frontmatters), incluir verificação de cascatas:

```bash
# Tarefas com cascata em andamento (status bloqueada + entrevistas-cascata não-vazio)
grep -l "^entrevistas-cascata:" {projeto}/tarefas/*.md 2>/dev/null
```

Pra cada match, ler frontmatter e renderizar:

```
### 🔄 Cascata pendente: [titulo da tarefa]
- Entrevistas: [N concluídas] de [M total]
- Próxima: [[entrevista-X]] (~5-7 min)
- Tempo restante estimado: ~[(M-N)*7] min

Pra continuar: rode `/entrevistador continua` ou abra a próxima entrevista no Obsidian.
```

Quando há ≥1 cascata pendente, sempre renderiza esta seção no dashboard (logo após "Tarefas em andamento" e antes de "Rascunhos").
