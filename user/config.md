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
memorias-usuario: user/memorias/         # dentro do plugin (global)
memorias-projeto: maestro/memorias/      # dentro do vault (por projeto)
```
