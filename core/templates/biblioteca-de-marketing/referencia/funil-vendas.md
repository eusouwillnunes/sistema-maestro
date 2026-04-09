---
titulo: Funil de Vendas
tipo: referencia
usado-por: Estrategista
gera-em: funis/[nome]/
pre-requisitos: identidade, dossie-produto, perfil-prospect, oferta-irresistivel
tags: [referencia, funil-vendas, estrategia]
---

# Funil de Vendas

> [!info] Template de referência
> Este template é usado pelo Maestro como receita para gerar entregas.
> Não é copiado para o projeto do usuário.

## Pré-requisitos

- [[identidade]] preenchida
- [[dossie-produto]] do(s) produto(s) vinculado(s)
- [[perfil-prospect]] definido
- [[oferta-irresistivel]] estruturada para o produto principal

## Estrutura da Entrega

### 1. Visão Geral

- Produto(s) vinculado(s) (wiki-links)
- Tipo de funil: Perpétuo, Lançamento, Webinar, VSL Direto, Aplicação
- Status atual: em construção, ativo, pausado

### 2. Arquitetura do Funil

- Fluxo principal: Tráfego → Captura → Nutrição → Conversão → Checkout → Pós-venda
- Fluxos alternativos: remarketing, recuperação de carrinho, no-show

### 3. Etapas Detalhadas

#### Etapa 1 — Tráfego (Entrada)
Canais utilizados, investimento mensal, CPL alvo, volume de leads/mês.
Assets vinculados: criativos de tráfego.

#### Etapa 2 — Captura
URL da página, promessa/hook principal, isca digital utilizada,
taxa de conversão alvo. Assets: copy da página de captação.

#### Etapa 3 — Nutrição
Mecanismo (email, WhatsApp, ambos), quantidade de touchpoints,
duração da sequência, objetivo por fase.
Assets: sequência de emails.

#### Etapa 4 — Conversão
Mecanismo (VSL, webinar, call, página direta), duração,
taxa de conversão alvo. Assets: roteiro de VSL/webinar.

#### Etapa 5 — Página de Vendas / Checkout
URLs, order bump (sim/não e qual), upsell (sim/não e qual),
ticket médio alvo. Assets: copy da página de vendas.

#### Etapa 6 — Pós-venda
Onboarding, primeiro contato, responsável, ações de retenção.

### 4. Métricas e Resultados

Tabela por etapa com colunas: Etapa | Métrica | Meta.
Métricas-chave: CPL, taxa de conversão por etapa, taxa de abertura,
ROAS, CAC, ticket médio.

### 5. Histórico de Otimizações

Registro cronológico de mudanças e seus impactos no funil.
Formato: data, o que mudou, resultado observado.

### 6. Checklist de Assets

Lista de todos os assets necessários para o funil funcionar:
- Criativos de tráfego
- Copy da página de captação
- Sequência de emails
- Roteiro de VSL/webinar
- Copy da página de vendas

## Pastas e Arquivos Gerados

```
funis/
  [nome]/
    estrutura.md            ← arquitetura e fluxos do funil
    pagina-captacao.md      ← copy e especificações da landing page
    pagina-vendas.md        ← copy e especificações da página de vendas
    sequencia-emails/       ← pasta com emails da sequência de nutrição
```

## Frameworks e Metodologia

- **Funil de 6 Etapas** — Tráfego, Captura, Nutrição, Conversão, Vendas, Pós-venda
- **Fluxos Alternativos** — remarketing e recuperação como caminhos paralelos
- **Métricas por Etapa** — acompanhamento granular de performance
- Wiki-links para [[dossie-produto]], [[oferta-irresistivel]] e [[escada-de-valor]]
