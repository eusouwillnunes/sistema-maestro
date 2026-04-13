---
name: maestro:sessao
description: >
  Sub-skill do Maestro para rituais de sessão. Abertura apresenta dashboard
  completo com estado de tarefas, entrevistas e tarefas em background.
  Fechamento registra progresso detalhado e sugere próximos passos.
  Integrado com Entrevistador, Gestor de Tarefas e memórias de sessão.
---

> [!important] Antes de executar, verifique se o Sistema Maestro está ativo neste projeto seguindo o `core/protocolos/protocolo-ativacao.md`.
> Aplica: [[protocolo-interacao]]

# Maestro: Rituais de Sessão

## 1. Escopo

Esta sub-skill é acionada quando:

| Gatilho | Ação |
|---------|------|
| `/maestro:iniciar-sessao`, iniciar sessão, abrir sessão, começar trabalho, bom dia, bom dia maestro | Ritual de abertura — dashboard |
| `/maestro:encerrar-sessao`, encerrar sessão, fechar sessão, parar por hoje, chega por hoje | Ritual de fechamento — registro |

### O que esta sub-skill NÃO faz

- **Não cria ou atualiza tarefas** — usa o Gestor de Tarefas para isso
- **Não roteia pedidos** — isso é papel do Maestro hub
- **Não conduz entrevistas** — isso é papel do Entrevistador (Fase 4)
- **Não toma decisões de execução** — isso é papel do maestro:tarefas

---

## 2. Ritual de Abertura

### Fluxo

1. **Detectar projeto ativo** — usar a lógica de detecção do Maestro hub (seção 2.1)
2. **Ler indexes:**
   - `{projeto}/tarefas/_tarefas.md`
   - `{projeto}/entrevistas/_entrevistas.md`
3. **Ler memórias de sessão:** `{projeto}/memorias/sessoes.md` (se existir)
4. **Ler status da biblioteca:** verificar quantos templates estão preenchidos vs. vazios
5. **Apresentar dashboard:**

```markdown
Bom dia! Aqui o estado do projeto **[Nome da Empresa]**:

## Resumo
- Tarefas: [N] concluídas, [N] em andamento, [N] bloqueadas, [N] pendentes
- Entrevistas: [N] pendentes, [N] em andamento, [N] concluídas
- Biblioteca: [N] templates preenchidos de [M] total

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

## Última sessão ([data])
- **Concluído:** [lista de tarefas/entregas concluídas]
- **Parou em:** [detalhe específico — ex: "entrevista X (3 de 5 perguntas respondidas)"]
- **Observações:** [padrões ou preferências notadas]

Após apresentar o dashboard, usar `AskUserQuestion` (conforme [[protocolo-interacao]]) com opções baseadas no estado atual. Montar as opções dinamicamente:

- Se há entrevistas pendentes: incluir opção "Resolver entrevistas" com description = "Tem [N] pendente(s): [nomes]"
- Se há tarefas prontas (não bloqueadas): incluir opção "Executar tarefa" com description = "[título da tarefa mais prioritária]"
- Se há tarefas bloqueadas por entrevista: incluir opção "Desbloquear tarefas" com description = "Resolver o que trava [N] tarefa(s)"
- Sempre incluir: "Outra coisa" com description = "Pedir algo novo ou diferente"

Máximo 4 opções. Priorizar: entrevistas pendentes > tarefas desbloqueáveis > tarefas prontas > outro.
```

### Regras do dashboard

- **Priorize o que o usuário pode resolver.** Entrevistas pendentes e tarefas prontas aparecem primeiro.
- **Mostre o que pode rodar autônomo.** Tarefas pendentes sem bloqueio que poderiam ser despachadas via Agent().
- **Ofereça ações concretas.** Quando há entrevistas pendentes, ofereça acionar o Entrevistador. Quando há tarefas prontas, ofereça executar.
- **Recupere contexto.** Use a última sessão registrada pra dar continuidade. Inclua progresso detalhado (ex: "3 de 5 perguntas respondidas").
- **Seja conciso.** Não liste tarefas concluídas antigas. Só o que mudou na última sessão.
- **Seções vazias podem ser omitidas.** Se não há nada rodando em background, omita "O que está rodando". Se não há bloqueios, omita "O que está bloqueado".

