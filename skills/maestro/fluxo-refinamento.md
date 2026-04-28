# Fluxo de Refinamento

> Aplica: [[protocolo-timestamp]]

Sub-skill lida pelo Maestro via `Read` quando o classificador retorna `tipo=Refinamento`.

Refinamento = edit de artefato existente mencionado pelo usuário via wiki-link ou nome. Não cria tarefa nova. Não roda QA. Roda Revisor (travessão pode aparecer em edit).

## TodoWrite obrigatório (4 itens fixos)

1. `Ler artefato existente em [[caminho]]`
2. `Despachar [especialista] pra editar`
3. `Executar Revisor sobre a edição. Se reprovar, re-despachar especialista do item 2 pra aplicar correção via Edit (Maestro NUNCA Edit em corpo — ver limites-maestro.md)`
4. `Especialista anexa entrada no Histórico de refinamentos no MESMO Edit do item 2 (ou item 3 se houve ciclo). Maestro NUNCA edita corpo. Apresentar resumo ao usuário.`

## Passo a passo

### Item 1 — Ler artefato existente

1. Ler o artefato mencionado pelo usuário via `Read`.
2. Identificar: tipo do artefato, `tags-dominio`, especialista original (se documentado no frontmatter), estado atual do conteúdo.
3. Se artefato não existe ou caminho está errado → abrir `AskUserQuestion` com opções de recuperação (redigitar caminho, buscar por substring, criar novo como Entrega).
4. Marcar item 1 `completed`.

### Item 2 — Despachar especialista pra editar

1. Roteamento: por default despachar o especialista indicado pelo frontmatter (`agente`). Se ausente, inferir do tipo do artefato (copy→copywriter, pesquisa→pesquisador, etc.).
2. Bloco CONTEXTO: anexar conteúdo atual do artefato + pedido de edição do usuário + campo `modo: refinamento` (especialista deve preservar estilo/estrutura).
3. Despachar via `Agent()`.
4. Se edição substitui >50% do conteúdo, abortar refinamento e oferecer ao usuário: "Isso está virando artefato novo. Criar como Entrega com tarefa própria?" (via `AskUserQuestion`).
5. Marcar item 2 `completed`.

### Item 3 — Executar Revisor

1. Despachar Revisor com o trecho editado (não artefato inteiro, só a parte mudada).
2. Aguardar retorno.
3. Se reprovar, aplicar protocolo "Revisor reprova" (ver `fluxo-entrega.md`, regra adaptada: edit re-executado, não artefato todo).
4. Quando aprovar, marcar item 3 `completed`.

### Item 4 — Anexar histórico (especialista) + apresentar (Maestro)

1. **Especialista** — no MESMO Edit do item 2 (ou item 3 quando houve ciclo de Revisor reprovar), anexar entrada em seção `## Histórico de refinamentos` do artefato (criar se não existir). **Maestro NUNCA edita corpo do artefato** — esse passo é do especialista. Aprendizado consolidado: "concern menor → Maestro aplica direto" escala recursivamente (B-S55-47).
2. **Especialista** — usar timestamp obtido via `Bash date +"%Y-%m-%d %H:%M"` (ver `protocolo-timestamp` — **nunca chutar**). Formato da entrada:
   - `- <YYYY-MM-DD HH:MM lido do sistema> — [descrição curta da mudança]`
3. **Especialista** — preservar frontmatter e `tags-dominio` originais.
4. **Maestro** — confirmar que a edição foi feita pelo especialista, marcar item 4 `completed`.
5. **Maestro** — apresentar ao usuário: resumo da mudança + link pro artefato atualizado.

> **Por que histórico vai junto com o Edit do especialista:** evita brecha "quem grava o histórico?" — sem dono explícito, antes do fix do B-S55-47, o Maestro acabava editando o corpo. Especialista anexar no mesmo Edit elimina a fronteira ambígua.

> **Cobertura de refinamento:** refinamento NÃO passa pelo Gerente (não cria tarefa). Isso significa que o tripwire do Gerente (Fluxo 2) não cobre refinamento — defesa aqui é só texto + TodoWrite. Auditoria contínua via painel `_violacoes-maestro-index.md` cobre apenas Entrega/Plano. Pra refinamento, ler `limites-maestro.md` quando classificador detecta sinal de violação iminente é a única defesa.

## Quando NÃO usar refinamento

- Se usuário pede "mais uma versão de X" → é Entrega nova, não refinamento
- Se artefato foi criado há mais de 90 dias e faz parte de plano concluído → Maestro pergunta via `AskUserQuestion` se é refinamento ou Entrega nova (alto risco de "refinar" virar reescrever)
- Se edição toca `tags-dominio` → vira Entrega (rascunho da decisão, não edição de conteúdo)

## Regras absolutas

1. Refinamento nunca cria tarefa nova no Gerente.
2. Refinamento nunca passa por QA (edição pequena não re-valida checklist).
3. Se tamanho da edição >50%, abortar e virar Entrega.
4. Histórico é append-only — nunca reescrever entradas anteriores.
