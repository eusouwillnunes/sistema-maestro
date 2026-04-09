---
titulo: Escada de Valor
tipo: referencia
usado-por: Estrategista
gera-em: escada-de-valor/
pre-requisitos: identidade, ao menos 1 produto cadastrado
tags: [referencia, escada-de-valor, estrategia]
---

# Escada de Valor

> [!info] Template de referência
> Este template é usado pelo Maestro como receita para gerar entregas.
> Não é copiado para o projeto do usuário.

## Pré-requisitos

- [[identidade]] preenchida (propósito, posicionamento, público)
- Ao menos 1 produto cadastrado com [[dossie-produto]] completo
- Recomendado: [[oferta-irresistivel]] definida para o produto principal

## Estrutura da Entrega

### 1. Visão Geral — Tabela dos 5 Níveis

Tabela com colunas: Nível | Produto | Preço | Objetivo | Funil vinculado.
Os 5 níveis clássicos (Russell Brunson):

| Nível | Objetivo | Ticket Típico |
|-------|----------|---------------|
| Lead Magnet | Capturar atenção, gerar lead | Gratuito |
| Tripwire | Converter lead em cliente (baixo risco) | R$ 7–97 |
| Core Offer | Transformação principal | R$ 497–2.997 |
| Profit Maximizer | Upsell, resultado acelerado | R$ 997–9.997 |
| Continuidade | Retenção, recorrência | R$ 97–497/mês |

### 2. Detalhamento por Nível

Para cada nível, gerar bloco com:
- Nome do produto/oferta naquele nível
- Formato (ebook, curso, mentoria, comunidade etc.)
- Promessa principal (resultado que entrega)
- Preço ou faixa de preço
- Conexão com próximo nível (como prepara o cliente para subir)

### 3. Fluxo Visual

Representação em texto da escada, do nível 5 (topo) ao nível 1 (entrada),
mostrando a progressão de valor e preço.

### 4. Métricas por Transição

Tabela com colunas: Transição | Taxa de Conversão | Meta.
Transições: Lead→Tripwire, Tripwire→Core, Core→Profit Max, Profit Max→Continuidade.
Incluir seção de LTV por caminho (parcial e completo).

### 5. Gaps na Escada

Tabela identificando quais níveis estão completos, incompletos ou ausentes.
Status possíveis: completo, em construção, ausente.
Coluna de ação necessária para cada gap.

### 6. Return Path (Caminho de Retorno)

Tabela com estratégias de retorno por segmento:
- Lead que não comprou tripwire
- Cliente tripwire que não comprou core
- Cliente core que não fez upsell
- Cliente que cancelou continuidade

## Pastas e Arquivos Gerados

```
escada-de-valor/
  [nome-da-marca].md    ← documento completo da escada
```

## Frameworks e Metodologia

- **Value Ladder** (Russell Brunson) — estrutura dos 5 níveis
- **Return Path** — estratégias de reativação por segmento
- **LTV por Caminho** — cálculo de valor vitalício por trajeto na escada
- Wiki-links para [[dossie-produto]] e funis vinculados a cada nível
