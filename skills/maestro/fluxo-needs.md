# Fluxo de NEEDS_*

Sub-skill lida pelo Maestro via `Read` quando qualquer despacho de especialista retornar `NEEDS_*` no bloco de status.

Três variantes tratadas aqui:
- `NEEDS_CONTEXT` — tag nova, campo desconhecido, referência quebrada
- `NEEDS_DECISION` — decisão estratégica não resolvida (Grupo 5)
- `NEEDS_DATA` — dependência obrigatória ausente (Grupo 9)

## Comportamento unificado

Independente da variante:

1. O item do TodoWrite correspondente ao dispatch **permanece `in_progress`** — não passa pra `completed`.
2. Maestro NUNCA resolve via texto livre — sempre `AskUserQuestion`.
3. Depois da resolução, re-despacha o especialista com contexto atualizado.
4. Só marca item `completed` quando especialista voltar com `STATUS: DONE` sem mais `NEEDS_*`.

## NEEDS_CONTEXT

Casos típicos:
- Tag fora do catálogo (Grupo 6)
- Campo desconhecido no frontmatter de referência
- Wiki-link quebrado

**Ação:**

1. Ler o report do especialista identificando exatamente o que falta.
2. Abrir `AskUserQuestion` com opções concretas:
   - **Adicionar ao catálogo/referências** (Maestro escreve no arquivo de config/catálogo correspondente)
   - **Substituir por alternativa** (usuário propõe ou Maestro sugere)
   - **Descartar** (remove do artefato alvo)
3. Aplicar escolha.
4. Re-despachar especialista com o contexto resolvido.

## NEEDS_DECISION

Casos: especialista detecta ambiguidade estratégica que precisa de input humano (tom entre 2 opções, preço entre faixas, oferta A vs B).

**Ação:**

1. Ler report com a decisão formulada.
2. Abrir `AskUserQuestion` com as opções propostas pelo especialista (máximo 4).
3. Registrar escolha em `memorias/decisoes.md` (protocolo Grupo 5).
4. Re-despachar especialista passando a decisão.

## NEEDS_DATA

Casos: dependência obrigatória ausente (ex: Copywriter precisa de identidade de marca pra escrever copy).

**Ação:**

1. Ler report identificando exatamente qual dependência.
2. Abrir `AskUserQuestion` com opções:
   - **Preencher agora** (disparar Entrevistador ou fluxo de identidade)
   - **Usar material existente externo** (usuário cola/linka)
   - **Cancelar entrega e preencher primeiro** (aborta pipeline atual, cria tarefa-dependência)
   - **Rascunho exploratório com suposições declaradas** (gera saída assumindo hipóteses explícitas — vai pra `rascunhos/` com `status: exploratorio`, não entra no grafo principal, exige revisão antes de promover)
3. Aplicar escolha.
4. Se preencher no fluxo, re-despachar especialista após dependência cumprida. Se "Rascunho exploratório" → executar a sub-seção "Transição pro modo exploratório (NEEDS_DATA → Rascunho Exploratório)" logo abaixo.

### Transição pro modo exploratório (NEEDS_DATA → Rascunho Exploratório)

Disparada quando usuário escolhe a 4ª opção ("Rascunho exploratório com suposições declaradas"). Executa 4 passos **dentro deste fluxo** antes de handoff pro `fluxo-rascunho.md`:

**1. Cancelar a tarefa de Entrega em curso.** A tarefa foi criada pelo Gerente no Item 1 do `fluxo-entrega.md`. Despachar Gerente em modo cancelar-tarefa com:
- `motivo`: `redirecionado-pra-exploratorio` (valor reservado do sistema — não é texto livre)
- `data-cancelamento`: timestamp via `Bash date +"%Y-%m-%dT%H:%M:%S"` (conforme `protocolo-timestamp`)
- `concluido-por: sistema` (conforme Grupo C — cancelamento via fluxo)

A tarefa fica com `status: cancelada`, mantém rastreabilidade.

**2. Resetar TodoWrite.** O TodoWrite do `fluxo-entrega.md` tem 5 itens e está no Item 2 ou posterior. Ao entrar em modo exploratório:
- Marcar todos os itens **restantes** do TodoWrite atual como `completed` com nota "redirecionado pra modo exploratório".
- Limpar TodoWrite.
- Iniciar TodoWrite novo de 3 itens do `fluxo-rascunho.md`.

**3. Injetar contexto da dependência no despacho do rascunho.** Capturar o nome da dependência ausente do report `NEEDS_DATA` do especialista original (campo `dependencia-ausente`). Passar essa variável pro despacho da Item 2 do `fluxo-rascunho.md` no modo exploratório, que a usa na instrução adicional ao especialista (ver `fluxo-rascunho.md` seção "Modo exploratório").

