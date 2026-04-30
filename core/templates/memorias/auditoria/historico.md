---
tipo: log-auditoria
descricao: Histórico append-only de eventos de auditoria do sistema (defesa anti-hallucination, futuros)
---

# Histórico de Auditoria

> Append-only. Cada linha é um evento. Não editar entradas anteriores.
>
> Formato: `- {YYYY-MM-DD HH:MM} — {evento} | agente: {agente} | {detalhes} | tarefa: [[{slug}]]`

## Eventos

(vazio — preenchido pelo Maestro quando defesa dispara)