### Dashboard sem tarefas

Se o projeto não tem `tarefas/_tarefas.md` ou está vazio:

```markdown
Bom dia! Projeto **[Nome da Empresa]** — sem tarefas registradas.

**Biblioteca:**
[Resumo rápido — scaffold existe? Quantos templates preenchidos de quantos total?]

Após apresentar o dashboard, usar `AskUserQuestion` (conforme [[protocolo-interacao]]):
- question: "Por onde quer começar?"
- options:
  - label: "Preencher identidade (Recomendado)", description: "Começa pela fundação: propósito, público, diferencial"
  - label: "Criar uma campanha", description: "Se já tem identidade pronta, vai direto pra ação"
  - label: "Pesquisar concorrentes", description: "Coleta dados de mercado antes de decidir"
```

### Dashboard sem projeto

Se não há projeto ativo detectado:

```markdown
Bom dia! Nenhum projeto ativo detectado.

Quer criar um novo projeto? Posso chamar o Bibliotecário pra montar a estrutura.
Ou se já tem um projeto, me diz o nome da empresa.
```

---

## 3. Ritual de Fechamento

### Fluxo

1. **Detectar o que mudou na sessão:**
   - Tarefas que mudaram de status (criadas, iniciadas, concluídas, bloqueadas, desbloqueadas)
   - Entrevistas criadas, iniciadas, concluídas ou parcialmente respondidas
   - Templates preenchidos ou modificados na biblioteca
   - Pesquisas realizadas
   - Agentes que rodaram como Agent() vs Skill()
2. **Registrar em `{projeto}/memorias/sessoes.md`:**

```markdown
### [AAAA-MM-DD]

- **Concluído:** [lista de tarefas/entregas concluídas com agente]
- **Em andamento:** [lista do que ficou em progresso, com detalhe de onde parou]
- **Entrevistas:** [N] concluídas, [N] iniciadas (parcial), [N] criadas (pendentes)
- **Pesquisas:** [N] realizadas
- **Pendências:** [N] tarefas prontas, [N] entrevistas pendentes, [N] tarefas bloqueadas
- **Modo de execução:** [quantas tarefas rodaram como Agent() vs Skill()]
- **Observações:** [padrões notados, preferências expressas, decisões tomadas]
```

3. **Apresentar resumo ao usuário:**

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

### Regras do fechamento

- **Seja factual.** Registre o que aconteceu, não o que deveria ter acontecido.
- **Registre progresso detalhado.** "Entrevista X: 3 de 5 perguntas respondidas" é melhor que "entrevista X em andamento".
- **Sugira próximos passos com justificativa.** Explique por que aquela sugestão é a melhor (ex: "desbloqueia 3 tarefas").
- **Ofereça resolver pendências antes de fechar.** Se há entrevistas pendentes curtas, pergunte se quer resolver.
- **Não force fechamento.** Se o usuário quer continuar, não insista.
- **Crie o arquivo `sessoes.md` se não existir.** Usando a estrutura de registro acima.
- **Registre o modo de execução.** Saber quantas tarefas rodaram como Agent() vs Skill() ajuda a calibrar confiança ao longo do tempo.

---

## 4. Restrições

- **Nunca crie ou atualize tarefas diretamente.** Use o Gestor de Tarefas.
- **Nunca roteia pedidos.** Isso é papel do Maestro hub.
- **Nunca bloqueie o usuário.** O ritual é opt-in. Se o usuário pedir algo direto, o Maestro segue o fluxo normal.
- **Nunca invente dados de sessões anteriores.** Se `sessoes.md` não existe, diga "primeira sessão registrada".
- **Sempre salve o registro de fechamento.** Mesmo que a sessão tenha sido curta.
