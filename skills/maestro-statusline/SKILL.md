---
name: maestro-statusline
description: >
  Configura a barra de status do Maestro no terminal. Toggle on/off inteligente:
  se desligada liga com defaults, se ligada oferece desligar ou configurar.
---

> [!important] Antes de executar, verifique se o Sistema Maestro está ativo neste projeto seguindo o `core/protocolos/protocolo-ativacao.md`.

## 1. Detecção de Estado

Ao ser acionado, verificar o estado atual:

1. Ler `~/.maestro/config.md` do plugin
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

Verificar se já existem preferências salvas em `~/.maestro/config.md` (seção `## Status Line`).

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

### 2.3 Verificar workspace trust

O Claude Code bloqueia statusLine em projetos sem workspace trust aceito (mensagem visível: `statusline skipped · restart to fix`).

> [!warning] Path do projeto pode existir em multiplas formas em `~/.claude.json`
> O arquivo acumula entradas distintas pra mesma pasta conforme voce renomeia/move (ex: `C:/marketing-primum/cbi`, `C:/primum-workspace/cbi`, `G:\\Meu Drive\\...\\cbi`). O fix precisa cobrir **todas as variantes que terminam no mesmo basename do CWD atual**, nao so o path canonico.

Executar o Bash unico abaixo (faz detecao + fix + verificacao numa passada, com backup):

```bash
python - <<'PYEOF'
import re, shutil, time, os, sys
path = os.path.expanduser('~/.claude.json')
cwd = os.getcwd().replace('\\', '/')
basename = os.path.basename(cwd)

with open(path, 'rb') as f:
    content = f.read()

# Achar TODAS as entradas que terminam no basename do CWD
# Pattern: "<qualquer-path>/<basename>": { ... "hasTrustDialogAccepted": false/true ...
needle_re = re.compile(rb'"([^"]*[/\\\\]' + re.escape(basename).encode() + rb')"\s*:\s*\{', re.IGNORECASE)
matches = list(needle_re.finditer(content))

if not matches:
    print(f"NENHUMA entrada com basename '{basename}' encontrada em .claude.json")
    sys.exit(0)

print(f"Encontradas {len(matches)} entrada(s) com basename '{basename}':")
to_fix = []
for m in matches:
    entry_path = m.group(1).decode('utf-8', errors='replace')
    # Ver o valor de hasTrustDialogAccepted nos proximos 1500 bytes
    chunk = content[m.end():m.end()+1500]
    tm = re.search(rb'"hasTrustDialogAccepted":\s*(true|false)', chunk)
    if tm:
        val = tm.group(1).decode()
        print(f"  - {entry_path[-60:]} -> trust={val}")
        if val == 'false':
            to_fix.append(m.end() + tm.start(1))
    else:
        print(f"  - {entry_path[-60:]} -> trust=AUSENTE (pular)")

if not to_fix:
    print("\nTodas ja em trust=true. Nada a fazer.")
    sys.exit(0)

# Backup antes do write
backup = f"{path}.bak-{int(time.time())}"
shutil.copy(path, backup)
print(f"\nBackup: {backup}")

# Replace de cada false -> true (do final pro comeco pra preservar offsets)
for offset in sorted(to_fix, reverse=True):
    content = content[:offset] + b'true' + content[offset+5:]

with open(path, 'wb') as f:
    f.write(content)
print(f"OK: {len(to_fix)} entrada(s) viraram trust=true. Reinicie o Claude Code.")
PYEOF
```

**IMPORTANTE:** Nunca usar `json.load`/`json.dump` no `~/.claude.json` — o arquivo contem caracteres Unicode surrogates em paths do Windows que corrompem na serializacao. Sempre usar leitura/escrita binaria.

Antes de executar, explicar ao usuario:

> "Pra barra de status funcionar, preciso ativar o **workspace trust** neste projeto.
>
> O workspace trust e uma trava de seguranca do Claude Code. Quando voce abre um projeto, o Claude pergunta se confia nele. Enquanto nao aceitar, ele bloqueia qualquer coisa que execute codigo automaticamente — como a barra de status, hooks e plugins.
>
> Esse projeto esta com o trust desativado, por isso a statusline nao aparece. Posso ativar agora? Vou cobrir todas as variantes do path desse projeto que existirem no arquivo de config (acumulam quando voce renomeia/move pasta)."

**Se sim:** executar o Bash acima e informar: "Trust ativado em N entrada(s). Reinicie o Claude Code pra barra voltar."

**Se nao:** informar: "Sem problema. A barra de status so funciona com trust ativo. Quando mudar de ideia, rode `/maestro-statusline` de novo."

**Se o Bash reportar "Todas ja em trust=true"** mas a barra continuar com `skipped`: problema esta em outro lugar (cache do Claude Code, settings local-level no projeto). Pedir pro usuario verificar `<CWD>/.claude/settings.local.json`.

### 2.4 Configurar os settings

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

### 2.5 Salvar estado

Atualizar `~/.maestro/config.md` — setar `statusline-ativo: true` na seção `## Status Line`.
Se a seção não existe, criá-la ao final do arquivo com todos os campos de preferências.

### 2.6 Confirmar

Informar:

> "Status line ativada! Ela aparece na próxima mensagem. Para desligar ou configurar, rode `/maestro-statusline`."
>
> Se a barra mostrar "statusline skipped", rode `/maestro-statusline` novamente — o sistema verifica e corrige o workspace trust automaticamente.

---

## 3. Fluxo de Desativação

### 3.1 Remover dos settings

1. Ler `~/.claude/settings.json`
2. Remover a chave `statusLine`
3. Salvar o arquivo preservando as demais configurações existentes

### 3.2 Atualizar estado

Atualizar `~/.maestro/config.md` — setar `statusline-ativo: false`.
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

Ler as preferências atuais de `~/.maestro/config.md` para montar o menu.

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

Aguardar resposta. Atualizar `statusline-itens` em `~/.maestro/config.md`.

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

Aguardar resposta. Atualizar `statusline-estilo-[item]` em `~/.maestro/config.md`.

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

1. Salvar preferências atualizadas em `~/.maestro/config.md`
2. Regenerar o script `~/.claude/maestro-statusline.sh` (mesmo fluxo da seção 2.2)
3. Informar: "Configuração atualizada! A barra já muda na próxima mensagem."

---

## 5. Tom e Estilo

- **Direto e prático** — sem jargão técnico
- **Sem persona** — é o Maestro falando
- **Frases curtas** — máximo 2-3 frases por mensagem
- **Use acentos corretos em português** — sempre
