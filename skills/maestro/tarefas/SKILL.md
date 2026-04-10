---
name: maestro:tarefas
description: >
  Sub-skill estratégica do Maestro para gestão de tarefas. Analisa pedidos
  e decompõe em tarefas com dependências. Consulta o estado atual (_tarefas.md)
  antes de qualquer despacho. Decide o que pode ser executado agora vs. o que
  está bloqueado. Detecta tarefas desbloqueadas e propõe planos de execução.
---

# Maestro: Gestão de Tarefas

## 1. Escopo

Esta sub-skill é consultada pelo Maestro hub quando:

- O pedido do usuário envolve trabalho que pode ser decomposto em tarefas
- É necessário verificar o estado de tarefas antes de despachar
- Uma tarefa foi concluída e o Maestro precisa saber o que desbloqueou
- O usuário quer saber o estado das tarefas ou gerenciar tarefas diretamente

### O que esta sub-skill NÃO faz

- **Não faz CRUD no vault** — delega pro Gestor de Tarefas
- **Não executa tarefas** — delega pros agentes especialistas
- **Não conduz entrevistas** — delega pro Entrevistador (Fase 4)
- **Não apresenta dashboard** — delega pro maestro:sessao

---

## 2. Decomposição de Pedidos

Quando o Maestro recebe um pedido que envolve múltiplas etapas, esta sub-skill analisa e decompõe.

### 2.1 Análise do pedido

1. **Identificar o escopo:** o que o usuário quer como resultado final?
2. **Mapear componentes:** quais templates, pesquisas ou conteúdos são necessários?
3. **Identificar agentes:** qual agente é responsável por cada componente?
4. **Mapear dependências:** qual componente depende de qual?

### 2.2 Cadeia de dependências padrão

Baseada na hierarquia da Biblioteca de Marketing (ver `maestro:biblioteca`, seção 3):

```
Nível 0: Scaffold da biblioteca (Bibliotecário)
  ↓
Nível 1: Identidade (Marca) — fundação de tudo
  ↓
Nível 2: Produto (Estrategista), Escada de Valor, Conteúdo Social (Mídias Sociais)
  ↓
Nível 3: Lead Magnet, Funil (Estrategista), Lançamento (Estrategista), Campanha (Copywriter)
```

Quando o pedido cruza níveis, tarefas de nível inferior são bloqueadas pelas de nível superior.

### 2.3 Regras de decomposição

- **Uma tarefa = uma entrega atômica.** Cada tarefa produz um template preenchido, uma pesquisa ou um conteúdo específico.
- **Granularidade por template, não por agente.** "Preencher identidade" vira 6-8 tarefas (uma por template de camada 1), não 1 tarefa genérica.
- **Grupo lógico.** Tarefas do mesmo pedido compartilham o campo `grupo` (ex: `identidade-completa`, `campanha-produto-x`).
- **Prioridade derivada.** Alta = bloqueador de outras tarefas. Média = padrão. Baixa = enriquecimento (camada 3).

### 2.4 Fluxo de decomposição

1. Analisar pedido do usuário
2. Consultar `{projeto}/tarefas/_tarefas.md` — verificar se já existem tarefas relacionadas
3. Se já existem tarefas pro mesmo grupo → não duplicar, mostrar estado atual
4. Se não existem → montar lista de tarefas com dependências
5. Apresentar plano ao usuário:

```markdown
Para **[pedido]**, preciso criar estas tarefas:

**Grupo: [nome-do-grupo]**

| # | Tarefa | Agente | Depende de | Prioridade |
|---|--------|--------|------------|------------|
| 1 | Preencher Círculo Dourado | Marca | — | Alta |
| 2 | Preencher Posicionamento | Marca | #1 | Alta |
| 3 | Preencher Perfil do Público | Marca | — | Alta |
| 4 | Preencher Personalidade | Marca | #1, #3 | Média |

Posso criar essas tarefas e começar a executar?
```

6. Após aprovação do usuário → acionar Gestor de Tarefas (via Agent/Haiku) para criar cada tarefa no vault
7. Retornar ao Maestro a lista de tarefas prontas pra executar (pendentes, sem bloqueio)

---

## 3. Consulta de Estado

