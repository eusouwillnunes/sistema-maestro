# Fluxo de Refinamento

> Aplica: [[protocolo-timestamp]]

Sub-skill lida pelo Maestro via `Read` quando o classificador retorna `tipo=Refinamento`.

Refinamento = edit de artefato existente mencionado pelo usuário via wiki-link ou nome. Não cria tarefa nova. Não roda QA. Roda Revisor (travessão pode aparecer em edit).

## TodoWrite obrigatório (4 itens fixos)

1. `Ler artefato existente em [[caminho]]`
2. `Despachar [especialista] pra editar`
3. `Executar Revisor sobre a edição`
4. `Atualizar artefato + registrar histórico de refinamento`

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

### Item 4 — Atualizar artefato + histórico

1. Gravar alteração no artefato original.
2. Ler timestamp atual via `Bash date +"%Y-%m-%d %H:%M"` (ver `protocolo-timestamp` — **nunca chutar**). Adicionar ao corpo, em seção `## Histórico de refinamentos` (criar se não existir):
   - `- <YYYY-MM-DD HH:MM lido do sistema> — [descrição curta da mudança]`
3. Preservar frontmatter e `tags-dominio` originais.
4. Marcar item 4 `completed`.
5. Apresentar ao usuário: resumo da mudança + link pro artefato atualizado.

## Quando NÃO usar refinamento

- Se usuário pede "mais uma versão de X" → é Entrega nova, não refinamento
- Se artefato foi criado há mais de 90 dias e faz parte de plano concluído → Maestro pergunta via `AskUserQuestion` se é refinamento ou Entrega nova (alto risco de "refinar" virar reescrever)
- Se edição toca `tags-dominio` → vira Entrega (rascunho da decisão, não edição de conteúdo)

## Regras absolutas

1. Refinamento nunca cria tarefa nova no Gerente.
2. Refinamento nunca passa por QA (edição pequena não re-valida checklist).
3. Se tamanho da edição >50%, abortar e virar Entrega.
4. Histórico é append-only — nunca reescrever entradas anteriores.
