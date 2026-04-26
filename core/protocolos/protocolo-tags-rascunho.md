---
description: Protocolo de tags no fluxo de rascunho do Sistema Maestro
tags:
  - "#maestro/protocolo"
---

# Protocolo de Tags em Rascunho

> [!info] Protocolo compartilhado
> Aplicado por 5 especialistas criativos (Copywriter, Estrategista, Marca, Mídias Sociais, Performance) e Pesquisador quando recebem despacho em modo rascunho.

## Matriz relaxada

- **`tema/*` obrigatório** (≥1). Escolher do catálogo (`plugin/core/templates/catalogo-tags.md` + `~/.maestro/templates/catalogo-tags.md`) um tema que represente o objetivo da peça.
- **`produto/*` opcional.** Adicionar quando o pedido cita produto explicitamente ou quando o projeto tem um único produto ativo em `biblioteca/produtos/`. Quando ambíguo, omitir.
- Tag fora do catálogo é **aceita sem round-trip** — contrato relaxado do rascunho. Validação estrita (Bibliotecário + AskUserQuestion) acontece só quando o rascunho é promovido via `/promover`.

## Bloco de retorno obrigatório

Ao final da resposta (após todo o conteúdo produzido), incluir exatamente:

    ---TAGS-RASCUNHO---
    - tema/<valor>
    - produto/<valor>   # omitir esta linha se não aplicável
    ---END-TAGS-RASCUNHO---

- Delimitadores `---TAGS-RASCUNHO---` e `---END-TAGS-RASCUNHO---` são literais e exclusivos deste protocolo. Não usar variantes.
- Valores em formato YAML inline (`- tema/x`). Case-sensitive no prefixo (`tema/`, `produto/`).
- O Maestro parseia este bloco literal no Item 3 do `fluxo-rascunho` e escreve em `tags-dominio:` do frontmatter, espelhando em `tags:` junto com `#maestro/rascunho`.

## Modo rascunho não usa report

Rascunho não passa por QA ou Revisor. O despacho é leve — o especialista retorna **conteúdo livre + bloco `---TAGS-RASCUNHO---`**, sem `---REPORT---`. Isso é documentado também em `protocolo-agent.md` seção 6 (Modo Rascunho).
