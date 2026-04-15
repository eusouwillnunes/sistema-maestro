---
maestro-ativo: true
---

# Configuração do Usuário

## Personas Ativas

| Agente | Persona |
|--------|---------|
| copywriter | schwartz |
| estrategista | brunson-hormozi |
| marca | sinek-neumeier |
| midias-sociais | garyvee-kane |
| performance | perry-marshall |
| pesquisador | (sem persona) |
| bibliotecario | (sem persona) |

## Preferências Globais

(o sistema preenche automaticamente com base no uso)

## Configuração do Pesquisador

```yaml
ferramenta-default: websearch  # websearch | sonar | sonar-deep-research
openrouter-api-key:            # configurar para usar Perplexity
pasta-pesquisas: pesquisas/    # caminho relativo no vault do projeto
```

## Memórias

```yaml
memorias-usuario: ~/.maestro/memorias/   # global, fora do plugin
memorias-projeto: maestro/memorias/      # dentro do vault (por projeto)
```

## Modelos

Override de modelos por agente. Use `~` para manter o default do sistema.
Valores válidos: `opus`, `sonnet`, `haiku`, `~`

```yaml
modelos:
  copywriter: ~        # default: sonnet
  estrategista: ~      # default: sonnet
  marca: ~             # default: sonnet
  midias-sociais: ~    # default: sonnet
  performance: ~       # default: sonnet
  pesquisador: ~       # default: sonnet
  entrevistador: ~     # default: sonnet
  qa: ~                # default: haiku
  revisor: ~           # default: sonnet
  bibliotecario: ~     # default: haiku
  gerente: ~           # default: haiku
```

## Status Line

```yaml
statusline-ativo: false
statusline-itens: contexto, limite-5h, limite-7d, modelo
statusline-estilo-contexto: barra
statusline-estilo-limite-5h: numero
statusline-estilo-limite-7d: numero
statusline-estilo-modelo: texto
statusline-estilo-custo: numero
statusline-faixas-contexto: 40,60,70
```
