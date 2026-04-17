---
name: maestro-debug
description: >
  Liga ou desliga o modo debug conversacional do Sistema Maestro. Com debug
  ligado, as respostas do sistema ganham rodapé [DEBUG] listando regras,
  passos e protocolos aplicados. Não afeta documentos produzidos.
---

> [!important] Antes de executar, verifique se o Sistema Maestro está ativo neste projeto seguindo o `core/protocolos/protocolo-ativacao.md`.

## 1. Detecção de Argumento

Ler o argumento passado ao slash command.

- `on`, `ligar`, `true`, `ativar` → fluxo de ativação (seção 2)
- `off`, `desligar`, `false`, `desativar` → fluxo de desativação (seção 3)
- vazio ou qualquer outro valor → fluxo de consulta (seção 4)

## 2. Fluxo de Ativação

1. Ler `~/.maestro/config.md`.
2. Localizar a seção `## Preferências Globais`.
3. Caso não exista a linha `modo-debug:` na seção, adicionar após o comentário placeholder:

   ```yaml
   modo-debug: true
   ```

4. Caso exista com `false`, substituir por `true` preservando indentação e comentário inline.
5. Caso já esteja com `true`, informar: "Debug já estava ligado." e encerrar.
6. Confirmar ao usuário (sem citar bastidor — segue a Restrição #12 do hub):

   > "Debug ligado. A partir da próxima resposta vou anexar o rodapé [DEBUG] com as regras, passos e protocolos aplicados."

## 3. Fluxo de Desativação

1. Ler `~/.maestro/config.md`.
2. Se a linha `modo-debug: true` existe, substituir por `modo-debug: false` preservando indentação e comentário.
3. Se a linha não existe ou já é `false`, informar: "Debug já estava desligado." e encerrar.
4. Confirmar ao usuário:

   > "Debug desligado. Volto pra conversa limpa."

## 4. Fluxo de Consulta

1. Ler `~/.maestro/config.md`.
2. Se `modo-debug: true`, informar: "Debug está **ligado**. Use `/maestro-debug off` pra desligar."
3. Se `modo-debug: false` ou linha ausente, informar: "Debug está **desligado**. Use `/maestro-debug on` pra ligar."

## Restrições

- Não altere outras seções do config.
- Não crie o config se ele não existir — nesse caso, informe: "O Sistema Maestro ainda não foi ativado neste projeto. Ative primeiro com `/maestro` pra usar o debug."
- Mensagens de confirmação seguem a Restrição #12 do hub: sem citar bastidor do sistema.
