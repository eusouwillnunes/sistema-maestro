# Templates de Memórias de Projeto

Referência usada pelo Maestro no setup de um novo projeto. Cada seção abaixo corresponde a um arquivo criado em `maestro/memorias/` no vault.

---

## _index.md

```
# Index de Memórias — Projeto

(nenhuma memória registrada ainda)
```

---

## contexto.md

```
# Contexto do Projeto

## Negócio
- Produto/serviço:
- Modelo: (B2B / B2C / ambos)
- Ticket médio:
- Margem:

## Público-alvo
- Perfil:
- Faixa etária:
- Dor principal:
- Desejo principal:

## Mercado
- Nicho:
- Concorrentes diretos:
- Diferencial:
```

---

## sessoes/ (pasta)

Criar pasta vazia `sessoes/` dentro de `memorias/`. Arquivos individuais por sessão são criados dinamicamente pelo `/tchau-maestro`, no formato `YYYY-MM-DD-HHMM-foco.md`.

O índice `_sessoes.md` (com queries Dataview) é criado pelo `/tchau-maestro` na primeira sessão do projeto. Não precisa ser criado no setup inicial.

Ver template do arquivo de sessão em `plugin/core/templates/_sessao-template.md` e template do índice em `plugin/core/templates/_sessoes-index-template.md`.

### Compatibilidade com `sessoes.md` legado

Projetos antigos podem ter `memorias/sessoes.md` (arquivo único). O sistema preserva o arquivo intocado e, no primeiro `/tchau-maestro` pós-update, oferece migração opt-in das últimas entradas para a pasta nova.

---

## decisoes.md

```
# Decisões do Projeto

(registrado quando decisões importantes são tomadas durante o uso)
```

---

## agentes/ (pasta)

Criar pasta `agentes/` vazia. Arquivos por agente são criados dinamicamente quando houver feedbacks específicos do projeto.
