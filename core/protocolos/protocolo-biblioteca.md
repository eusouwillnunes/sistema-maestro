---
description: Protocolo compartilhado para agentes acessarem a Biblioteca de Marketing de forma autônoma
tags:
  - "#maestro/protocolo"
---

# Protocolo de Biblioteca

> [!info] Protocolo compartilhado do sistema MAESTRO.
> Referenciado por todos os agentes especialistas que consomem contexto da Biblioteca de Marketing.
> Ver também: [[protocolo-contexto]] para as regras de carregamento de contexto de marca pelo Maestro.

## Objetivo

Permitir que cada agente especialista busque e carregue de forma autônoma os templates e documentos que precisa da Biblioteca de Marketing, sem depender do Maestro para pré-carregar contexto.

---

## Ordem de Busca

O agente busca contexto nesta ordem de prioridade. A primeira fonte encontrada prevalece.

| Prioridade | Fonte | Caminho | O que contém |
|:----------:|-------|---------|-------------|
| 1 | Biblioteca do projeto | `biblioteca/` na raiz do projeto | Dados preenchidos deste projeto (identidade, produtos, referências) |
| 2 | Biblioteca do usuário | `user/biblioteca/` (dentro do plugin Maestro) | Templates reutilizáveis criados pelo usuário |
| 3 | Templates-modelo | `core/templates/biblioteca-de-marketing/` | Templates vazios/padrão do sistema |

---

## Resolução de Caminhos

1. **Tente o caminho padrão:** `biblioteca/` na raiz do projeto onde o Maestro está ativo
2. **Se não encontrar:** leia `maestro/config.md` (ou `maestro-config.md`) do projeto e procure o campo `caminho_biblioteca`
3. **Se ainda não encontrar:** pergunte ao usuário: "Não encontrei a Biblioteca de Marketing. Onde estão seus documentos de contexto?"
4. **Lembre o caminho:** se o usuário informou um caminho diferente, sugira registrar no config pra não precisar perguntar de novo

---

## Como Carregar Contexto

### Passo 1 — Identificar necessidades

Cada agente tem seu próprio **Mapa de Necessidades** (definido na seção "Contexto e Biblioteca" da sua skill). Consulte o mapa para saber o que carregar com base no tipo de tarefa.

### Passo 1.5 — Verificar dependências do template

Se a tarefa envolve preencher um template:

1. Ler o frontmatter do template-alvo
2. Verificar o campo `depende-de` (lista de caminhos relativos à biblioteca)
3. Para cada dependência listada, ler o template correspondente em `biblioteca/`
4. Se a dependência não está preenchida (só tem [PREENCHER]), seguir sem — mas anotar como lacuna e informar ao usuário que a qualidade será melhor com essa dependência preenchida
5. Dependências preenchidas servem como contexto pra produzir com coerência

Exemplo de frontmatter com dependências:

```yaml
---
titulo: Dossiê de Produto
tipo: template
camada: 2
depende-de:
  - identidade/posicionamento
  - identidade/perfil-publico
---
```

O campo `depende-de` usa caminhos relativos à pasta `biblioteca/`. Exemplo: `identidade/posicionamento` resolve pra `biblioteca/identidade/posicionamento.md`.

### Passo 2 — Buscar na Biblioteca

Para cada documento necessário:

1. Procure na `biblioteca/` do projeto (prioridade 1)
2. Se não encontrou, procure em `user/biblioteca/` (prioridade 2)
3. Se não encontrou em nenhuma, siga sem — use seus frameworks e conhecimento próprio

> [!important] Templates são aceleradores, não dependências.
> A ausência de um template NUNCA bloqueia a execução. O agente se resolve com seus frameworks próprios.

### Passo 3 — Estrutura esperada da Biblioteca

```
biblioteca/
  identidade/          ← Círculo Dourado, posicionamento, tom de voz, etc.
  produto/
    [nome-produto]/    ← Uma pasta por produto (dossiê, oferta, prospect, etc.)
  referencia/          ← Funis, lançamentos, lead magnets, etc.
```

Para carregar identidade: leia todos os arquivos em `biblioteca/identidade/`.
Para carregar produto: identifique qual produto está envolvido na tarefa e leia `biblioteca/produto/[nome-produto]/`.
Para carregar referência: leia apenas o template relevante para o tipo de tarefa.

### Passo 4 — Combinar com contexto extra

Além da Biblioteca, considere:
- **Contexto da delegação:** informações que o Maestro passou ao delegar a tarefa
- **Contexto da conversa:** arquivos, links ou textos que o usuário forneceu diretamente

O contexto do usuário complementa a Biblioteca, não substitui.

---

## Quando Sugerir Salvar como Template

