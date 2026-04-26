# Fluxo de Rascunho

> Aplica: [[protocolo-timestamp]], [[protocolo-tags-rascunho]]

> [!info] **Path resolution.** Toda escrita e Glob em pasta de vault usa `{projeto}/` resolvido pelo Maestro (via `protocolo-ativacao.md` Sub-fluxo 1). Nunca CWD direto nem path relativo.

Sub-skill lida pelo Maestro via `Read` quando o classificador retorna `tipo=Rascunho`.

Rascunho = artefato rápido sem validação. Sai em `rascunhos/` fora do grafo principal. Não passa por QA nem Revisor. Pode ser promovido pra Entrega depois via `/promover`.

## TodoWrite obrigatório (3 itens fixos)

1. `Criar arquivo em rascunhos/ com frontmatter mínimo`
2. `Despachar [especialista] sem validação`
3. `Salvar conteúdo + validar tags + sinalizar prazo de expiração`

## Passo a passo

### Item 1 — Criar arquivo em rascunhos/

1. Ler timestamp atual via `Bash date +"%Y-%m-%d-%H%M"` (nome de arquivo), `date +"%Y-%m-%d"` (campo `data`), `date +"%H:%M"` (campo `hora`), `date -d "+30 days" +"%Y-%m-%d"` (campo `expira-em`). **Nunca chutar** — ver `protocolo-timestamp`.
2. Gerar nome do arquivo com o timestamp lido: `<YYYY-MM-DD-HHMM>-slug.md` (slug = 3-5 palavras do pedido).
3. Escrever em `rascunhos/` (criar pasta se não existe).
4. Frontmatter (preencher com valores lidos no passo 1). `tags-dominio` fica vazio; será preenchido no Item 3 a partir do bloco `---TAGS-RASCUNHO---` retornado pelo especialista:
   ```yaml
   ---
   tipo: rascunho
   data: <YYYY-MM-DD>
   hora: <HH:MM>
   origem-pedido: [texto do pedido do usuário]
   expira-em: <YYYY-MM-DD>  # hoje + 30 dias
   agente: [nome do especialista]
   status: rascunho
   tags-dominio: []
   tags:
     - "#maestro/rascunho"
   ---
   ```
5. Marcar item 1 `completed`.

### Item 2 — Despachar especialista sem validação

1. Bloco CONTEXTO reduzido: só identidade de marca + produto (quando relevante). Sem carregamento de templates complexos. **O catálogo de tags NÃO é anexado ao CONTEXTO** — o especialista lê via Read pelo caminho literal que já conhece da sua seção "Tags de Domínio" (mesma mecânica da entrega).
2. Instrução literal adicional no despacho:
   > "Modo rascunho. Aplique `[[protocolo-tags-rascunho]]`: matriz relaxada (`tema/*` obrigatório ≥1; `produto/*` opcional) e bloco de retorno `---TAGS-RASCUNHO---` / `---END-TAGS-RASCUNHO---` no final da resposta. Sem `---REPORT---` — contrato leve de rascunho."
3. Despachar via `Agent()` com nota "modo rascunho — sem validação posterior".
4. Especialista entrega conteúdo + bloco `---TAGS-RASCUNHO---` ao final.
5. Marcar item 2 `completed`.

### Item 3 — Salvar + validar tags + sinalizar expiração

1. Escrever o conteúdo do especialista no arquivo criado em Item 1 (tudo que vem antes do bloco `---TAGS-RASCUNHO---`).
2. **Parse do bloco `---TAGS-RASCUNHO---`:**
   - Extrair linhas entre `---TAGS-RASCUNHO---` e `---END-TAGS-RASCUNHO---`.
   - Parser tolerante: case-insensitive no nome do delimitador; aceita `-`, `*` ou espaço como bullet; tolera whitespace extra.
   - Se bloco ausente ou vazio → pular pro passo 5 com `tags-dominio: []` e adicionar aviso "especialista não sugeriu tags" no output final.
3. **Validação contra catálogo (grep local, sem round-trip):**
   - Ler `plugin/core/templates/catalogo-tags.md` (core) e `~/.maestro/templates/catalogo-tags.md` (user, se existe) via Read.
   - Extrair tags válidas de cada seção `## {dim}/` (formato `` `{dim}/{valor}` `` em bullets), merge aditivo core+user (mesma mecânica do Bibliotecário em FECHAR ARTEFATO).
   - Pra cada tag retornada pelo especialista, verificar se existe no catálogo merged:
     - Qualquer tag `produto/*` é **sempre aceita** como válida em rascunho (contrato relaxado — frontmatter do rascunho não tem campo `produto:` pra cruzar). Validação estrita de `produto/*` fica pro `/promover`, onde o especialista preenche tags da entrega do zero e o Bibliotecário valida contra o cadastro formal em `biblioteca/produtos/`.
     - Todas as outras precisam bater literalmente.
