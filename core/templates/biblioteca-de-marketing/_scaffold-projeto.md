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
│   │   ├── config.md
│   │   └── checklists/                ← Critérios de qualidade customizados (opcional, com README)
│   │       └── README.md
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
│   ├── planos/
│   │   └── _planos.md
│   ├── entrevistas/
│   │   └── _entrevistas.md
│   └── rascunhos/
│       └── _rascunhos.md
```

## Indexes Vazios por Área

> [!info] 9 áreas viraram painéis Dataview (Grupo E, v2.15.0)
> `identidade`, `escada-de-valor`, `lead-magnets`, `produtos`, `funis`, `lancamentos`, `campanhas`, `pesquisas`, `entregas` agora usam **cópia literal** dos templates em `plugin/core/templates/indexes-area/_<area>-index.md` (renomeando para `_<area>.md` no destino — sufixo `-index` cai). Ver "Ordem de Criação" abaixo. As 3 áreas restantes (`social`, `referencias`, `memorias`) seguem com indexes inline.

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
| identidade/ | Pasta + _identidade.md (cópia literal do painel Dataview) + 8 templates | — |
| escada-de-valor/ | Pasta + _escada-de-valor.md (cópia literal do painel Dataview) | Cada escada quando solicitada |
| lead-magnets/ | Pasta + _lead-magnets.md (cópia literal do painel Dataview) | Cada lead magnet quando solicitado |
| produtos/ | Pasta + _produtos.md (cópia literal do painel Dataview) | Pasta do produto + 8 templates quando solicitado |
| funis/ | Pasta + _funis.md (cópia literal do painel Dataview) | Cada funil quando solicitado |
| lancamentos/ | Pasta + _lancamentos.md (cópia literal do painel Dataview) | Cada lançamento quando solicitado |
| campanhas/ | Pasta + _campanhas.md (cópia literal do painel Dataview) | Cada campanha quando solicitada |
| social/ | Pasta + _social.md (inline) | Plataforma + mês + semana quando solicitado |
| pesquisas/ | Pasta + _pesquisas.md (cópia literal do painel Dataview) | Cada pesquisa pelo Pesquisador |
| entregas/ | Pasta + _entregas.md (cópia literal do painel Dataview) | Cada entrega avulsa |
| referencias/ | Pasta + _referencias.md (inline) | Cada arquivo pelo usuário |
| memorias/ | Pasta + _memorias.md (inline) | Cada arquivo de memória por agente |
| tarefas/ | Pasta + _tarefas.md (cópia literal do painel Dataview) | Cada tarefa pelo Gerente de Projetos |
| planos/ | Pasta + _planos.md (cópia literal do painel Dataview) | Cada plano pelo Gerente de Projetos |
| entrevistas/ | Pasta + _entrevistas.md (cópia literal do painel Dataview) | Cada entrevista pelo Gerente de Projetos |
| rascunhos/ | Pasta + _rascunhos.md (cópia literal do painel Dataview) | Cada rascunho pelo especialista via `/rascunho` |
| maestro/checklists/ | Pasta + README.md (cópia literal de _readme-checklists-projeto.md) | Cada arquivo de critério customizado pelo usuário ou via fluxo-needs |
| (raiz) _qa-reprovacoes.md | Cópia literal do painel Dataview | — |
| (raiz) _pendencias-aceitas.md | Cópia literal do painel Dataview | — |

## Ordem de Criação

1. Criar pasta do projeto (`[nome-da-empresa]/`)
2. `[nome-da-empresa].md` (dentro da pasta) — usar template _index-biblioteca.md, preenchendo `empresa:` e `criado:`
3. maestro/config.md
4. identidade/ — pasta + 8 templates de identidade preenchidos vazios + painel Dataview `_identidade.md` (cópia literal — ver passo 6)
5. Pastas com indexes inline (`social`, `referencias`, `memorias`) — usar conteúdo da seção "Indexes Vazios por Área" deste documento
6. **Os 15 painéis Dataview** (13 nas áreas + 2 na raiz do projeto) — pastas (quando aplicável) + painéis **copiados literalmente** dos templates abaixo, **renomeando `_X-index.md` → `_X.md`** no destino:

   | Origem (template) | Destino no vault |
   |-------------------|------------------|
   | `plugin/core/templates/_tarefas-index.md` | `tarefas/_tarefas.md` |
   | `plugin/core/templates/_planos-index.md` | `planos/_planos.md` |
   | `plugin/core/templates/_entrevistas-index.md` | `entrevistas/_entrevistas.md` |
   | `plugin/core/templates/_rascunhos-index.md` | `rascunhos/_rascunhos.md` |
   | `plugin/core/templates/indexes-area/_produtos-index.md` | `produtos/_produtos.md` |
   | `plugin/core/templates/indexes-area/_funis-index.md` | `funis/_funis.md` |
   | `plugin/core/templates/indexes-area/_lancamentos-index.md` | `lancamentos/_lancamentos.md` |
   | `plugin/core/templates/indexes-area/_campanhas-index.md` | `campanhas/_campanhas.md` |
   | `plugin/core/templates/indexes-area/_lead-magnets-index.md` | `lead-magnets/_lead-magnets.md` |
   | `plugin/core/templates/indexes-area/_escada-de-valor-index.md` | `escada-de-valor/_escada-de-valor.md` |
   | `plugin/core/templates/indexes-area/_pesquisas-index.md` | `pesquisas/_pesquisas.md` |
   | `plugin/core/templates/indexes-area/_entregas-index.md` | `entregas/_entregas.md` |
   | `plugin/core/templates/indexes-area/_identidade-index.md` | `identidade/_identidade.md` |
   | `plugin/core/templates/indexes-area/_qa-reprovacoes-index.md` | `_qa-reprovacoes.md` (raiz do projeto) |
   | `plugin/core/templates/indexes-area/_pendencias-aceitas-index.md` | `_pendencias-aceitas.md` (raiz do projeto) |

   Além disso, criar `maestro/checklists/` (vazia) + `maestro/checklists/README.md` (cópia literal de `plugin/core/templates/_readme-checklists-projeto.md`).

   **Não inventar conteúdo** — copiar literalmente. Cada painel precisa ter o callout `[!info]` + as queries Dataview do template pra funcionar. Ver `bibliotecario/SKILL.md` pro fluxo de validação de existência (caso template ausente, avisa user e continua sem painel).
