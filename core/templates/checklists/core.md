# Checklist core (universal)

Aplicado em toda entrega que passa pelo QA. Itens binários sempre que possível — substituiu o "Checklist Global" antigo do `qa/SKILL.md`.

## Conteúdo do artefato

- [ ] Acentuação correta em português do Brasil (palavras como "é", "não", "próximo", "já", "também", "você", "análise", "estratégia", "conteúdo" aparecem com acento)
- [ ] ≥1 wikilink (`[[...]]`) no corpo OU no frontmatter, conectando o artefato a outro arquivo do vault
- [ ] Sem placeholders `[PREENCHER]` ou `[preencher]` no corpo
- [ ] Sem placeholders nos campos obrigatórios do frontmatter
- [ ] Hex codes de cor (ex: `#FF5733`) entre backticks no corpo (não viram tag órfã no Obsidian)

## Frontmatter

- [ ] `tipo:` declarado (não vazio)
- [ ] Se tipo é `funil`, `campanha`, `lancamento`, `lead-magnet`, `escada-de-valor` ou `analise-performance`: `produto:` declarado e preenchido
- [ ] `tags-dominio:` declarado com ≥1 valor `tema/{x}` válido do catálogo (`plugin/core/templates/catalogo-tags.md` + override user)
- [ ] Se tipo exige produto: `tags-dominio` também tem ≥1 valor `produto/{slug}` derivado do `produto:` por slugify
- [ ] Campo `tags:` espelha todos os valores de `tags-dominio` (Obsidian tag pane só renderiza hierarquia via campo nativo)
- [ ] Frontmatter `origem-tarefa:` aponta pra `[[tarefas/<slug>]]` que despachou (ou frase explícita "tarefa direta sem origem registrada" se não aplicável)

## Decisões estratégicas

- [ ] Seção `## Decisões estratégicas` existe (preenchida com tabela ou frase explícita "Nenhuma decisão estratégica canônica nesta tarefa.")
- [ ] Se a tarefa tocou ponto canônico (24 IDs no `protocolo-decisoes-estrategicas.md` seção 9): tabela tem `Ponto | Escolha | Origem` preenchidos; se escopo ≠ tarefa, também gravado em `memorias/decisoes.md`

## Cruzamento tarefa↔artefato

- [ ] Título do artefato (`titulo:`) menciona o assunto principal da tarefa (≥1 palavra-chave significativa em comum, ignorando stop words `[a, o, de, da, do, em, para, pra, com, e, ou]`)
