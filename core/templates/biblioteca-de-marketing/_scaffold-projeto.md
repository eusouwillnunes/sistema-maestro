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
│   ├── [nome-da-empresa].md              ← Index geral (usar _index-biblioteca.md)
│   ├── maestro/
│   │   └── config.md
│   ├── identidade/
│   │   ├── _identidade.md
│   │   ├── circulo-dourado.md            ← Camada 1
│   │   ├── posicionamento.md             ← Camada 1
│   │   ├── perfil-publico.md             ← Camada 1
│   │   ├── personalidade-marca.md        ← Camada 1
│   │   ├── tom-de-voz.md                 ← Camada 1
│   │   ├── identidade-visual.md          ← Camada 1
│   │   ├── manifesto.md                  ← Camada 3
│   │   └── historia-fundadores.md        ← Camada 3
│   ├── escada-de-valor/
│   │   └── _escada-de-valor.md
│   ├── lead-magnets/
│   │   └── _lead-magnets.md
│   ├── produtos/
│   │   └── _produtos.md
│   ├── funis/
│   │   └── _funis.md
│   ├── lancamentos/
│   │   └── _lancamentos.md
│   ├── campanhas/
│   │   └── _campanhas.md
│   ├── social/
│   │   └── _social.md
│   ├── pesquisas/
│   │   └── _pesquisas.md
│   ├── entregas/
│   │   └── _entregas.md
│   ├── referencias/
│   │   └── _referencias.md
│   ├── memorias/
│   │   └── _memorias.md
│   ├── tarefas/
│   │   └── _tarefas.md
│   └── entrevistas/
│       └── _entrevistas.md
```

## Indexes Vazios por Área

### identidade/_identidade.md

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

### escada-de-valor/_escada-de-valor.md

```
---
titulo: Escada de Valor
tipo: index
area: escada-de-valor
---

# Escada de Valor

Nenhuma escada de valor criada ainda. Peça ao Maestro: "Quero montar minha escada de valor"

A Escada de Valor conecta seus [[_lead-magnets|Lead Magnets]] e [[_produtos|Produtos]] em uma sequência lógica de ascensão.

| Escada | Níveis | Status | Link |
|--------|--------|--------|------|
| (vazio) | — | — | — |
```

### lead-magnets/_lead-magnets.md

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

### produtos/_produtos.md

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

### funis/_funis.md

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

### lancamentos/_lancamentos.md

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

### campanhas/_campanhas.md

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

### social/_social.md

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

### pesquisas/_pesquisas.md

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

### entregas/_entregas.md

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

### referencias/_referencias.md

```
---
tipo: index
area: referencias
atualizado: [data de criação]
---

# Material de Referência

Nenhum material importado ainda. Para importar, coloque seus arquivos nesta pasta e peça ao Maestro: "lê meus arquivos de referência"

| Arquivo | Formato | Descrição | Templates relacionados |
|---------|---------|-----------|----------------------|
```

### memorias/_memorias.md

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
| identidade/ | Pasta + _identidade.md + 8 templates | — |
| escada-de-valor/ | Pasta + _escada-de-valor.md | Cada escada quando solicitada |
| lead-magnets/ | Pasta + _lead-magnets.md | Cada lead magnet quando solicitado |
| produtos/ | Pasta + _produtos.md | Pasta do produto + 8 templates quando solicitado |
| funis/ | Pasta + _funis.md | Cada funil quando solicitado |
| lancamentos/ | Pasta + _lancamentos.md | Cada lançamento quando solicitado |
| campanhas/ | Pasta + _campanhas.md | Cada campanha quando solicitada |
| social/ | Pasta + _social.md | Plataforma + mês + semana quando solicitado |
| pesquisas/ | Pasta + _pesquisas.md | Cada pesquisa pelo Pesquisador |
| entregas/ | Pasta + _entregas.md | Cada entrega avulsa |
| referencias/ | Pasta + _referencias.md | Cada arquivo pelo usuário |
| memorias/ | Pasta + _memorias.md | Cada arquivo de memória por agente |
| tarefas/ | Pasta + _tarefas.md | Cada tarefa pelo Gerente de Projetos |
| entrevistas/ | Pasta + _entrevistas.md | Cada entrevista pelo Gerente de Projetos |

## Ordem de Criação

1. Criar pasta do projeto (`[nome-da-empresa]/`)
2. `[nome-da-empresa].md` (dentro da pasta) — usar template _index-biblioteca.md, preenchendo `empresa:` e `criado:`
3. maestro/config.md
4. identidade/ — pasta + _identidade.md + 8 templates vazios
5. Demais pastas com indexes vazios (nomeados `_[area].md`)
6. tarefas/ e entrevistas/ — pastas + indexes vazios (usando templates _tarefas-index.md e _entrevistas-index.md)