4. **Escrever no frontmatter** (contrato relaxado — aceita mesmo tags inválidas):
   - `tags-dominio:` recebe a lista completa (válidas + inválidas).
   - `tags:` mantém `#maestro/rascunho` e adiciona cada valor de `tags-dominio` como espelho.
   - Acumular tags inválidas numa lista local pra mensagem de aviso.
5. Conferir que `expira-em` é hoje + 30 dias (recalcular se tempo passou entre itens).
6. Marcar item 3 `completed`.
7. **Apresentar ao usuário:** link pro rascunho + aviso de expiração + (condicional) aviso de tags:
   - Se houve tag inválida: "Especialista sugeriu tag(s) fora do catálogo: `<tag>`. Foi salva como está (contrato relaxado). Pra tornar válida, adicione em `~/.maestro/templates/catalogo-tags.md`, ou resolva ao promover via `/promover`."
   - Se bloco ausente: "Rascunho salvo sem tags de domínio — especialista não sugeriu. Edite manualmente se quiser que apareça nos painéis por tema."
   - Aviso padrão sempre: "rascunho expira em 30 dias; pra salvar formal use `/promover [[slug]]`".

## Limites obrigatórios

### Máximo de 20 rascunhos simultâneos

Antes do Item 1, contar rascunhos abertos em `rascunhos/` (excluindo pasta `arquivados/`).

- **Se <20:** prosseguir normalmente.
- **Se =20:** abortar criação e abrir `AskUserQuestion`: "Projeto tem 20 rascunhos abertos (limite). Precisa promover, arquivar ou apagar 1 antes de criar novo. Qual você escolhe limpar?". Listar os 5 rascunhos mais antigos. Usuário escolhe ação → Maestro aplica → só então cria o novo.
- **Sem exceção:** instrução permissiva do usuário ("é urgente, deixa") não remove o bloqueio. `AskUserQuestion` é obrigatório.

### Expiração com decisão forçada

No `/ola-maestro`, rascunhos com `expira-em` vencida são listados com `AskUserQuestion`: "Rascunho [[x]] venceu em YYYY-MM-DD. Promover, arquivar ou apagar?"

- **Promover:** dispara `/promover [[x]]`.
- **Arquivar:** move pra `rascunhos/arquivados/`, atualiza `status: arquivado`.
- **Apagar:** remove arquivo.

Não pode ignorar — usuário precisa decidir.

## Modo exploratório (quando veio de NEEDS_DATA)

Variante do Rascunho disparada quando o usuário escolhe "Rascunho exploratório com suposições declaradas" na 4ª opção do `AskUserQuestion` do `fluxo-needs.md` (NEEDS_DATA). A transição de estado (cancelar tarefa da Entrega, resetar TodoWrite, capturar `dependencia-ausente`) é executada pelo `fluxo-needs.md` antes do handoff — aqui assume-se que já rodou.

### Diferenças vs. rascunho normal

**1. Frontmatter:**

```yaml
status: exploratorio   # (em vez de `status: rascunho`)
```

**2. Despacho (Item 2) — instrução adicional ao especialista:**

> "Modo exploratório. Você não tem dado suficiente sobre **[dependencia-ausente — valor capturado do NEEDS_DATA pelo fluxo-needs]**. Declare suas suposições sobre esse ponto como bullets no topo da resposta, numa seção `## Suposições declaradas`, antes do conteúdo principal. Seja explícito — o usuário vai revisar antes de promover."

O bloco `---TAGS-RASCUNHO---` do contrato de rascunho continua obrigatório (mesma mecânica do rascunho normal — ver `protocolo-tags-rascunho`).

**3. Escrita no arquivo (Item 3):**

- O bloco `## Suposições declaradas` do especialista **é** a primeira seção do corpo do rascunho, antes do conteúdo principal.
- Tudo o mais segue o Item 3 normal (parse de tags, validação contra catálogo, escrita de `tags-dominio` + `tags`, aviso de expiração).

### Herda do rascunho normal

Pasta `rascunhos/`, expiração 30 dias, limite 20 simultâneos, contrato relaxado de tags, painel Dataview `_rascunhos-index.md` (exploratórios aparecem em seção separada por `status: exploratorio`).

## Regras absolutas

1. Rascunho NUNCA passa por QA ou Revisor.
2. Rascunho NUNCA fica nos indexes principais do vault (fora do grafo).
3. Limite de 20 simultâneos é inviolável — sem override.
4. Expiração dispara `AskUserQuestion` obrigatório — usuário não pode deixar rascunho vencido indefinidamente.
