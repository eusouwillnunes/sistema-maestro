---
name: maestro-statusline
description: >
  Configura a barra de status do Maestro no terminal. Toggle on/off inteligente:
  se desligada liga com defaults, se ligada oferece desligar ou configurar.
---

## 1. Detecção de Estado

Ao ser acionado, verificar o estado atual:

1. Ler `user/config.md` do plugin
2. Verificar se existe a seção `## Status Line` com campo `statusline-ativo`

**Se `statusline-ativo` não existe ou é `false`:**
→ Executar o **Fluxo de Ativação** (seção 2)

**Se `statusline-ativo: true`:**
→ Perguntar: "A status line está ativa. Quer desligar ou configurar?"
- **Desligar** → Executar o **Fluxo de Desativação** (seção 3)
- **Configurar** → Executar o **Menu de Configuração** (seção 4)

---

## 2. Fluxo de Ativação

### 2.1 Ler preferências

Verificar se já existem preferências salvas em `user/config.md` (seção `## Status Line`).

**Se existem:** usar as preferências salvas (o usuário configurou antes e desligou).

**Se não existem:** usar os defaults:

```yaml
statusline-ativo: true
statusline-itens: contexto, limite-5h, limite-7d, modelo
statusline-estilo-contexto: barra
statusline-estilo-limite-5h: numero
statusline-estilo-limite-7d: numero
statusline-estilo-modelo: texto
statusline-estilo-custo: numero
statusline-faixas-contexto: 40,60,70
```

### 2.2 Gerar o script

1. Ler o template do script em `core/statusline/maestro-statusline.sh`
2. Substituir as variáveis de configuração no topo do script com os valores das preferências:
   - `ITEMS` → valor de `statusline-itens`
   - `ESTILO_CONTEXTO` → valor de `statusline-estilo-contexto`
   - `ESTILO_LIMITE_5H` → valor de `statusline-estilo-limite-5h`
   - `ESTILO_LIMITE_7D` → valor de `statusline-estilo-limite-7d`
   - `ESTILO_MODELO` → valor de `statusline-estilo-modelo`
   - `ESTILO_CUSTO` → valor de `statusline-estilo-custo`
   - `FAIXAS_CONTEXTO` → valor de `statusline-faixas-contexto`
3. Salvar o script gerado em `~/.claude/maestro-statusline.sh`
4. Tornar executável: `chmod +x ~/.claude/maestro-statusline.sh`

### 2.3 Configurar o settings.json

1. Ler `~/.claude/settings.json`
2. Adicionar (ou atualizar) a chave `statusLine`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/maestro-statusline.sh"
  }
}
```

3. Salvar o arquivo preservando as demais configurações existentes

### 2.4 Salvar estado

Atualizar `user/config.md` — setar `statusline-ativo: true` na seção `## Status Line`.
Se a seção não existe, criá-la ao final do arquivo com todos os campos de preferências.

### 2.5 Confirmar

Informar:

> "Status line ativada! Ela aparece na próxima mensagem. Para desligar ou configurar, rode `/maestro-statusline`."

---

## 3. Fluxo de Desativação

### 3.1 Remover do settings.json

1. Ler `~/.claude/settings.json`
2. Remover a chave `statusLine`
3. Salvar o arquivo preservando as demais configurações existentes

### 3.2 Atualizar estado

Atualizar `user/config.md` — setar `statusline-ativo: false`.
**Manter todas as outras preferências** (itens, estilos, faixas) — quando o usuário religar, volta com a mesma configuração.

### 3.3 Confirmar

Informar:

> "Status line desativada. Suas preferências foram mantidas — quando quiser religar, rode `/maestro-statusline`."

---

## 4. Menu de Configuração

Apresentar o estado atual:

```
Configuração da Status Line:

1. Itens visíveis: Contexto ✓, 5h ✓, 7d ✓, Modelo ✓, Custo ✗
2. Estilo por item: Contexto [barra], 5h [número], 7d [número]
3. Faixas de cor do contexto: verde até 40%, amarelo até 60%, laranja até 70%, vermelho 71%+

O que quer alterar? (número ou "pronto")
```

Ler as preferências atuais de `user/config.md` para montar o menu.

### 4.1 Opção 1 — Itens visíveis

Mostrar os 5 itens com estado atual:

```
Quais itens mostrar na barra?
[x] Contexto
[x] Limite 5h
[x] Limite 7d
[x] Modelo
[ ] Custo

Fale quais quer ligar ou desligar.
```

Aguardar resposta. Atualizar `statusline-itens` em `user/config.md`.

### 4.2 Opção 2 — Estilo por item

Mostrar os itens ativos com estilo atual:

```
Qual estilo para cada item?
- Contexto: [barra] ou [número]?
- Limite 5h: [barra] ou [número]?
- Limite 7d: [barra] ou [número]?
- Custo: [barra] ou [número]?

Fale qual item quer mudar e pra qual estilo.
```

Aguardar resposta. Atualizar `statusline-estilo-[item]` em `user/config.md`.

### 4.3 Opção 3 — Faixas de cor do contexto

```
Faixas de cor do contexto (atuais):
- Verde: 0–40%
- Amarelo: 41–60%
- Laranja: 61–70%
- Vermelho: 71%+

Informe 3 números separados por vírgula (ex: 40,60,70) ou "padrão" pra resetar.
```

Aguardar resposta.
- Se "padrão" → setar `statusline-faixas-contexto: 40,60,70`
- Se 3 números → validar que são crescentes e entre 1-99 → salvar

### 4.4 Aplicar alterações

Após qualquer mudança (ou quando o usuário disser "pronto"):

1. Salvar preferências atualizadas em `user/config.md`
2. Regenerar o script `~/.claude/maestro-statusline.sh` (mesmo fluxo da seção 2.2)
3. Informar: "Configuração atualizada! A barra já muda na próxima mensagem."

---

## 5. Tom e Estilo

- **Direto e prático** — sem jargão técnico
- **Sem persona** — é o Maestro falando
- **Frases curtas** — máximo 2-3 frases por mensagem
- **Use acentos corretos em português** — sempre
