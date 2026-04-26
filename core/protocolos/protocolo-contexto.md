---
description: Protocolo compartilhado do Sistema Maestro para carregamento de contexto da Biblioteca de Marketing
tags:
  - "#maestro/protocolo"
---

# Protocolo de Contexto

> [!info] Protocolo compartilhado do sistema MAESTRO.
> Este documento é referenciado pelo Maestro e por todos os agentes que consomem contexto da Biblioteca de Marketing.

## Objetivo

Garantir que o contexto da Biblioteca de Marketing chegue aos agentes que precisam dele. O Maestro carrega o essencial (identidade de marca), cada especialista busca o complementar (produto, referências).

---

## Contexto Obrigatório (Maestro empacota)

Antes de delegar qualquer tarefa pra um agente que produz conteúdo, o Maestro verifica e lista os templates de identidade do projeto ativo:

| Template | Caminho relativo |
|----------|-----------------|
| Círculo Dourado | `biblioteca/identidade/circulo-dourado.md` |
| Posicionamento | `biblioteca/identidade/posicionamento.md` |
| Personalidade da marca | `biblioteca/identidade/personalidade-marca.md` |
| Tom de voz | `biblioteca/identidade/tom-de-voz.md` |
| Perfil do público | `biblioteca/identidade/perfil-publico.md` |

### Formato das referências

**Modo Agent():** incluir no Bloco CONTEXTO como caminhos pra leitura:

    ---CONTEXTO---
    Contexto de marca (LEIA estes arquivos antes de executar):
    - {projeto}/biblioteca/identidade/tom-de-voz.md
    - {projeto}/biblioteca/identidade/personalidade-marca.md
    - {projeto}/biblioteca/identidade/posicionamento.md
    - {projeto}/biblioteca/identidade/circulo-dourado.md
    - {projeto}/biblioteca/identidade/perfil-publico.md

    Contexto complementar (leia se relevante pra tarefa):
    - [caminhos do Mapa de Necessidades do agente]

    Entrevistas e pesquisas:
    - [caminhos se houver]

    Memória de decisões estratégicas (somente para especialistas criativos, se arquivo existe):
    - {projeto}/memorias/decisoes.md
    ---END-CONTEXTO---

**Modo Skill():** instruir o especialista:
> "Antes de executar, leia os arquivos de identidade de marca em `biblioteca/identidade/`. Especialmente tom de voz e personalidade."

---

## Aviso Persuasivo (identidade vazia)

Quando `biblioteca/identidade/` não existe ou está vazia (templates só com [PREENCHER]):

> "A identidade de marca ainda não está preenchida. Sem ela, o resultado vai sair genérico — sem tom de voz, sem personalidade, sem direção clara. É como pedir pra alguém escrever pra sua marca sem conhecer ela.
>
> Quer preencher agora? São 5-10 minutos que mudam a qualidade de tudo que vem depois."

Usar `AskUserQuestion` (conforme [[protocolo-interacao]]):
- question: "A identidade de marca ainda não foi preenchida. Quer preencher antes?"
- options:
  - label: "Preencher agora (Recomendado)", description: "5-10 minutos que mudam a qualidade de tudo que o sistema produz"
  - label: "Seguir sem identidade", description: "O resultado pode ficar genérico sem tom de voz e personalidade definidos"

Se "seguir sem": executa normalmente. Registra no report que contexto de marca não estava disponível.
Se "preencher agora": acionar o fluxo de preenchimento da biblioteca (identidade primeiro).

---

## Contexto Complementar (especialista busca)

Cada especialista tem um **Mapa de Necessidades** definido na seção "Contexto e Biblioteca" da sua skill. O mapa lista:

- **Templates obrigatórios** — ler antes de executar. Se não existe, perguntar ao usuário.
- **Templates complementares** — ler se existir. Melhora qualidade mas não bloqueia.

No modo Agent(), o Maestro identifica os templates do mapa e inclui os caminhos no Bloco CONTEXTO. No modo Skill(), o especialista lê por conta própria.

---

## Dependências nos Templates

Cada template da biblioteca tem um campo `depende-de` no frontmatter YAML:

```yaml
depende-de:
  - identidade/posicionamento
  - identidade/perfil-publico
```

### Regras

1. **Não obrigatório** — indica contexto ideal, não bloqueia preenchimento
2. **Caminhos relativos à biblioteca** — `identidade/tom-de-voz` resolve pra `biblioteca/identidade/tom-de-voz.md`
3. **Agente lê frontmatter primeiro** — antes de preencher, vê `depende-de` e carrega as dependências que existirem
4. **Se dependência não preenchida** — seguir sem, mas anotar como lacuna

---

## Solicitação de Material Adicional

