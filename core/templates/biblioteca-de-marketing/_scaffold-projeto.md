---
titulo: Scaffold do Projeto
tipo: meta
descricao: >
  Define a estrutura completa de pastas e indexes vazios que o /biblioteca
  cria dentro da pasta do projeto (nomeada pela empresa). Cada index
  vazio funciona como guia.
tags: [meta, scaffold, biblioteca]
---

# Scaffold do Projeto

> [!info] Documento de referência
> Este documento é usado pelo comando /biblioteca para scaffoldar a estrutura
> do projeto no vault do usuário. Não é copiado diretamente.

## Estrutura de Pastas

```
[raiz]/
├── [nome-da-empresa]/                    ← Pasta do projeto (lowercase, hifens, sem acentos)
│   ├── index.md                          ← Index geral (usar _index-biblioteca.md)
│   ├── maestro/
│   │   └── config.md
│   ├── identidade/
│   │   ├── index.md
│   │   ├── circulo-dourado.md            ← Camada 1
│   │   ├── posicionamento.md             ← Camada 1
│   │   ├── perfil-publico.md             ← Camada 1
│   │   ├── personalidade-marca.md        ← Camada 1
│   │   ├── tom-de-voz.md                 ← Camada 1
│   │   ├── identidade-visual.md          ← Camada 1
│   │   ├── manifesto.md                  ← Camada 3
│   │   └── historia-fundadores.md        ← Camada 3
│   ├── escada-de-valor/
│   │   └── index.md
│   ├── lead-magnets/
│   │   └── index.md
│   ├── produtos/
│   │   └── index.md
│   ├── funis/
│   │   └── index.md
│   ├── lancamentos/
│   │   └── index.md
│   ├── campanhas/
│   │   └── index.md
│   ├── social/
│   │   └── index.md
│   ├── pesquisas/
│   │   └── index.md
│   ├── entregas/
│   │   └── index.md
│   └── memorias/
│       └── index.md
```

## Indexes Vazios por Área

### identidade/index.md

```
---
titulo: Identidade da Marca
tipo: index
area: identidade
---

# Identidade da Marca

> [!info] Fundação
> A identidade é a base de tudo. Sem ela, nenhum agente consegue trabalhar com precisão.
> Comece pelo [[circulo-dourado]] — é o ponto de partida.

| Documento | Camada | Status | Link |
|-----------|--------|--------|------|
| Círculo Dourado | 1 (obrigatório) | vazio | [[circulo-dourado]] |
| Posicionamento | 1 (obrigatório) | vazio | [[posicionamento]] |
| Perfil do Público | 1 (obrigatório) | vazio | [[perfil-publico]] |
| Personalidade da Marca | 1 (obrigatório) | vazio | [[personalidade-marca]] |
| Tom de Voz | 1 (obrigatório) | vazio | [[tom-de-voz]] |
| Identidade Visual | 1 (obrigatório) | vazio | [[identidade-visual]] |
| Manifesto | 3 (enriquecimento) | vazio | [[manifesto]] |
| História dos Fundadores | 3 (enriquecimento) | vazio | [[historia-fundadores]] |
```

### escada-de-valor/index.md

```
---
titulo: Escada de Valor
tipo: index
area: escada-de-valor
---

# Escada de Valor

Nenhuma escada de valor criada ainda. Peça ao Maestro: "Quero montar minha escada de valor"

A Escada de Valor conecta seus [[lead-magnets/index|Lead Magnets]] e [[produtos/index|Produtos]] em uma sequência lógica de ascensão.

| Escada | Níveis | Status | Link |
|--------|--------|--------|------|
| (vazio) | — | — | — |
```

### lead-magnets/index.md

```
---
titulo: Lead Magnets
tipo: index
area: lead-magnets
---

# Lead Magnets

Nenhum lead magnet criado ainda. Peça ao Maestro: "Quero criar um lead magnet"

| Lead Magnet | Tipo | Produto Destino | Status | Link |
|-------------|------|-----------------|--------|------|
| (vazio) | — | — | — | — |
```

