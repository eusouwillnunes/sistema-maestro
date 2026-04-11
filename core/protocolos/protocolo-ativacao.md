---
description: Protocolo compartilhado de verificação de ativação do Sistema Maestro no projeto atual
tags:
  - "#maestro/protocolo"
---

# Protocolo de Ativação

> [!info] Protocolo compartilhado do sistema MAESTRO.
> Referenciado por todas as skills para verificar se o Sistema Maestro está ativo no projeto antes de executar.

## Objetivo

Garantir que nenhuma skill crie estrutura ou execute ações no projeto sem que o usuário tenha ativado o Sistema Maestro explicitamente.

---

## Verificação

Antes de executar qualquer ação, siga estes passos:

### 1. Verificar existência do config

Tente ler o arquivo `maestro/config.md` no diretório de trabalho atual.

### 2. Verificar campo de ativação

Verifique o campo `maestro-ativo` no frontmatter do `maestro/config.md`.

### 3. Decidir

- **`maestro/config.md` não existe** → BLOQUEADO. Exibir mensagem de bloqueio e encerrar.
- **`maestro-ativo: false`** → BLOQUEADO. Exibir mensagem de bloqueio e encerrar.
- **`maestro-ativo: true`** → LIBERADO. Prosseguir com a execução normal da skill.

---

## Mensagem de bloqueio

Quando bloqueado, exibir exatamente:

> O Sistema Maestro não está ativo nesse projeto. Para ativar, digite o comando /maestro.

Não executar mais nada após a mensagem. Não sugerir alternativas. Não fazer perguntas.