Após entregar o resultado, avalie se ele merece virar template reutilizável.

### Sugira salvar quando o resultado é:
- Um plano estruturado (lançamento, funil, campanha)
- Uma definição que será referenciada depois (oferta, público, posicionamento)
- Algo que o usuário disse que quer replicar

### NÃO sugira pra:
- Peças finais de conteúdo (um post, um email, uma headline)
- Análises pontuais (diagnóstico, relatório)

### Fluxo de sugestão

1. Avalie se o resultado é reutilizável
2. Se sim, pergunte: "Esse [tipo] pode ser salvo como template pra reutilizar em outros projetos. Quer salvar?"
3. Se o usuário aceitar:
   - Templates reutilizáveis entre projetos → salvar em `user/biblioteca/[categoria]/`
   - Dados específicos deste projeto → salvar em `biblioteca/[categoria]/` do projeto
4. Nunca sobrescreva template existente sem aprovação
5. Use nomenclatura kebab-case (ex: `lancamento-semente-black-friday.md`)
6. Se não encaixa nas categorias existentes (identidade, produto, referencia) → salvar em `custom/`

---

## Regras

1. **Autonomia total:** o agente decide o que precisa e busca sozinho. Não depende do Maestro pra contexto.
2. **Sem bloqueio:** template ausente nunca impede execução. Frameworks próprios suprem a lacuna.
3. **Aprovação obrigatória:** nenhum template novo é salvo sem ok explícito do usuário.
4. **Separação core/user:** templates do core nunca são alterados. Templates do usuário ficam em `user/biblioteca/` ou `biblioteca/` do projeto.

---

## Cadastro formal

**Menção em identidade ≠ cadastro formal.** Mesmo que um produto, persona ou conceito apareça em algum template da Biblioteca (ex: campo "linhas de produtos" no posicionamento, ou nome de cliente no manifesto), isso NÃO substitui o cadastro formal no template específico.

Exemplo: o posicionamento pode listar 3 linhas de produto que a marca vende. Pra produzir entrega sobre uma dessas linhas (página de vendas, email, oferta), o produto precisa ter `produtos/[slug]/dossie.md` preenchido. Identidade conta o que a marca vende em termos gerais; o cadastro formal tem dados estruturados que alimentam a execução.

Especialistas que precisem de cadastro formal declaram `produto` (ou outra dependência específica) na coluna "Críticas" da sua tabela "Dependências obrigatórias por peça/entrega". Maestro abre cadastro via cascata de entrevistas conforme `fluxo-needs.md`.

**Mensagem padrão amigável (UX):** quando o Maestro precisa explicar a regra ao usuário, usa o template:

> "Você mencionou [conceito] em [arquivo da identidade] (ótimo!). Pra produzir [peça], preciso de um [template específico] dedicado: [campos principais]. Posso abrir o cadastro agora? (~[X] min)"

A frase explica o **porquê** do cadastro extra, não soa burocrática.

---

## Wikilinks em frontmatter

Todo campo de frontmatter que aponta para outro artefato do vault usa o formato `[[pasta/slug]]` com a pasta-destino do tipo do alvo. Em listas, cada item segue o mesmo formato.

**Não usar `[[slug]]` simples** — ambíguo no Obsidian quando dois arquivos compartilham slug em pastas diferentes (ex: tarefa e entrega promovida com mesmo slug).

### Exemplos canônicos

```yaml
parte-de: "[[planos/plano-x]]"           # OK — tarefa aponta pra plano
parte-de: "[[plano-x]]"                  # ERRADO — sem path

bloqueada-por:                           # OK — lista
  - "[[tarefas/tarefa-y]]"
  - "[[tarefas/tarefa-z]]"

resultado: "[[campanhas/campanha-black-friday]]"   # OK — pasta varia conforme tipo do artefato gerado
```

### Tabela canônica (8 templates × 11 campos)

| Campo | Template(s) | Pasta destino |
|-------|-------------|---------------|
| `parte-de` | `tarefa.md` | `planos/` |
| `bloqueada-por` | `tarefa.md` (lista) | `tarefas/` |
| `resultado` | `tarefa.md` | qualquer pasta (depende do tipo do artefato gerado) |
| `corrige` | `plano.md` | `planos/` |
| `correcoes` | `plano.md` (lista) | `planos/` |
| `regera` | `plano.md` | `planos/` |
| `produto` | `campanha.md`, `funil.md`, `lancamento.md`, `escada-de-valor.md` | `produtos/` |
| `produto-destino` | `lead-magnet.md` | `produtos/` |
| `tarefa-relacionada` | `entrevista.md` | `tarefas/` |
| `campanha` | `analise-performance.md` | `campanhas/` |
| `promovido-para` | (preenchido por `fluxo-entrega.md` no rascunho promovido) | qualquer pasta |
| `origem-tarefa` | (adicionado pelo especialista ao frontmatter do artefato gerado) | `tarefas/` |

