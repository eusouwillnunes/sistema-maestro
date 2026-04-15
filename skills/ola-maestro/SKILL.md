---
name: ola-maestro
description: >
  Abre a sessão de trabalho no Sistema Maestro. Apresenta dashboard completo
  com estado de tarefas, entrevistas, biblioteca e memórias. Adapta o nível
  de detalhe ao intervalo desde a última sessão.
---

> [!important] Antes de executar, verifique se o Sistema Maestro está ativo neste projeto seguindo o `core/protocolos/protocolo-ativacao.md`.
> Aplica: [[protocolo-interacao]]

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

## 2. Intervalo Adaptativo

Antes de montar o dashboard, calcular quantos dias se passaram desde a última sessão registrada.

### Como calcular

1. Ler `{projeto}/memorias/sessoes.md`
2. Encontrar a data da entrada mais recente no formato `### [AAAA-MM-DD]`
3. Calcular a diferença em dias entre essa data e a data atual
4. Aplicar a tabela abaixo

### Tabela de comportamento

| Intervalo | Frase no topo do dashboard | Comportamento da seção "Última sessão" |
|-----------|---------------------------|----------------------------------------|
| Primeira sessão (sem `sessoes.md` ou arquivo vazio) | "Primeira sessão registrada!" | Omitir a seção "Última sessão" |
| 0–2 dias | "Última sessão: hoje / ontem / anteontem" | Resumo enxuto: 1–2 linhas, só "onde parou" |
| 3–7 dias | "Faz [X] dias desde a última sessão" | Resumo padrão: concluído + onde parou + observações |
| Mais de 7 dias | "Faz [X] dias desde a última sessão — aqui vai um resumo mais completo" | Resumo expandido: últimas 2–3 sessões, mudanças na biblioteca, recap do estado geral |

---

## 3. Fluxo

1. **Detectar projeto ativo** — usar a lógica de detecção do Maestro hub (protocolo-ativacao)
2. **Ler indexes:**
   - `{projeto}/tarefas/_tarefas.md`
   - `{projeto}/entrevistas/_entrevistas.md`
3. **Ler memórias de sessão:** `{projeto}/memorias/sessoes.md` (se existir)
4. **Calcular intervalo adaptativo** — conforme seção 2
5. **Ler status da biblioteca** — verificar quantos templates estão preenchidos vs. vazios
6. **Apresentar dashboard** — conforme seção 4, usando o intervalo calculado
7. **Oferecer opções** via `AskUserQuestion` — conforme [[protocolo-interacao]]

---

## 4. Dashboard

### Dashboard com tarefas

```markdown
[FRASE DO INTERVALO ADAPTATIVO — ex: "Faz 5 dias desde a última sessão"]

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
[Conteúdo varia conforme intervalo adaptativo — ver seção 2:]

[0–2 dias — resumo enxuto:]
- **Parou em:** [detalhe específico — ex: "entrevista X (3 de 5 perguntas respondidas)"]

[3–7 dias — resumo padrão:]
- **Concluído:** [lista de tarefas/entregas concluídas]
- **Parou em:** [detalhe específico]
- **Observações:** [padrões ou preferências notadas]

[Mais de 7 dias — resumo expandido: mostrar as últimas 2–3 entradas de sessoes.md]
## Últimas sessões
- **[data-1]:** [concluído, onde parou]
- **[data-2]:** [concluído, onde parou]
- **[data-3]:** [concluído, onde parou]
- **Mudanças na biblioteca desde a última sessão:** [templates preenchidos, modificados ou criados]
- **Recap geral:** [estado atual do projeto em 2–3 frases]
```

Após apresentar o dashboard, usar `AskUserQuestion` (conforme [[protocolo-interacao]]) com opções baseadas no estado atual. Montar as opções dinamicamente:

- Se há entrevistas pendentes: incluir opção "Resolver entrevistas" com description = "Tem [N] pendente(s): [nomes]"
- Se há tarefas prontas (não bloqueadas): incluir opção "Executar tarefa" com description = "[título da tarefa mais prioritária]"
- Se há tarefas bloqueadas por entrevista: incluir opção "Desbloquear tarefas" com description = "Resolver o que trava [N] tarefa(s)"
- Sempre incluir: "Outra coisa" com description = "Pedir algo novo ou diferente"

Máximo 4 opções. Priorizar: entrevistas pendentes > tarefas desbloqueáveis > tarefas prontas > outro.

### Dashboard sem tarefas

Se o projeto não tem `tarefas/_tarefas.md` ou está vazio:

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

---

## 5. Regras do dashboard

- **Priorize o que o usuário pode resolver.** Entrevistas pendentes e tarefas prontas aparecem primeiro.
- **Mostre o que pode rodar autônomo.** Tarefas pendentes sem bloqueio que poderiam ser despachadas via Agent().
- **Ofereça ações concretas.** Quando há entrevistas pendentes, ofereça acionar o Entrevistador. Quando há tarefas prontas, ofereça executar.
- **Recupere contexto.** Use a última sessão registrada pra dar continuidade. Inclua progresso detalhado (ex: "3 de 5 perguntas respondidas").
- **Seja conciso.** Não liste tarefas concluídas antigas. Só o que mudou na última sessão.
- **Seções vazias podem ser omitidas.** Se não há nada rodando em background, omita "O que está rodando". Se não há bloqueios, omita "O que está bloqueado".
- **Adapte o nível de detalhe ao intervalo.** Quem voltou ontem não precisa do mesmo contexto de quem sumiu por 2 semanas.

---

## 6. Restrições

- **Nunca crie ou atualize tarefas diretamente.** Use o Gerente de Projetos.
- **Nunca roteia pedidos.** Isso é papel do Maestro hub.
- **Nunca bloqueie o usuário.** O ritual é opt-in. Se o usuário pedir algo direto, o Maestro segue o fluxo normal.
- **Nunca invente dados de sessões anteriores.** Se `sessoes.md` não existe, diga "Primeira sessão registrada!".
