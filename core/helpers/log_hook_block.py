#!/usr/bin/env python3
"""
Helper pra registrar bloqueios do hook PreToolUse em historico.md.

Invocado por skills (sub-fluxo A) ou pelo hub Maestro (sub-fluxo B) quando
recebem deny do hook. Formato canonico do protocolo-agent.md secao 9.3.

Justificativa (aprendizado #47): logica deterministica de timestamp +
formato + atomic append nao deve ser gerada inline pelo modelo a cada
bloqueio — helper garante formato consistente pro painel Dataview.
"""
import argparse
import datetime
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--evento", required=True)
    ap.add_argument("--skill", default="desconhecido")
    ap.add_argument("--target", required=True)
    ap.add_argument("--agente", default="maestro")
    ap.add_argument("--projeto-path", required=True)
    args = ap.parse_args()

    projeto = Path(args.projeto_path)
    historico = projeto / "memorias" / "auditoria" / "historico.md"
    if not historico.parent.exists():
        print(
            f"erro: pasta de auditoria nao existe ({historico.parent})",
            file=sys.stderr,
        )
        return 2

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    linha = (
        f"- {timestamp} — {args.evento} | skill: {args.skill} | "
        f"target: {args.target} | agente: {args.agente} | tarefa: null\n"
    )

    # Cria historico.md se nao existe (pasta existe — checado acima)
    if not historico.exists():
        historico.write_text("# Historico de auditoria\n\n", encoding="utf-8")

    with historico.open("a", encoding="utf-8") as f:
        f.write(linha)

    print(f"ok: registrado em {historico}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
