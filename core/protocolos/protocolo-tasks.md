---
description: Protocolo compartilhado para agentes usarem indicadores visuais de progresso via TaskCreate/TaskUpdate
tags:
  - "#maestro/protocolo"
---

# Protocolo de Tasks Visuais

> [!info] Protocolo compartilhado do sistema MAESTRO.
> Referenciado por todos os agentes especialistas para criar indicadores visuais de progresso durante a execução.

## Objetivo

Dar ao usuário feedback visual de progresso durante a execução de qualquer agente especialista, usando as ferramentas nativas `TaskCreate` e `TaskUpdate` do Claude Code.

---

## Coexistência com o Protocolo de Sub-tarefas

Este protocolo cobre **tasks visuais gerais** (ex: Gerente mostrando progresso ao criar um lote de tarefas: "Criar tarefa 1/8, 2/8..."). É um uso **diferente e complementar** ao Protocolo de Sub-tarefas (`protocolo-sub-tarefas.md`), que cobre as **sub-tarefas dinâmicas dos especialistas** durante a execução de uma tarefa.

Os dois usos convivem no mesmo TodoWrite da sessão sem conflito:
- Tasks visuais gerais: criadas por agentes operacionais (Gerente, Bibliotecário) pra mostrar progresso de operações em lote.
- Sub-tarefas dinâmicas: criadas pelos especialistas durante a execução, conforme o Protocolo de Sub-tarefas.

Ambos seguem a convenção de higiene ao final (marcar completed ou deleted).

---

## Regras

### 1. Sempre criar tasks

Toda execução de agente DEVE criar tasks visuais. Sem exceção, independente da complexidade da tarefa.

### 2. Quando criar

No início da execução, ANTES de qualquer outra ação:
1. Analise o trabalho que vai executar
2. Identifique as etapas reais que vai seguir
3. Crie todas as tasks de uma vez com `TaskCreate`

### 3. Quantidade

- **Mínimo:** 3 tasks
- **Máximo:** 7 tasks
- Cada task deve representar uma etapa real de trabalho — se você pensaria "agora vou fazer X" naturalmente, vira task

### 4. Nomenclatura

- **subject:** verbo no infinitivo — "Coletar contexto do negócio", "Aplicar framework de headlines"
- **activeForm:** verbo no gerúndio — "Coletando contexto do negócio", "Aplicando framework de headlines"
- Sempre preencher ambos os campos

Exemplo:
```
TaskCreate({
  subject: "Coletar contexto do negócio",
  description: "Entrevistar o usuário sobre público-alvo, produto e objetivos",
  activeForm: "Coletando contexto do negócio"
})
```

### 5. Atualização obrigatória

- Marcar como `in_progress` **ANTES** de começar a etapa
- Marcar como `completed` **LOGO APÓS** terminar a etapa
- **Nunca** avançar para a próxima etapa sem atualizar a task anterior

### 6. Tasks emergentes

Se durante a execução surgir uma etapa não prevista inicialmente, crie uma nova task com `TaskCreate` antes de executá-la.

### 7. O que NÃO é task

- Micro-passos internos (ler um arquivo, fazer uma busca) — isso é parte de uma etapa, não uma etapa em si
- Decisões internas do agente — tasks são para etapas visíveis ao usuário
