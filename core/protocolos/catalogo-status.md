# Catálogo de Status

Fonte única de verdade dos valores válidos do campo `status:` no frontmatter de cada tipo. Lido pelo helper `plugin/core/helpers/patch_frontmatter.py` e pelo hook `plugin/hooks/maestro-orquestra.py`. Referenciado pelos Dataviews em documentação humana (não parseado por eles).

> [!important] Editar este arquivo é uma decisão arquitetural.
> Adicionar status novo exige PR + bump + atualização sincronizada dos Dataviews afetados. Não edite só pra "deixar passar uma exceção".

## Status canônicos universais

- `backlog` — ideia registrada, não atacar ainda
- `pendente` — pronto pra atacar, ninguém pegou
- `em-andamento` — agente executando agora
- `bloqueado` — impedido (ver `bloqueada-por:` ou `motivo-bloqueio:`)
- `em-revisao` — em ciclo QA/Revisor automático
- `reprovado` — rejeitado, precisa refazer (ver `motivo-reprovacao:`)
- `entregue` — finalizado pelo Maestro, esperando avaliação do usuário
- `concluido` — usuário aprovou (ver `pendencias-aceitas:` se houver ressalva)
- `cancelado` — abandonado de propósito

**Convenção de grafia:** minúsculas, hífens, sem acentos. `concluido` masculino sem acento como forma neutra pra labels técnicos.

## Por tipo de documento

### tipo: tarefa
- status-canonicos: pendente, em-andamento, bloqueado, em-revisao, reprovado, entregue, concluido, cancelado
- extensoes: (nenhuma)
- campos-auxiliares: bloqueada-por, motivo-bloqueio, motivo-reprovacao, pendencias-aceitas, motivo-cancelamento
# Sem categoria-criativa-vai-pra-entregue: tarefa é container genérico. A decisão sai do tipo do artefato em `resultado:` (ver D7/D8 do spec).

### tipo: plano
- status-canonicos: backlog, em-andamento, em-revisao, reprovado, entregue, concluido, cancelado
- extensoes: aprovado, aguardando-validacao
- campos-auxiliares: motivo-reprovacao, motivo-cancelamento, pendencias-aceitas
- categoria-criativa-vai-pra-entregue: true

### tipo: identidade
- status-canonicos: pendente, em-andamento, em-revisao, reprovado, entregue, concluido
- extensoes: (nenhuma)
- campos-auxiliares: motivo-reprovacao, pendencias-aceitas
- categoria-criativa-vai-pra-entregue: true

### tipo: produto
- status-canonicos: pendente, em-andamento, em-revisao, reprovado, entregue, concluido
- extensoes: (nenhuma)
- campos-auxiliares: motivo-reprovacao, pendencias-aceitas
- categoria-criativa-vai-pra-entregue: true

### tipo: pesquisa
- status-canonicos: pendente, em-andamento, concluido, cancelado
- extensoes: (nenhuma)
- campos-auxiliares: motivo-cancelamento
- categoria-criativa-vai-pra-entregue: false

### tipo: rascunho
- status-canonicos: pendente, concluido, cancelado
- extensoes: exploratorio
- campos-auxiliares: (nenhum)
- categoria-criativa-vai-pra-entregue: false

### tipo: entrevista
- status-canonicos: pendente, em-andamento, concluido, cancelado
- extensoes: (nenhuma)
- campos-auxiliares: motivo-cancelamento
- categoria-criativa-vai-pra-entregue: false

### tipo: campanha, funil, lead-magnet, lancamento, escada-de-valor, analise-performance, entrega-generica
- status-canonicos: pendente, em-andamento, em-revisao, reprovado, entregue, concluido, cancelado
- extensoes: (nenhuma)
- campos-auxiliares: motivo-reprovacao, pendencias-aceitas, motivo-cancelamento
- categoria-criativa-vai-pra-entregue: true

## Bloco canônico `choice()` pra labels visuais em Dataview

Reutilizado em painéis que listam tarefas/artefatos individualmente. Copy-paste no template:

```dataview
choice(status = "entregue", "🔄 Aguardando você",
choice(status = "concluido", "✅ Aprovado",
choice(status = "em-revisao", "🔍 Em revisão",
choice(status = "reprovado", "❌ Reprovado, refazer",
choice(status = "em-andamento", "⚙️ Em andamento",
choice(status = "bloqueado", "🚫 Bloqueado",
choice(status = "pendente", "⏳ Pendente",
choice(status = "backlog", "📋 Backlog",
choice(status = "cancelado", "❌ Cancelado", status))))))))) as Status
```

## Parser

- Cabeçalho `### tipo: X` (vírgulas separam tipos com schema compartilhado).
- Linha `- chave: valor1, valor2, ...` declara lista; `(nenhuma)` / `(nenhum)` = lista vazia.
- Linha `- chave: true|false` declara boolean.
- Ordem das linhas dentro do bloco não importa.
- Comentários `#` ignorados até o fim da linha.
- Implementação: regex simples por seção + split por vírgula. Sem dependência externa.
