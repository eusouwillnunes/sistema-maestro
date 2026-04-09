---
name: maestro-off
description: >
  Desativa o Sistema Maestro no projeto atual. O Claude volta a
  funcionar normalmente sem roteamento automático.
---

## Fluxo

### 1. Desativar o sistema

Alterar `user/config.md` — setar `maestro-ativo: false`.

### 2. Confirmar desativação

Informar: "Sistema Maestro desativado. Funcionando como Claude padrão. As memórias e configurações foram preservadas — use `/maestro-on` para reativar."