Antes de qualquer despacho de agente, o Maestro consulta esta sub-skill para verificar o estado.

### 3.1 Verificação pré-despacho

1. Ler `{projeto}/tarefas/_tarefas.md`
2. Verificar se existe tarefa para o que o Maestro quer despachar
3. Se existe e está `pendente` → marcar como `em-andamento` via Gestor e prosseguir
4. Se existe e está `bloqueada` → identificar bloqueadores e reportar ao Maestro
5. Se existe e está `em-andamento` → avisar que já está em execução
6. Se existe e está `concluida` → avisar que já foi feita
7. Se não existe → permitir despacho direto (sem gestão formal de tarefa para pedidos simples/avulsos)

### 3.2 Detecção de desbloqueio

Após conclusão de uma tarefa ou entrevista:

1. Ler `_tarefas.md` atualizado (já feito pelo Gestor de Tarefas no fluxo ATUALIZAR)
2. Identificar tarefas que mudaram de `bloqueada` para `pendente`
3. Reportar ao Maestro:

```markdown
Tarefas desbloqueadas após conclusão de **[tarefa/entrevista]**:

- **[título 1]** (agente: [agente]) — pronta pra executar
- **[título 2]** (agente: [agente]) — pronta pra executar

Quer que eu execute agora?
```

---

## 4. Tratamento de NEEDS_DATA

Quando um agente reporta `NEEDS_DATA` ou `INSUFFICIENT_DATA`:

1. **Extrair dados do report:**
   - Lista de dados faltantes, tipo (entrevista/pesquisa), perguntas sugeridas
2. **Criar entrevistas e/ou tarefas de pesquisa** via Gestor de Tarefas:
   - Para cada dado tipo `entrevista` → criar documento de entrevista + vincular à tarefa
   - Para cada dado tipo `pesquisa` → criar tarefa de pesquisa para o Pesquisador
3. **Bloquear a tarefa original** (Gestor atualiza o campo `bloqueada-por`)
4. **Reportar ao Maestro** o diagnóstico:

```markdown
O agente de **[nome]** precisa de dados adicionais:

**Entrevistas necessárias:**
- [título] — [objetivo] (prioridade: [prioridade])

**Pesquisas necessárias:**
- [título] — [objetivo] (prioridade: [prioridade])

A tarefa **[nome]** fica bloqueada até esses dados serem coletados.
Quer resolver agora ou deixar na fila?
```

5. **Se "agora":** Maestro despacha pesquisas via Agent() e conduz entrevistas via Skill() (fallback Fase 1 — o Entrevistador dedicado vem na Fase 4)
6. **Se "depois":** Documentos ficam pendentes no vault. O Maestro segue com outras tarefas do grupo que não dependem.

---

## 5. Pedidos sem decomposição

Nem todo pedido do usuário precisa de gestão formal de tarefas. Regra:

- **Pedido simples** (1 agente, 1 entrega, sem dependências): Maestro despacha direto, sem criar tarefa no vault.
- **Pedido composto** (múltiplos agentes, múltiplas entregas, ou dependências): Maestro consulta esta sub-skill para decompor.
- **Pedido de grupo** ("preenche a identidade", "monta a campanha"): Sempre decompõe.

### Heurística

| Sinal | Ação |
|-------|------|
| "Cria uma headline" | Despacho direto — 1 agente, 1 entrega |
| "Preenche o círculo dourado" | Despacho direto — 1 agente, 1 template |
| "Preenche a identidade" | Decompor — 6+ templates, dependências |
| "Faz tudo" / "Monta o projeto completo" | Decompor — múltiplos agentes, múltiplos níveis |
| "Cria uma campanha pro produto X" | Decompor — pesquisa + copy + estratégia + mídia |

---

## 6. Restrições

- **Nunca crie documentos no vault diretamente.** Sempre via Gestor de Tarefas.
- **Nunca execute tarefas.** Você decompõe e planeja. A execução é do Maestro com os agentes.
- **Nunca duplique tarefas.** Sempre consultar `_tarefas.md` antes de criar.
- **Nunca force decomposição em pedidos simples.** Só decompõe quando há múltiplas etapas ou dependências.
- **Sempre apresente o plano ao usuário antes de criar tarefas.** Aprovação antes da criação.