**4. Handoff.** Após os 3 passos acima, Maestro lê `fluxo-rascunho.md` via Read e prossegue no modo exploratório com `dependencia-ausente` disponível. Comunicar ao usuário: "Cancelei a tarefa de entrega anterior (motivo: redirecionado-pra-exploratorio). Abrindo rascunho exploratório com suas suposições declaradas."

---

## Cap do Revisor com bridge pro feedback (Canal 3)

Quando o Revisor reprova **o mesmo padrão (mesmo id) no mesmo artefato** em rodada 2 ou 3, antes de re-despachar o especialista, o Maestro intervém:

### Rodada 2

```
AskUserQuestion(
  question="O Revisor reprovou o padrão A-XX duas vezes seguidas. Essa correção parece exagero?",
  options=[
    "Não, é texto sujo mesmo — manda corrigir de novo",
    "Sim, registrar como possível falso positivo (limiar pode estar errado)"
  ]
)
```

- "Não" → re-despacha especialista normalmente (rodada 3 vem a seguir se reprovar de novo).
- "Sim" → registra entrada em `{projeto}/memorias/feedback-revisor.md` na seção "Falsos positivos" com nota "captura via Canal 3 rodada 2"; segue re-despachando especialista (decisão de override fica pra rodada 3).

### Rodada 3 (cap)

Antes de oferecer "aprovar com pendência" (já existe abaixo), insere AUQ:

```
AskUserQuestion(
  question="O padrão A-XX reprovou 3 vezes nesse artefato. É calibragem errada (falso positivo recorrente) ou texto realmente sujo?",
  options=[
    "Texto sujo mesmo — quero re-revisar manualmente",
    "Calibragem errada — registrar 3 falsos positivos consolidados e suspender o padrão pro projeto",
    "Aprovar com pendência (continuar do jeito que está)"
  ]
)
```

- "Texto sujo" → fluxo manual de revisão pelo usuário.
- "Calibragem errada" → grava 3 entradas em `feedback-revisor.md` (rodadas 1, 2 e 3) E aplica `DESATIVAR: A-XX` em `{projeto}/maestro/escrita-natural.md` no mesmo passo, com comentário de origem:
  ```
  - DESATIVAR: A-XX
    # Origem: cap de Revisor 2026-04-XX (3 falsos positivos consolidados via Canal 3)
  ```
  Cria o arquivo `{projeto}/maestro/escrita-natural.md` se ainda não existir.
- "Aprovar com pendência" → cai no fluxo já existente abaixo.

> Esse mecanismo dispensa rodar `/maestro-revisar-memorias` pra casos recorrentes — resolve no momento que a divergência fica clara.

---

## Governança de "aprovar com pendência" (QA/Revisor 3x reprovou)

Essa opção só aparece após 3 rodadas de reprovação em QA ou Revisor (ver `fluxo-entrega.md`). Mas a contabilidade longitudinal vive aqui:

### Registro

Cada uso registrado em `memorias/pendencias-aceitas.md` com:
- Data
- Artefato
- Checklist item que reprovou
- Motivo do override (campo livre)
- Contador do projeto

### Gatilho de intervenção

Após 3 usos no mesmo projeto **sem mudança de checklist**:

1. Maestro bloqueia opção "forçar entrega com pendência" na 4a vez.
2. Abre `AskUserQuestion`:
   - **Ajustar o item do checklist** (escreve em `{projeto}/maestro/checklists/{nome}.md` — projeto-específico, aditivo ao core)
     - Se o item ajustado vem de `core.md` ou `delta-{categoria}.md`: gravar em `{projeto}/maestro/checklists/{nome-original}.md`
     - Se o item ajustado vem de `tipo-{tipo}.md` ou `peca-{peca}.md`: gravar em `{projeto}/maestro/checklists/{nome-original}.md`
     - Conteúdo: lista de `- [ ] item ajustado` espelhando formato do core, com observação no topo "ajustado via fluxo-needs em {data}"
   - **Desativar o item pra este projeto** (marca como skip)
   - **Contestar o padrão com revisão formal** (abre tarefa no backlog pra revisar Grupo 7/8)
3. Aplicar a escolha.

> **Nota sobre legado:** projetos pré-v2.17.0 com `memorias/checklists-ajustados.md` legado: arquivo fica intocado (greenfield-only). Sistema novo escreve apenas em `{projeto}/maestro/checklists/`. Usuário pode migrar manualmente se quiser.

### Feedback pro ciclo de melhoria

Seção "Pendências aceitas" em cada artefato vira input do `/maestro-revisar-memorias`:
- Padrões recorrentes detectados geram proposta automática de evolução dos checklists
- Usuário sempre decide se aceita

## Regras absolutas

1. `NEEDS_*` nunca é "ignorado com texto livre" — sempre `AskUserQuestion`.
2. Opção "aprovar com pendência" nunca aparece antes de 3 rodadas reprovadas.
3. 3 usos da opção no mesmo projeto bloqueia automaticamente — nenhum override.
4. Contador reseta se checklist do item for ajustado (escolha a/b do gatilho).
