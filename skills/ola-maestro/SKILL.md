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

1. Obter lista de arquivos em `{projeto}/memorias/sessoes/` (ver seção 3)
2. Se há arquivos, pegar o mais recente (primeiro da lista ordenada descendente)
3. Ler o frontmatter do arquivo — extrair `data`
4. Calcular a diferença em dias entre `data` e a data atual
5. Aplicar a tabela abaixo
6. Se não há arquivos novos mas há `sessoes.md` legado, extrair a data do cabeçalho mais recente (`### [AAAA-MM-DD]`) e calcular igual
7. Se não há nenhuma fonte, primeira sessão

### Tabela de comportamento

| Intervalo | Frase no topo do dashboard | Quantidade carregada | Seção "Última sessão" |
|-----------|---------------------------|----------------------|------------------------|
| Primeira sessão | "Primeira sessão registrada!" | 0 | Omitir |
| 0-2 dias | "Última sessão: hoje / ontem / anteontem" | `max(N, 1)` | Resumo enxuto (1-2 linhas, só "parou em") |
| 3-7 dias | "Faz [X] dias desde a última sessão" | `max(N, 1)` | Resumo padrão (concluído + parou em + observações) |
| > 7 dias | "Faz [X] dias desde a última sessão — resumo mais completo" | `max(N, 3)` | Resumo expandido (últimas 2-3 sessões + recap geral) |

`N` = valor de `sessoes-ao-iniciar` no `~/.maestro/config.md` (default 1).

---

## 3. Leitura de sessões

### Descoberta de arquivos

1. **Ler `~/.maestro/config.md`** — extrair valor de `sessoes-ao-iniciar`.
   - Se ausente ou inválido (não-inteiro, ou negativo diferente de zero), avisar no dashboard ("config `sessoes-ao-iniciar` inválida, usando default `1`") e usar `1`.
   - Chamar o valor final de **N**.

2. **Listar arquivos em `{projeto}/memorias/sessoes/`** — glob `*.md`, excluir `_sessoes.md`.
   - Ordenar descendente por nome (prefixo `YYYY-MM-DD-HHMM` garante ordem cronológica natural).
   - Chamar a lista de **arquivos-novos**.

3. **Verificar existência de `{projeto}/memorias/sessoes.md` legado.**
   - Se existe, chamar de **legado-existe = true**.

### Decisão de fonte

| Situação | Fonte do dashboard |
|----------|---------------------|
| `arquivos-novos` >= 3 | Só arquivos-novos |
| `arquivos-novos` 1-2 + `legado-existe` | Híbrido: arquivos-novos + últimas 2-3 entradas do legado |
| `arquivos-novos` 1-2 + não há legado | Só arquivos-novos |
| `arquivos-novos` == 0 + `legado-existe` | Só legado (parser antigo) |
| `arquivos-novos` == 0 + não há legado | Primeira sessão registrada |

### Quantas sessões carregar

Depende do intervalo adaptativo (ver seção 2):

| Intervalo | Quantidade |
|-----------|------------|
| 0-2 dias | `max(N, 1)` |
| 3-7 dias | `max(N, 1)` |
| > 7 dias | `max(N, 3)` |

### Detecção de backup de emergência

Antes de montar o dashboard, verificar se `~/.maestro/sessoes-emergencia/` existe e tem arquivos. Se sim, avisar:

> "Detectei sessão(ões) em backup de emergência: [lista]. Quer copiar pra `{projeto}/memorias/sessoes/`? [Sim / Não agora]"

Se sim, copiar e remover do backup. Se não, continuar normalmente.

---

## 4. Fluxo

1. **Detectar projeto ativo** — usar a lógica de detecção do Maestro hub (protocolo-ativacao)
2. **Ler indexes:**
   - `{projeto}/tarefas/_tarefas.md`
   - `{projeto}/entrevistas/_entrevistas.md`
3. **Executar leitura de sessões** — conforme seção 3 (Leitura de sessões):
   - Carregar config
   - Descobrir arquivos-novos via glob
   - Decidir fonte (só-novo / híbrido / só-legado / primeira-sessão)
   - Detectar backup de emergência e oferecer recuperação se houver
4. **Calcular intervalo adaptativo** — conforme seção 2
5. **Ler status da biblioteca** — verificar quantos templates estão preenchidos vs. vazios
6. **Apresentar dashboard** — conforme seção 5, usando o intervalo calculado
7. **Oferecer opções** via `AskUserQuestion` — conforme [[protocolo-interacao]]

---

## 5. Dashboard

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

## Última sessão ([data] [hora])
[Conteúdo varia conforme intervalo adaptativo — ver seção 2:]

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

## 6. Regras do dashboard

- **Priorize o que o usuário pode resolver.** Entrevistas pendentes e tarefas prontas aparecem primeiro.
- **Mostre o que pode rodar autônomo.** Tarefas pendentes sem bloqueio que poderiam ser despachadas via Agent().
- **Ofereça ações concretas.** Quando há entrevistas pendentes, ofereça acionar o Entrevistador. Quando há tarefas prontas, ofereça executar.
- **Recupere contexto.** Use o `parou-em` do frontmatter da última sessão pra dar continuidade. Se ausente, use a primeira linha da seção "Em andamento" do corpo.
- **Seja conciso.** Não liste tarefas concluídas antigas. Só o que mudou no intervalo carregado.
- **Seções vazias podem ser omitidas.** Se não há nada rodando em background, omita "O que está rodando". Se não há bloqueios, omita "O que está bloqueado".
- **Adapte o nível de detalhe ao intervalo.** Quem voltou ontem não precisa do mesmo contexto de quem sumiu por 2 semanas.
- **Use wiki-links do corpo da sessão pra popular links do dashboard.** Tarefas, planos, entrevistas listados na sessão já são `[[wiki-link]]` — basta repetir.

---

## 7. Restrições

- **Nunca crie ou atualize tarefas diretamente.** Use o Gerente de Projetos.
- **Nunca roteia pedidos.** Isso é papel do Maestro hub.
- **Nunca bloqueie o usuário.** O ritual é opt-in. Se o usuário pedir algo direto, o Maestro segue o fluxo normal.
- **Nunca invente dados de sessões anteriores.** Se `sessoes/` está vazio e `sessoes.md` legado não existe, diga "Primeira sessão registrada!".
- **Nunca modifique arquivos de sessão.** Leitura apenas. A escrita é papel do `/tchau-maestro`.
- **Nunca toque em `sessoes.md` legado.** Apenas leitura com parser antigo quando necessário.
