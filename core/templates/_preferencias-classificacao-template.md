---
tipo: memoria
area: preferencias
escopo: classificacao
---

# Preferências de classificação

Registro de escolhas do usuário em `AskUserQuestion` de ambiguidade. Após 3 ocorrências do mesmo padrão com a mesma escolha, o Maestro passa a assumir a preferência (mas avisa sempre com opção de override).

## Padrão

Cada entrada no formato:

```
- Padrão: [verbo + substantivo + modificadores]
  - Exemplos: "cria headline rápido", "escreve post corrido"
  - Escolha do usuário: [Conversa/Rascunho/Refinamento/Entrega/Plano]
  - Contador: N/3 (ou "ativo" quando ≥3)
  - Última ocorrência: YYYY-MM-DD
```

## Entradas

(vazio no início — Maestro popula ao longo do uso)
