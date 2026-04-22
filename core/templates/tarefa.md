---
titulo: "[PREENCHER]"
tipo: tarefa
agente: "[PREENCHER]"
categoria: "[identidade|copy|estrategia|midias|performance|pesquisa|biblioteca|revisao|validacao-plano|geral]"
status: em-andamento
bloqueada-por: []
grupo: "[PREENCHER]"
prioridade: media
solicitante: "[PREENCHER]"
parte-de: ~                           # wiki-link do plano (~ em tarefa atômica)
adicionada-em: ~                      # timestamp ISO 8601 quando adicionada pós-aprovação do plano; ~ em tarefas criadas junto do plano
data-criacao: "[PREENCHER — YYYY-MM-DDTHH:MM:SS]"
data-inicio: "[PREENCHER — YYYY-MM-DDTHH:MM:SS]"
data-conclusao: ~
data-cancelamento: ~                  # timestamp ISO 8601 | ~ (preenchido só em status=cancelada)
motivo-cancelamento: ~                # enum: duplicada|obsoleta|mudanca-de-prioridade|erro|substituida|outro|cascata-automatica | ~
aguardando-decisoes: []               # lista de IDs canônicos pendentes (ex: [formato-lancamento]); vazia quando não há decisão pendente
decisoes-pendentes-report: ~          # string multi-linha com o report NEEDS_DECISION preservado; ~ quando vazio
decisoes-resolvidas: {}               # mapa de id→escolha após usuário responder; limpo após re-despacho bem-sucedido
resultado: "[[caminho-do-artefato]]"
tags:
  - "#maestro/tarefa"
---

## Descrição

[Briefing que o especialista vai ler — objetivo, contexto e critérios de sucesso]

## Sub-tarefas

[Preenchido pelo especialista no início da execução — dinâmico, específico ao pedido]

## Validações

[Fixo por categoria — carregado pelo Gerente com base na categoria, sem filtro]

## Dependências

- **Bloqueada por:** nenhuma
- **Bloqueia:** nenhuma
