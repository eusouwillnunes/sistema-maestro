---
name: tchau-maestro
description: >
  Encerra a sessão de trabalho no Sistema Maestro. Registra progresso
  detalhado em sessoes.md, apresenta resumo visual e sugere próximos
  passos baseados em impacto e dependências.
---

> [!important] Antes de executar, verifique se o Sistema Maestro está ativo neste projeto seguindo o `core/protocolos/protocolo-ativacao.md`.
> Aplica: [[protocolo-interacao]]

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

## 2. Fluxo

1. **Detectar o que mudou na sessão:**
   - Tarefas que mudaram de status (criadas, iniciadas, concluídas, bloqueadas, desbloqueadas)
   - Entrevistas criadas, iniciadas, concluídas ou parcialmente respondidas
   - Templates preenchidos ou modificados na biblioteca
   - Pesquisas realizadas
   - Agentes que rodaram como Agent() vs Skill()

2. **Registrar em `{projeto}/memorias/sessoes.md`** com o formato padrão da seção 3.

3. **Apresentar resumo visual ao usuário** conforme o template da seção 4.

4. **Sugerir próximos passos com justificativa** — explicar por que aquela sugestão é a melhor (ex: "desbloqueia 3 tarefas").

5. **Oferecer resolver pendências antes de fechar** — se há entrevistas pendentes curtas, perguntar se o usuário quer resolver antes de encerrar.

---

## 3. Formato do registro

Criar ou atualizar `{projeto}/memorias/sessoes.md` adicionando uma entrada no topo com este formato:

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

## 5. Regras do fechamento

- **Seja factual.** Registre o que aconteceu, não o que deveria ter acontecido.
- **Registre progresso detalhado.** "Entrevista X: 3 de 5 perguntas respondidas" é melhor que "entrevista X em andamento".
- **Sugira próximos passos com justificativa.** Explique por que aquela sugestão é a melhor (ex: "desbloqueia 3 tarefas").
- **Ofereça resolver pendências antes de fechar.** Se há entrevistas pendentes curtas, pergunte se quer resolver.
- **Não force fechamento.** Se o usuário quer continuar, não insista.
- **Crie o arquivo `sessoes.md` se não existir.** Usando a estrutura de registro da seção 3.
- **Registre o modo de execução.** Saber quantas tarefas rodaram como Agent() vs Skill() ajuda a calibrar confiança ao longo do tempo.

---

## 6. Restrições

- **Nunca crie ou atualize tarefas diretamente.** Use o Gerente de Projetos.
- **Nunca roteia pedidos.** Isso é papel do Maestro hub.
- **Nunca bloqueie o usuário.** O ritual é opt-in. Se o usuário pedir algo direto, o Maestro segue o fluxo normal.
- **Nunca invente dados de sessões anteriores.** Se `sessoes.md` não existe, diga "primeira sessão registrada".
- **Sempre salve o registro de fechamento.** Mesmo que a sessão tenha sido curta.
