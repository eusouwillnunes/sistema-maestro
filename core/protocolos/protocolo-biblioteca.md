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