**Fora desta regra:** `depende-de` em templates de identidade/produto. Já usa formato `pasta/slug` sem brackets — é referência simbólica resolvida pelo Bibliotecário, não wikilink Obsidian.

### Quando aplicar

Toda skill que escreve wikilink em frontmatter de artefato deve referenciar este protocolo via cabeçalho `Aplica:` no topo do SKILL.md (mesmo padrão de `protocolo-interacao`, `protocolo-timestamp`, etc.).

---

## Tags de Domínio

Sistema de tags transversais que permitem navegação por produto, tema e dimensões futuras. Complementa (não substitui) as tags estruturais `#maestro/*`.

### Catálogo

Duas camadas com merge aditivo:

| Prioridade | Fonte | Caminho |
|:---:|---|---|
| 1 | Usuário | `~/.maestro/templates/catalogo-tags.md` |
| 2 | Core | `plugin/core/templates/catalogo-tags.md` |

Tags válidas = união das duas fontes, deduplicado. Usuário **acrescenta**, não substitui. Tag core não pode ser removida via override.

### Formato canônico

Cada dimensão é uma seção com header `## {dim}/` (barra obrigatória no fim). Itens:

```
- `{dim}/{valor}` — {descrição opcional}
```

Parser regex (2 passadas):

- Identificar seções: `(?m)^##\s+(?P<dim>[a-z0-9][a-z0-9-]*)\/\s*$`
- Extrair tags dentro de cada seção até o próximo `##`: `` `(?P<tag>[a-z0-9][a-z0-9-]*\/[a-z0-9][a-z0-9-]*)` ``

Exceção `produto/`: o core não lista bullets — tags são derivadas do frontmatter de cada artefato via slugify.

### Campo no frontmatter

Templates de artefato aplicáveis (`funil`, `campanha`, `lancamento`, `lead-magnet`, `escada-de-valor`, `analise-performance`, `pesquisa`, `entrega-generica`) têm:

```yaml
tags-dominio:
  - produto/<slug>
  - tema/<valor>
```

**Regra de slugify pra `produto/`:** tag = `produto/<slug>`, onde `<slug>` = conteúdo do wiki-link do campo `produto:` em lowercase + espaços convertidos em hífen + sem acentos.

Exemplos:
- `produto: "[[curso-x]]"` → `produto/curso-x`
- `produto: "[[Curso Completo do João]]"` → `produto/curso-completo-do-joao`

Campo `produto:` do frontmatter continua string única (produto principal). Cruzamentos (artefato envolve 2+ produtos) moram em `tags-dominio` como `produto/*` adicionais.

### Matriz de obrigatoriedade

| Tipo | `produto/*` | `tema/*` |
|---|:---:|:---:|
| funil, campanha, lancamento, lead-magnet, escada-de-valor, analise-performance | obrigatório | obrigatório |
| pesquisa, entrega-generica | opcional | obrigatório |
| tarefa, plano, entrevista | **não se aplica** | **não se aplica** |

### Fluxo de validação

- **QA** valida **presença** (Fluxo 5.1 passo 3 do Maestro). Item binário no checklist da categoria. Reprova se ausente → tarefa de revisão.
- **Bibliotecário** valida **legalidade** (Fluxo FECHAR ARTEFATO, após aprovação humana). Parseia catálogos, verifica cada tag.
  - Tag existe no catálogo → OK.
  - Tag é `produto/<slug>` e casa com `produto:` via slugify → OK (auto-válido mesmo sem declaração).
  - Tag não bate → acumula em `tags-novas` com sugestões por prefixo.

### Round-trip de tag nova

Bibliotecário em Agent() **NÃO abre `AskUserQuestion`**. Reporta `NEEDS_CONTEXT`:

```
BLOCKER:
  motivo: "tags fora do catálogo"
  tags-novas: [<lista>]
  sugestoes: {<tag>: [<sugestões por prefixo>]}
```

Maestro recebe, abre `AskUserQuestion` (1 por tag, 3 opções: adicionar ao user / trocar por sugestão / descartar), aplica decisões (escreve em `~/.maestro/templates/catalogo-tags.md` para adições), re-despacha Bibliotecário com CONTEXTO enriquecido por `tags-decisoes: {<tag>: {acao: ..., alvo: ...}}`.

Bibliotecário na 2ª rodada aplica trocas/descartes no artefato e valida — idempotente, máximo 2 rodadas.
