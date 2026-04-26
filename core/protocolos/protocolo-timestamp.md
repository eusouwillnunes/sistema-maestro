# Protocolo de Timestamp

Regra única e absoluta: **nunca chutar data/hora**. Sempre ler o timestamp atual do sistema via `Bash date` antes de gravar.

## Por que existe

O modelo tende a completar timestamps livremente (ex: arredondar pra "10:00:00" ou preservar a data mas errar a hora). Isso polui o histórico do vault: impossível reconstruir ordem real de edições, correlacionar com sessões, ou usar timestamps como proxy de recência em queries Dataview.

## Regra

Toda vez que for gravar data/hora em frontmatter, nome de arquivo ou corpo de artefato:

1. Execute `Bash` com o formato apropriado da tabela abaixo.
2. Use a saída **literal** como valor. Não arredonde, não ajuste, não estime.
3. Se por qualquer razão o `Bash` falhar, reporte o erro — **não tente chutar**.

## Formatos padrão

| Uso | Comando | Exemplo de saída |
|---|---|---|
| Frontmatter ISO 8601 (`data-criacao`, `data-inicio`, `data-conclusao`, `data-cancelamento`, `criado-em`, `adicionada-em`) | `date +"%Y-%m-%dT%H:%M:%S"` | `2026-04-24T07:23:41` |
| Nome de arquivo (tarefa, plano, rascunho, sessão, entrevista, artefato) | `date +"%Y-%m-%d-%H%M"` | `2026-04-24-0723` |
| Histórico legível (corpo de artefato, linha de log) | `date +"%Y-%m-%d %H:%M"` | `2026-04-24 07:23` |
| Só data (campo `data`, `expira-em`) | `date +"%Y-%m-%d"` | `2026-04-24` |
| Data + N dias (ex: `expira-em: hoje + 30 dias`) | `date -d "+30 days" +"%Y-%m-%d"` | `2026-05-24` |

## Proibido

- Chutar hora "arredondada" (`10:00:00`, `14:30:00`) sem ler do sistema.
- Reusar timestamp de turno anterior como se fosse agora.
- Preencher campo `~` quando o formato pede valor — reportar erro em vez disso.
- Inferir fuso horário — use o do sistema (sem `-u`) a menos que o campo exija UTC explicitamente.

## Uso

Skills e fluxos que gravam timestamps referenciam este protocolo via `> Aplica: [[protocolo-timestamp]]` no topo. A regra vale pra qualquer operação de escrita do sistema — Gerente, Maestro (fluxos), tchau-maestro, Bibliotecário e especialistas que preenchem histórico em artefatos.
