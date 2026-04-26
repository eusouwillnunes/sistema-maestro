# Checklists deste projeto

Pasta opcional. Adicione critérios específicos do cliente/time aqui.

## Como funciona

Quando o QA valida uma entrega, ele soma 3 níveis:
1. **Padrão geral do Maestro** (sempre, vem do plugin)
2. **Sua preferência pessoal** (em `~/.maestro/checklists/`, opcional)
3. **Critério deste projeto** (esta pasta, opcional)

Os 3 níveis são aditivos — somam, não substituem.

## Exemplos

- `peca-email.md` — adicione critérios específicos pra emails deste projeto
  ```
  - [ ] Tom formal (sem gírias)
  - [ ] Assinatura inclui CNPJ
  ```
- `peca-headline.md` — critérios específicos pra headlines
- `delta-copy.md` — critérios pra qualquer entrega de copy neste projeto

## Customização

Os arquivos seguem mesmo formato dos checklists do Maestro (lista de itens com `- [ ]`).
Quando o QA reprovar um item desta pasta, vai citar "Critério deste projeto" no relatório de falha.
