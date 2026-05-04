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

### 1.1 Migração: apagar cache global legado (idempotente)

A partir do fix B-F1-1 (Sessão 66), o cache de projeto-ativo vive na workspace local — não há mais pasta global. Apagar a pasta legada na primeira execução pós-fix:

```bash
if [ -d "$HOME/.maestro/projeto-ativo-cache" ]; then
  rm -rf "$HOME/.maestro/projeto-ativo-cache"
fi
```

Custo após primeira execução: 1 stat (idempotente). Conteúdo da pasta legada é descartável (caches stale do refactor `macro:` → `workspace:` da Sessão 63 e formatos pré-F1).

### 1.2 Detectar workspace via dirname-up

```bash
if command -v cygpath >/dev/null 2>&1; then
  CWD_NORM=$(cygpath -m "$(pwd)")
else
  CWD_NORM=$(pwd | tr '\\' '/')
fi

# Detectar status direto: CWD = projeto?
if [ -f "$CWD_NORM/maestro/config.md" ]; then
  CANDIDATE_WORKSPACE=$(dirname "$CWD_NORM")
  if [ -f "$CANDIDATE_WORKSPACE/.maestro-workspace" ]; then
    PROJETO="$CWD_NORM"
    WORKSPACE="$CANDIDATE_WORKSPACE"
    STATUS="CWD-PROJETO"
  else
    # Vault legado pré-F1 ou projeto órfão (B-F1-8): parent não é workspace.
    # NUNCA escrever em parent. Cair em CWD-PROJETO-ORFAO pra AUQ.
    PROJETO="$CWD_NORM"
    WORKSPACE=""
    STATUS="CWD-PROJETO-ORFAO"
  fi
else
  # Subir dirname procurando marker .maestro-workspace
  DIR="$CWD_NORM"
  WORKSPACE=""
  COUNT=0
  while [ "$DIR" != "/" ] && [ "$DIR" != "" ] && [ "$COUNT" -lt 30 ]; do
    if [ -f "$DIR/.maestro-workspace" ]; then
      WORKSPACE="$DIR"
      break
    fi
    PARENT=$(dirname "$DIR")
    if [ "$PARENT" = "$DIR" ]; then break; fi  # raiz alcançada
    DIR="$PARENT"
    COUNT=$((COUNT + 1))
  done

  if [ -z "$WORKSPACE" ]; then
    STATUS="CWD-INVALIDO"
  else
    STATUS="CWD-WORKSPACE"
  fi
fi

CACHE_FILE="$WORKSPACE/.maestro/cache/projeto-ativo.md"
```

Limite de 30 níveis na escalada de parents protege contra loop infinito em paths raiz que não terminam em `/` (caso edge do Git Bash do Windows). Guard `[ "$PARENT" = "$DIR" ]` é a saída normal — limite é cap de segurança.

### 1.3 Ler cache local (se existe e workspace foi detectada)

Se `STATUS=CWD-WORKSPACE` ou `STATUS=CWD-PROJETO` e `$CACHE_FILE` existe, extrair frontmatter:
- `slug`
- `caminho-absoluto`
- `workspace`

Validar que `caminho-absoluto` ainda existe como pasta e contém `maestro/config.md`. Se não, marcar cache como **inválido** (será sobrescrito).

### 1.4 Aplicar matriz de decisão

| Status do CWD | Cache local | Ação |
|---|---|---|
| CWD-PROJETO | qualquer | Silencioso. `{projeto} = CWD`. Atualiza cache local em `<workspace>/.maestro/cache/projeto-ativo.md` |
| CWD-PROJETO-ORFAO | n/a | AUQ "Transformar esta pasta em workspace + projeto / Cancelar". Se transformar: cria `.maestro-workspace` no CWD, persiste cache em `<CWD>/.maestro/cache/`. Se cancelar: para sem ativar. **NUNCA escreve em parent.** Ver `ola-maestro/SKILL.md` Sub-fluxo CWD-PROJETO-ORFAO. |
| CWD-WORKSPACE, cache válido | preenchido | Silencioso. `{projeto} = cache.caminho-absoluto` |
| CWD-WORKSPACE, cache vazio/inválido, 1 projeto na workspace | qualquer | Auto-resolve silencioso (com aviso "1 projeto encontrado, ativando [X]"). Atualiza cache. |
| CWD-WORKSPACE, cache vazio/inválido, ≥2 projetos | qualquer | AUQ com lista dos projetos. Atualiza cache após escolha. |
| CWD-WORKSPACE, cache vazio/inválido, 0 projetos | qualquer | Recuperação 2B.-1 do onboarding (workspace meia-criada). |
| CWD-INVALIDO | n/a | Mensagem orientada: "Você não está numa pasta do Sistema Maestro. Entre na pasta de um projeto (`cd <nome-do-projeto>`) ou na pasta da sua área de trabalho que contém os projetos." |

> **Multi-window dentro do mesmo workspace:** todas as janelas leem/escrevem o mesmo cache local. Última escrita vence. Mesma limitação do modelo anterior — duas janelas em CWD=workspace já compartilhavam cache por hash idêntico.

### 1.5 Persistir cache local

Após resolução bem-sucedida (não em CWD-PROJETO-ORFAO antes da decisão do AUQ), escrever/atualizar `<workspace>/.maestro/cache/projeto-ativo.md`. Guard defensivo: persistir só se `WORKSPACE` está confirmada via marker (`.maestro-workspace` existe). Sem isso, B-F1-8 reaparece em qualquer caminho que esqueça a verificação.

```bash
# Guard contra B-F1-8: nunca escrever cache em pasta sem marker confirmado
[ -f "$WORKSPACE/.maestro-workspace" ] || exit 0

mkdir -p "$WORKSPACE/.maestro/cache"
cat > "$WORKSPACE/.maestro/cache/projeto-ativo.md" <<EOF
---
versao: 1
slug: <slug>
caminho-absoluto: <caminho-absoluto-do-projeto>
workspace: $WORKSPACE
atualizado-em: $(date -u +%Y-%m-%dT%H:%M:%SZ)
---
EOF
```

Tratamento de falhas:
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
- **Multi-window dentro do mesmo workspace:** todas as janelas compartilham `<workspace>/.maestro/cache/projeto-ativo.md`. Última escrita vence. Sem isolamento entre janelas no mesmo workspace — mesma limitação do modelo anterior por hash de CWD-workspace idêntico.
- **Resolução 1x por sessão:** mudança de CWD mid-session **não é detectada por design**. Claude Code mantém CWD fixo por sessão; tentar detectar mudança seria caro e raramente útil. Usuário usa `/projeto` pra trocar mid-session.
- **Cache versionado:** campo `versao: 1` no frontmatter habilita migração futura de schema.
- **Cache local em vez de global:** desde o fix B-F1-1 (Sessão 66), cache vive em `<workspace>/.maestro/cache/projeto-ativo.md`. Pasta global `~/.maestro/projeto-ativo-cache/` foi descontinuada — apagada silenciosamente na primeira execução pós-fix. Justificativa: cache global permitia contaminação cruzada entre CWDs distintos quando hash do CWD não tinha cache próprio (modelo fazia fallback pra outros caches em vez de cair em CWD-inválido).
- **Detecção semântica de troca rejeitada permanentemente.** Não tentar inferir troca de projeto a partir de menção a empresa/produto na mensagem do usuário — fonte conhecida de bug "modelo infere e troca contexto sem usuário perceber".
