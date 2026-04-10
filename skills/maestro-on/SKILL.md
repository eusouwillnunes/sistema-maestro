---
name: maestro-on
description: >
  Ativa o Sistema Maestro no projeto atual. Configura memórias,
  verifica estrutura e prepara o ambiente de trabalho.
---

## Fluxo

### 1. Ativar o sistema

Alterar `user/config.md` — setar `maestro-ativo: true`.

### 2. Confirmar ativação

Informar: "Sistema Maestro ativado. Todas as mensagens agora passam pelo roteamento automático."

### 3. Setup de memórias (primeira ativação no projeto)

Verificar se a estrutura de memórias existe e criar o que faltar:

**Memórias de usuário:**
- Verificar se `user/memorias/_index.md` existe no plugin
- Se não existe, informar que a estrutura precisa ser criada (pode ter sido removida)

**Memórias de projeto:**
- Verificar se `maestro/memorias/` existe no vault do projeto
- Se não existe, criar usando templates de `core/templates/_memorias-projeto-template.md`:
  - `maestro/memorias/_index.md`
  - `maestro/memorias/contexto.md`
  - `maestro/memorias/sessoes.md`
  - `maestro/memorias/decisoes.md`
  - `maestro/memorias/agentes/` (pasta vazia)

**Config do projeto:**
- Verificar se `maestro/config.md` existe no vault
- Se não existe, criar usando `core/templates/_maestro-config-template.md`
- Preencher caminhos do vault e do plugin

**CLAUDE.md do projeto:**
- Verificar se o CLAUDE.md do projeto do usuário tem seção `## Maestro`
- Se não tem, adicionar ao final:
  ```
  ## Maestro
  > Sistema Maestro ativo. Configuração e memórias: maestro/config.md
  > Memórias de usuário: [caminho do plugin]/user/memorias/
  ```

### 4. Resumo do setup

Informar ao usuário o que foi configurado:
- Quais estruturas foram criadas (se primeira vez)
- Quantas memórias existem (se já configurado antes)
- Status da Biblioteca de Marketing (existe/não existe)

### 5. Verificar onboarding

Após o setup, verificar se o onboarding foi concluído:

1. Ler `maestro/config.md` no vault do projeto
2. Verificar o campo `onboarding-completo`

**Se `onboarding-completo` não existe ou é `false`:**
- Informar: "Parece que o onboarding ainda não foi feito. Vou iniciar agora."
- Executar o fluxo de onboarding guiado (skill `[[maestro:onboarding]]`)

**Se `onboarding-completo: true`:**
- Não fazer nada — o setup já está completo
