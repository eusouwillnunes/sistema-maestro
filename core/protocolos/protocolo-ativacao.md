---
description: Protocolo compartilhado de resolução de projeto ativo + verificação de ativação do Sistema Maestro
tags:
  - "#maestro/protocolo"
---

# Protocolo de Ativação

> [!info] Protocolo compartilhado do sistema MAESTRO.
> Referenciado pelo hub do Maestro e pelas skills (ola-maestro, tchau-maestro) para (a) resolver qual projeto está ativo e (b) verificar se o Sistema Maestro está habilitado nele antes de executar.

## Objetivo

Garantir que toda interação tenha `{projeto}` resolvido pra caminho absoluto antes de qualquer operação de leitura/escrita no vault. Bloquear execução em projeto não-ativado.

---

## Sub-fluxo 1: Resolver Projeto Ativo

Roda **uma vez por sessão** (na primeira entrada do hub) e em invocação explícita de `/projeto`. Resultado fica em estado da sessão — não rerresolve em mensagens subsequentes.

### 1.1 Computar hash do CWD

```bash
# Normalizar CWD pra forward slash (Git Bash do Windows pode entregar backslash em alguns contextos)
CWD_NORM=$(echo "$CWD" | tr '\\' '/')
HASH=$(echo -n "$CWD_NORM" | md5sum | cut -c1-32)
CACHE_DIR="$HOME/.maestro/projeto-ativo-cache"
CACHE_FILE="$CACHE_DIR/${HASH}.md"
```

Cache por hash isola janelas Claude Code simultâneas (multi-window) — cada janela com CWD distinto tem cache próprio. Normalização garante que o mesmo CWD sempre produz o mesmo hash, independente de como o shell representa o path.

### 1.2 Ler cache (se existe)

Se `$CACHE_FILE` existe, extrair frontmatter:
- `slug`
- `caminho-absoluto`
- `macro`

Validar que `caminho-absoluto` ainda existe como pasta e contém `maestro/config.md`. Se não, marcar cache como **inválido** (será sobrescrito).

### 1.3 Detectar status do CWD

- **CWD-projeto** — `$CWD/maestro/config.md` existe com `maestro-ativo: true` no frontmatter
- **CWD-macro** — Glob `$CWD/*/maestro/config.md` em **profundidade 1** retorna ≥1 match com `maestro-ativo: true`
- **CWD-inválido** — nenhum dos dois

> Profundidade 1 + filtro `maestro-ativo: true` evita custo absurdo em CWD genérico (home dir) e falsos positivos.

### 1.4 Aplicar matriz de decisão

| CWD status | Cache | Ação |
|---|---|---|
| CWD-projeto = cache.caminho-absoluto | qualquer | Silencioso. `{projeto} = CWD`. Atualiza `atualizado-em` |
| CWD-projeto ≠ cache (cache válido) | preenchido | AUQ: "CWD em **[Y]**, cache em **[X]**. Trocar pra **[Y]**?" — opções: **[Sim, troca]** (default) / [Não, continua em **[X]**] / [Cancelar] |
| CWD-projeto, sem cache ou cache inválido | vazio/inválido | Silencioso. Grava cache. `{projeto} = CWD` |
| CWD-macro, cache aponta projeto **dentro** desta macro | preenchido válido | Silencioso. `{projeto} = cache.caminho-absoluto` |
| CWD-macro, cache vazio/inválido **ou** aponta projeto fora desta macro | qualquer | AUQ com lista dos projetos da macro atual. Auto-seleciona silencioso se lista tem exatamente 1 (com aviso "1 projeto encontrado, ativando [X]") |
| CWD-inválido | qualquer | Mensagem orientada: "Você está em pasta sem Maestro. Vai pra um projeto (`cd cliente-x`) ou roda `/iniciar-sessao` numa macro" |

### 1.5 Persistir cache

Após resolução bem-sucedida, escrever/atualizar `$CACHE_FILE`:

```yaml
---
versao: 1
slug: <slug>
caminho-absoluto: <caminho-absoluto>
macro: <pasta-pai-de-caminho-absoluto>
atualizado-em: <ISO 8601>
---
```

Tratamento de falhas:
- Se `$CACHE_DIR` não existe → criar via `mkdir -p`
- Se Write falha (permissão) → aviso "cache não pode ser persistido — projeto ativo válido só nessa sessão" + segue sem cache (matriz aplica toda sessão)

### 1.6 Output

Variáveis injetadas no estado da sessão:
- `{projeto}` — caminho absoluto, normalizado em forward slash. Exemplo: `C:/dev/clientes/cliente-x`
- `{projeto-slug}` — forma curta. Exemplo: `cliente-x`

O Maestro substitui literalmente `{projeto}` por caminho absoluto antes de injetar no bloco CONTEXTO de qualquer dispatch (ver `protocolo-contexto.md`).

---

## Sub-fluxo 2: Verificar Ativação no projeto resolvido

Após Sub-fluxo 1 produzir `{projeto}`:

### 2.1 Verificar config

Tente ler `{projeto}/maestro/config.md`.

### 2.2 Verificar campo de ativação

Verifique `maestro-ativo` no frontmatter.

### 2.3 Decidir

- **`{projeto}/maestro/config.md` não existe** → BLOQUEADO. Mensagem de bloqueio (Seção 3).
- **`maestro-ativo: false`** → BLOQUEADO. Mensagem de bloqueio.
- **`maestro-ativo: true`** → LIBERADO. Prosseguir.

---

## 3. Mensagem de bloqueio

Quando bloqueado, exibir exatamente:

> O Sistema Maestro não está ativo nesse projeto. Para ativar, digite o comando /maestro.

Não executar mais nada após a mensagem. Não sugerir alternativas. Não fazer perguntas.

---

## 4. Notas de implementação

- **Caminhos sempre normalizados:** forward slash, absoluto. Exemplo válido: `C:/dev/clientes/cliente-x`. Inválido: `C:\dev\clientes\cliente-x` ou `./cliente-x`. Comparação CWD vs. cache normaliza dos dois lados antes do match.
- **Multi-window:** cache por hash do CWD garante isolamento entre janelas Claude Code simultâneas. Sem race condition.
- **Resolução 1x por sessão:** mudança de CWD mid-session **não é detectada por design**. Claude Code mantém CWD fixo por sessão; tentar detectar mudança seria caro e raramente útil. Usuário usa `/projeto` pra trocar mid-session.
- **Cache versionado:** campo `versao: 1` no frontmatter habilita migração futura de schema.
- **Detecção semântica de troca rejeitada permanentemente.** Não tentar inferir troca de projeto a partir de menção a empresa/produto na mensagem do usuário — fonte conhecida de bug "modelo infere e troca contexto sem usuário perceber".