Em qualquer momento, o especialista pode:
1. **Perguntar ao usuário** — "Qual o tom de voz da marca?"
2. **Pedir documentos** — "Você tem manual de marca? Coloca na pasta `referencias/` que eu leio."
3. **No modo Agent():** reportar NEEDS_DATA ou NEEDS_CONTEXT

O sistema nunca fica travado.

---

## Contexto para o Especialista no modo "Decompor plano" (Fluxo de Plano v2 — Grupo B)

O Maestro anexa no bloco CONTEXTO do despacho do especialista-dono em modo decompor:

### Padrão pra todos os 6 especialistas (Estrategista, Copywriter, Marca, Mídias Sociais, Performance, Pesquisador)

```
Contexto de identidade (se existe):
- {projeto}/_identidade.md

Memória de decisões estratégicas (se existe):
- {projeto}/memorias/decisoes.md

Briefing original do usuário:
[bloco de texto com o pedido literal capturado no brainstorm da Fase 1]

Tags de domínio sugeridas pelo Maestro:
- produto/[slug se aplicável]
- tema/[slug do contexto]
```

### Extensões por especialista-dono

| Especialista | Adicionais ao CONTEXTO |
|---|---|
| Estrategista | Produto referenciado (se citado e existe), pesquisas recentes do projeto (se existem), escada-de-valor existente (se existe) |
| Copywriter | Produto referenciado (se citado), posicionamento do produto (se existe), ângulos prévios usados em campanhas anteriores (se existem) |
| Marca | Plataforma de marca atual (se existe), naming history (se existe) |
| Mídias Sociais | Calendário social vigente — 3 últimos meses (se existe), perfis de plataforma usados (se existem) |
| Performance | Histórico de campanhas pagas (se existem), pixel/analytics setup (se existe) |
| Pesquisador | Pesquisas anteriores do mesmo tema (se existem) |

### Modo de invocação

`MODO: decompor-plano` no bloco INSTRUÇÃO. Especialista identifica pelo modo qual fluxo seguir (decomposição vs entrega vs rascunho).

### Iteração (CK1 — Ajustar)

Quando o usuário pede ajuste no CK1, o Maestro re-despacha o mesmo especialista com:
- Bloco CONTEXTO idêntico (prompt cache hit reduz custo ~80%).
- Bloco `AJUSTE PEDIDO:` com texto livre do usuário.
- Última versão do `RESUMO-PRO-PLAN-MODE` pra contexto.

Cap de 5 iterações no loop (decisão do hub).

---

## Contexto para o Bibliotecário no Fluxo FECHAR ARTEFATO

O Maestro anexa sempre no bloco CONTEXTO do despacho do Bibliotecário pra fechar artefato:

```
Catálogos de tags (leia antes de validar):
- plugin/core/templates/catalogo-tags.md
- ~/.maestro/templates/catalogo-tags.md   (se existe; senão trate como user vazio)
```

Em **re-despacho** após o Maestro resolver tags novas via `AskUserQuestion` (Fluxo 5.12 do hub), o CONTEXTO ganha também:

```
Decisões aplicadas pelo Maestro:
tags-decisoes:
  <tag>: {acao: "adicionar" | "trocar" | "descartar", alvo: "<tag-destino-se-troca>"}
```

Bibliotecário usa `tags-decisoes` pra editar o artefato (trocar/descartar tags) antes de revalidar contra o catálogo já atualizado (o Maestro escreveu no catálogo user antes do re-despacho).

---

## Checklist Rápido

Antes de despachar um especialista:

- [ ] Identidade de marca existe e está preenchida? → Incluir caminhos no CONTEXTO
- [ ] Identidade vazia? → Aviso persuasivo, seguir se usuário quiser
- [ ] Tarefa envolve produto específico? → Incluir dossiê do produto no CONTEXTO
- [ ] Agente tem Mapa de Necessidades? → Incluir templates complementares
- [ ] Especialista criativo (`estrategista`, `marca`, `copywriter`, `midias-sociais`, `performance`)? → Incluir `{projeto}/memorias/decisoes.md` no CONTEXTO (se arquivo existe). Vale tanto no despacho do especialista quanto no despacho do Revisor.
- [ ] Modo Agent()? → Caminhos no Bloco CONTEXTO
- [ ] Modo Skill()? → Instruir leitura de biblioteca/identidade/
- [ ] Despachando Bibliotecário pra fechar artefato? → Incluir os 2 catálogos de tags no CONTEXTO (core + user)
- [ ] Despachando especialista no modo "Decompor plano" (Fase 2 do Fluxo de Plano v2)? → Incluir CONTEXTO padrão + extensões do especialista-dono (ver seção dedicada acima)
