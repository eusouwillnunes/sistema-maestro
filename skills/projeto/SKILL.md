---
name: projeto
description: Slash command pra trocar projeto ativo mid-session sem mudar CWD. Lista projetos da macro atual. Atualiza cache de projeto ativo. Uso /projeto, /projeto <slug>, /projeto listar.
model: sonnet
tools: Read, Write, Glob, Bash, AskUserQuestion
---

# Projeto

> Aplica: [[protocolo-ativacao]]

## 1. Papel

Permite ao usuário inspecionar projeto ativo e trocar pra outro projeto da mesma macro sem fechar o Claude Code. Operacional — sem produção criativa.

## 2. Modos

| Comando | Comportamento |
|---|---|
| `/projeto` (sem arg) | Mostra projeto ativo + lista os outros disponíveis na macro |
| `/projeto <slug>` | Troca direto se slug bate. Se não bate, AUQ com lista. Atualiza cache |
| `/projeto listar` | Só lista, não troca |

## 3. Detecção de projetos disponíveis

Glob `{macro}/*/maestro/config.md` em **profundidade 1**, onde `{macro}` é o parent dir do `{projeto}` ativo. Filtra pelos que têm `maestro-ativo: true` no frontmatter.

Se cache vazio (primeira chamada sem projeto ativo prévio), AUQ pede pra usuário escolher um projeto a partir do CWD.

## 4. Output esperado de `/projeto`

```
Projeto ativo: cliente-x (C:/dev/clientes/cliente-x)
Macro: C:/dev/clientes

Outros projetos disponíveis:
- cliente-y
- cliente-z
- meu-pessoal

Pra trocar: /projeto <slug>
```

## 5. Output de `/projeto <slug>` (sucesso)

```
Trocado pra cliente-y (C:/dev/clientes/cliente-y).
```

Cache atualizado silenciosamente. Próxima mensagem já roda no projeto novo.

## 6. Output de `/projeto <slug>` (slug não bate)

`AskUserQuestion` com lista dos projetos da macro:

- question: "Slug `<inválido>` não bate. Escolhe qual?"
- options: [cada projeto da macro com label = slug]

Após escolha, mesmo flow de troca da Seção 5.

## 7. Não-objetivos

- `/projeto criar` — criação continua via `/maestro-onboarding`
- `/projeto remover/renomear` — operações de gestão de projetos não cabem aqui (fora de escopo)
- `/projeto --all` (cross-macro) — fica pro P1 grafo cross-project

## 8. Atualização de cache

Após troca, atualizar `~/.maestro/projeto-ativo-cache/{md5-do-CWD-inicial}.md`:

```bash
# Normalizar CWD pra forward slash (Git Bash do Windows pode vir com backslash)
CWD_NORM=$(echo "$CWD" | tr '\\' '/')
HASH=$(echo -n "$CWD_NORM" | md5sum | cut -c1-32)
mkdir -p "$HOME/.maestro/projeto-ativo-cache"
cat > "$HOME/.maestro/projeto-ativo-cache/${HASH}.md" <<EOF
---
versao: 1
slug: <novo-slug>
caminho-absoluto: <caminho-novo-absoluto-normalizado>
macro: <macro>
atualizado-em: <ISO 8601 agora>
---
EOF
```

Se Write falha (permissão), aviso "cache não pode ser persistido — projeto ativo válido só nessa sessão" + segue.

## 9. Estado da sessão

Após troca, atualizar variáveis em estado da sessão:
- `{projeto}` — caminho absoluto novo
- `{projeto-slug}` — forma curta nova

Próximos dispatches Agent() recebem o `{projeto}` substituído pelo caminho novo no bloco CONTEXTO.
