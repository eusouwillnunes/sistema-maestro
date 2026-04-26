# Checklists do Sistema Maestro

Pasta com checklists do QA. Modelo `core + delta + tipo + peca` em 3 níveis aditivos.

## Estrutura

- `core.md` — itens universais (toda entrega passa por estes)
- `delta-{categoria}.md` — itens específicos por categoria do agente (copy, estrategia, midias, performance, pesquisa, biblioteca, identidade, revisao, geral)
- `tipo-{tipo}.md` — itens operacionais por tipo de artefato (funil, lancamento, pesquisa, analise-performance, campanha, escada-de-valor, lead-magnet, entrega-generica)
- `peca-{peca}.md` — itens operacionais por peça (headline, email, vsl, post, carrossel, reels, story, copy-longa, sequencia-email, pagina-de-vendas)

## Quando cada um é carregado

- **Gerente** carrega `core` + `delta-{categoria}` + `tipo-{tipo}` na criação da tarefa (montagem em paralelo)
- **QA** completa em runtime com `peca-{x}` quando especialista declarou `peca/{x}` em `tags-dominio` do artefato

## 3 níveis aditivos

1. **Core** (este diretório) — sempre carregado
2. **User** (`~/.maestro/checklists/`) — preferências cross-projeto, opcional
3. **Projeto** (`{projeto}/maestro/checklists/`) — critérios cliente/time, opcional

Os 3 níveis SOMAM. Item idêntico (após trim) em níveis diferentes vira 1 item (dedup).

## Customizar

Pra adicionar critério próprio em qualquer arquivo, criar arquivo de mesmo nome no nível user ou projeto:

```
~/.maestro/checklists/peca-headline.md   # adiciona itens ao headline core
{projeto}/maestro/checklists/peca-email.md  # adiciona itens ao email do projeto
```

Formato idêntico (lista de `- [ ] item`). Maestro dedup automático.