### produtos/index.md

```
---
titulo: Produtos
tipo: index
area: produtos
---

# Produtos

Nenhum produto criado ainda. Peça ao Maestro: "Quero criar um novo produto"

| Produto | Status | Documentos | Link |
|---------|--------|------------|------|
| (vazio) | — | — | — |
```

### funis/index.md

```
---
titulo: Funis de Vendas
tipo: index
area: funis
---

# Funis de Vendas

Nenhum funil criado ainda. Peça ao Maestro: "Quero criar um funil de vendas"

| Funil | Produto | Tipo | Status | Link |
|-------|---------|------|--------|------|
| (vazio) | — | — | — | — |
```

### lancamentos/index.md

```
---
titulo: Lançamentos
tipo: index
area: lancamentos
---

# Lançamentos

Nenhum lançamento criado ainda. Peça ao Maestro: "Quero planejar um lançamento"

Tipos disponíveis: Semente, Rápido (com Live), Meteórico.

| Lançamento | Produto | Tipo | Data | Status | Link |
|------------|---------|------|------|--------|------|
| (vazio) | — | — | — | — | — |
```

### campanhas/index.md

```
---
titulo: Campanhas
tipo: index
area: campanhas
---

# Campanhas

Nenhuma campanha criada ainda. Peça ao Maestro: "Quero criar uma campanha"

Tipos: flash sale, data comemorativa, remarketing, reativação, indicação, teste.

| Campanha | Produto | Tipo | Período | Status | Link |
|----------|---------|------|---------|--------|------|
| (vazio) | — | — | — | — | — |
```

### social/index.md

```
---
titulo: Social
tipo: index
area: social
---

# Social

Nenhum conteúdo criado ainda. Peça ao Maestro: "Quero planejar conteúdo para redes sociais"

Organização: plataforma → mês → semana → pasta por post.

| Plataforma | Link |
|------------|------|
| (nenhuma) | — |
```

### pesquisas/index.md

```
---
titulo: Pesquisas
tipo: index
area: pesquisas
---

# Pesquisas

Nenhuma pesquisa realizada ainda. Use /pesquisar ou peça ao Maestro.

| Data | Título | Tipo | Ferramenta | Link |
|------|--------|------|------------|------|
```

### entregas/index.md

```
---
titulo: Entregas
tipo: index
area: entregas
---

# Entregas

Entregas avulsas dos agentes que não se encaixam em outra categoria.

| Data | Entrega | Agente | Link |
|------|---------|--------|------|
```

### memorias/index.md

```
---
titulo: Memórias
tipo: index
area: memorias
---

# Memórias

Memórias dos agentes — feedbacks, preferências e padrões identificados.

| Agente | Última Atualização | Link |
|--------|--------------------|------|
```

## O que é scaffoldado na criação vs sob demanda

| Área | Na criação | Sob demanda |
|------|-----------|-------------|
| identidade/ | Pasta + index + 8 templates | — |
| escada-de-valor/ | Pasta + index | Cada escada quando solicitada |
| lead-magnets/ | Pasta + index | Cada lead magnet quando solicitado |
| produtos/ | Pasta + index | Pasta do produto + 8 templates quando solicitado |
| funis/ | Pasta + index | Cada funil quando solicitado |
| lancamentos/ | Pasta + index | Cada lançamento quando solicitado |
| campanhas/ | Pasta + index | Cada campanha quando solicitada |
| social/ | Pasta + index | Plataforma + mês + semana quando solicitado |
| pesquisas/ | Pasta + index | Cada pesquisa pelo Pesquisador |
| entregas/ | Pasta + index | Cada entrega avulsa |
| memorias/ | Pasta + index | Cada arquivo de memória por agente |

## Ordem de Criação

1. Criar pasta do projeto (`[nome-da-empresa]/`)
2. index.md (dentro da pasta) — usar template _index-biblioteca.md, preenchendo `empresa:` e `criado:`
3. maestro/config.md
4. identidade/ — pasta + index + 8 templates vazios
5. Demais pastas com indexes vazios
