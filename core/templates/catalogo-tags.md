---
tipo: catalogo
area: tags
descricao: "Catálogo de tags de domínio permitidas no vault"
---

# Catálogo de Tags

> [!info] Como funciona
> Tags de domínio são aplicadas pelos especialistas no frontmatter dos artefatos (campo `tags-dominio`). O QA valida presença; o Bibliotecário valida legalidade contra este catálogo (core + user, merge aditivo). Tag nova dispara round-trip de aprovação via Maestro. Override aditivo em `~/.maestro/templates/catalogo-tags.md`.

## produto/

Lidas automaticamente do frontmatter `produto:` dos artefatos — não precisa declarar aqui.
Tag = `produto/<slug>` onde `<slug>` = conteúdo do wiki-link em lowercase, espaços→hífen, sem acentos.
Exemplos:
- `produto: "[[curso-x]]"` → `produto/curso-x`
- `produto: "[[Curso Completo do João]]"` → `produto/curso-completo-do-joao`

## tema/

- `tema/vendas` — peças focadas em conversão direta, oferta, CTA
- `tema/autoridade` — construção de reputação, demonstração de expertise
- `tema/nutricao` — educação, aquecimento de lista, pré-venda
- `tema/captura` — lead magnet, topo de funil, aquisição
- `tema/relacionamento` — peças de proximidade, pós-venda, retenção
- `tema/prova-social` — cases, depoimentos, resultados
- `tema/diferenciacao` — posicionamento único, contraste com concorrência

## disciplina/ (v2.12.0)

Disciplina = qual expertise/agente produziu o artefato. Renomeada de `tipo/` pra evitar choque com campo frontmatter `tipo:` (template/artefato type).

- `disciplina/copy` — peças de redação persuasiva
- `disciplina/pesquisa` — pesquisas de mercado, concorrentes, tendências
- `disciplina/estrategia` — planos, funis, ofertas, diagnósticos
- `disciplina/marca` — identidade, posicionamento, arquétipo, naming, manifesto
- `disciplina/midias-sociais` — conteúdo social (posts, reels, carrosséis)
- `disciplina/performance` — campanhas pagas, otimização, métricas

## peca/ (v2.12.0)

Peça = formato final do artefato. Permite queries tipo "todas as headlines do tema autoridade pro produto X".

- `peca/headline` — headlines avulsas ou conjuntos
- `peca/email` — emails (nutrição, vendas, lançamento)
- `peca/vsl` — video sales letters
- `peca/pagina-de-vendas` — landing pages de venda
- `peca/post` — posts de redes sociais (qualquer formato)
- `peca/carrossel` — carrosséis
- `peca/reels` — vídeos curtos verticais
- `peca/anuncio` — criativos de mídia paga
- `peca/pesquisa` — relatório de pesquisa
- `peca/funil` — documento de funil completo
- `peca/identidade` — documento de identidade de marca
- `peca/manifesto` — manifesto de marca
