---
name: desligar-maestro
description: >
  Desativa o Sistema Maestro no projeto atual. Preserva todos os dados
  (memórias, biblioteca, config, tarefas) para reativação posterior.
---

## Fluxo

### 1. Verificar se o Maestro está ativo

Tente ler `maestro/config.md` no diretório de trabalho atual.

**Se `maestro/config.md` não existe:**
- Informar: "O Sistema Maestro nunca foi ativado neste projeto. Nada a desligar."
- Encerrar.

**Se `maestro-ativo: false`:**
- Informar: "O Sistema Maestro já está desligado neste projeto."
- Encerrar.

**Se `maestro-ativo: true`:**
- Prosseguir para o passo 2.

### 2. Desativar o sistema

Alterar `maestro/config.md` — setar `maestro-ativo: false`.

### 3. Confirmar desativação

Informar: "Sistema Maestro desligado neste projeto. Seus dados foram preservados. Para reativar, digite /maestro."
