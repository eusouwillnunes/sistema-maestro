#!/usr/bin/env python3
"""
Helper de verificacao de ferramentas pro onboarding do Sistema Maestro.

Sub-comandos:
- detect: detecta Python, Pandoc, libs e Obsidian. Emite JSON.
- install: instala ferramenta via gerenciador do SO. Emite JSON.
- log: grava Markdown de auditoria em memorias/auditoria/checks-de-ferramenta/.
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path


APPX_TIMEOUT = 1.0
INSTALL_TIMEOUT = 30.0
WINGET_VERSION_TIMEOUT = 2.0
WHICH_TIMEOUT = 2.0
PYTHON_MIN_VERSION = (3, 10)
PANDOC_MIN_VERSION = (2, 0)


def detect_obsidian_windows() -> dict:
    """Detecta Obsidian no Windows iterando 4 paths + fallback AppxPackage."""
    paths = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Obsidian" / "Obsidian.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Obsidian" / "Obsidian.exe",
        Path(os.environ.get("PROGRAMFILES", "")) / "Obsidian" / "Obsidian.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Obsidian" / "Obsidian.exe",
    ]
    for p in paths:
        if p.exists():
            return {"instalado": True, "metodo": f"path:{p.parent}"}

    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Get-AppxPackage -Name Obsidian.Obsidian"],
            capture_output=True, text=True, timeout=APPX_TIMEOUT,
        )
        if result.returncode == 0 and result.stdout.strip():
            return {"instalado": True, "metodo": "store:AppxPackage"}
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    return {"instalado": False, "metodo-tentado": "paths+AppxPackage"}


def detect_obsidian_mac() -> dict:
    """Detecta Obsidian no Mac via /Applications/Obsidian.app."""
    app_path = Path("/Applications/Obsidian.app")
    if app_path.exists():
        return {"instalado": True, "metodo": f"path:{app_path.as_posix()}"}
    return {"instalado": False, "metodo-tentado": "/Applications/Obsidian.app"}


def detect_obsidian_linux() -> dict:
    """Detecta Obsidian no Linux via which."""
    try:
        result = subprocess.run(
            ["which", "obsidian"], capture_output=True, text=True, timeout=WHICH_TIMEOUT
        )
        if result.returncode == 0 and result.stdout.strip():
            return {"instalado": True, "metodo": f"which:{result.stdout.strip()}"}
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return {"instalado": False, "metodo-tentado": "which:obsidian"}


def _parse_python_version(stdout: str):
    """Parse 'Python 3.14.0' -> (3, 14, 0). Retorna None se nao parsear."""
    m = re.search(r"Python (\d+)\.(\d+)(?:\.(\d+))?", stdout)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3) or 0))


def detect_python() -> dict:
    """Detecta Python 3.10+. Tenta 'python' depois 'python3'."""
    for cmd_name in ("python", "python3"):
        try:
            result = subprocess.run(
                [cmd_name, "--version"], capture_output=True, text=True, timeout=WHICH_TIMEOUT
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            continue
        if result.returncode != 0:
            continue
        version = _parse_python_version(result.stdout)
        if version is None:
            continue
        versao_str = ".".join(str(v) for v in version)
        if version < PYTHON_MIN_VERSION:
            return {"instalado": False, "motivo": "versao-antiga", "versao-detectada": versao_str}
        return {"instalado": True, "versao": versao_str, "metodo": f"command:{cmd_name}"}
    return {"instalado": False, "motivo-tentado": "python+python3"}


def _parse_pandoc_version(stdout: str):
    """Parse 'pandoc X.Y.Z[.W]' -> (tuple, versao_str). Retorna None se nao parsear."""
    # Grupo extra (?:\.\d+)* captura versoes legacy 4-segmento (ex: 1.19.2.4)
    # pra exibir string completa em versao-detectada; tupla compara so major.minor.patch.
    m = re.search(r"pandoc\s+((\d+)\.(\d+)(?:\.(\d+))?(?:\.\d+)*)", stdout)
    if not m:
        return None
    versao_str = m.group(1)
    major = int(m.group(2))
    minor = int(m.group(3))
    patch = int(m.group(4) or 0)
    return (major, minor, patch), versao_str


def detect_pandoc() -> dict:
    """Detecta Pandoc 2.0+."""
    try:
        result = subprocess.run(
            ["pandoc", "--version"], capture_output=True, text=True, timeout=WHICH_TIMEOUT
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return {"instalado": False, "metodo-tentado": "command:pandoc"}
    if result.returncode != 0:
        return {"instalado": False, "metodo-tentado": "command:pandoc"}
    parsed = _parse_pandoc_version(result.stdout)
    if parsed is None:
        return {"instalado": False, "motivo-tentado": "parse-falhou"}
    version, versao_str = parsed
    if version < PANDOC_MIN_VERSION:
        return {"instalado": False, "motivo": "versao-antiga", "versao-detectada": versao_str}
    return {"instalado": True, "versao": versao_str, "metodo": "command:pandoc"}


LIBS_NECESSARIAS = ["docx", "openpyxl", "pdfplumber"]


def detect_libs() -> dict:
    """Detecta libs Python necessarias (docx, openpyxl, pdfplumber)."""
    faltando = [lib for lib in LIBS_NECESSARIAS if importlib.util.find_spec(lib) is None]
    if not faltando:
        return {"instalado": True, "faltando": []}
    return {"instalado": False, "faltando": faltando}


def detect_package_manager(os_name: str) -> str:
    """Detecta gerenciador disponivel. Retorna 'winget'/'brew'/'apt'/'none'."""
    cmd_map = {
        "windows": (["winget", "--version"], "winget"),
        "macos": (["brew", "--version"], "brew"),
        "linux": (["apt", "--version"], "apt"),
    }
    if os_name not in cmd_map:
        return "none"
    cmd, name = cmd_map[os_name]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=WINGET_VERSION_TIMEOUT
        )
        return name if result.returncode == 0 else "none"
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return "none"


def _detect_os() -> str:
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    return "linux"


COMANDOS = {
    "python": {
        "windows": ["winget", "install", "--id", "Python.Python.3.14", "-e", "--silent"],
        "macos":   ["brew", "install", "python"],
        "linux":   ["sudo", "apt", "install", "-y", "python3", "python3-pip"],
    },
    "pandoc": {
        "windows": ["winget", "install", "--id", "JohnMacFarlane.Pandoc", "-e", "--silent"],
        "macos":   ["brew", "install", "pandoc"],
        "linux":   ["sudo", "apt", "install", "-y", "pandoc"],
    },
    "libs": {
        "default":  ["pip", "install", "python-docx", "openpyxl", "pdfplumber"],
        "fallback": ["pip", "install", "--user", "python-docx", "openpyxl", "pdfplumber"],
    },
}


LINKS_MANUAIS = {
    "python": "https://www.python.org/downloads/",
    "pandoc": "https://pandoc.org/installing.html",
    "libs": "pip install python-docx openpyxl pdfplumber",
    "obsidian": "https://obsidian.md/download",
}


def _resumir_stderr(stderr: str, max_lines: int = 5) -> str:
    linhas = [ln for ln in stderr.splitlines() if ln.strip()]
    return "\n".join(linhas[-max_lines:])


def cmd_install_impl(ferramenta: str, os_name: str, isatty_true: bool) -> dict:
    """Executa install. Retorna dict (nao imprime). isatty_true = sys.stdin.isatty()."""
    if ferramenta == "libs":
        cmd = COMANDOS["libs"]["default"]
        fallback = COMANDOS["libs"]["fallback"]
    else:
        cmd = COMANDOS.get(ferramenta, {}).get(os_name)
        fallback = None
        if cmd is None:
            return {
                "status": "sem-gerenciador",
                "link-manual": LINKS_MANUAIS.get(ferramenta, ""),
                "mensagem-natural": f"Nao tenho comando de install pra {ferramenta} no {os_name}.",
            }

    # Pre-check sudo-sem-tty
    if cmd[0] == "sudo" and not isatty_true:
        comando_sugerido = " ".join(cmd)
        return {
            "status": "sudo-sem-tty",
            "comando-sugerido": comando_sugerido,
            "mensagem-natural": f"Preciso rodar `{comando_sugerido}` no seu terminal — abre um terminal, cola o comando, depois me chama.",
        }

    def _run(cmd_list):
        return subprocess.run(
            cmd_list, capture_output=True, text=True, timeout=INSTALL_TIMEOUT
        )

    try:
        result = _run(cmd)
    except (FileNotFoundError, OSError):
        return {
            "status": "sem-gerenciador",
            "link-manual": LINKS_MANUAIS.get(ferramenta, ""),
            "mensagem-natural": f"Gerenciador de pacotes nao disponivel pro {ferramenta}. Instala manualmente em {LINKS_MANUAIS.get(ferramenta, '')}.",
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "comando-sugerido": " ".join(cmd),
            "mensagem-natural": f"A instalacao do {ferramenta} demorou demais e travou. Tenta rodar `{' '.join(cmd)}` no seu terminal manualmente.",
        }

    if result.returncode == 0:
        return {"status": "ok", "mensagem-natural": f"{ferramenta} instalado com sucesso."}

    # Fallback --user pra libs
    if ferramenta == "libs" and fallback is not None:
        try:
            result2 = _run(fallback)
            if result2.returncode == 0:
                return {"status": "ok", "mensagem-natural": "Libs instaladas com --user."}
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass

    return {
        "status": "falhou",
        "codigo": result.returncode,
        "stderr-resumido": _resumir_stderr(result.stderr),
        "mensagem-natural": f"Nao consegui instalar {ferramenta} (codigo {result.returncode}).",
    }


def cmd_install(ferramenta: str, os_name: str) -> int:
    """Wrapper CLI: imprime JSON do install."""
    isatty = sys.stdin.isatty()
    payload = cmd_install_impl(ferramenta, os_name, isatty_true=isatty)
    print(json.dumps(payload, ensure_ascii=True))
    sys.stdout.flush()
    return 0


def _timestamp_to_slug(iso_ts: str) -> str:
    """2026-05-20T14:22:00Z -> 20260520-142200."""
    safe = re.sub(r"[^0-9]", "", iso_ts[:19])
    return f"{safe[:8]}-{safe[8:14]}"


def cmd_log_impl(workspace: Path, payload: dict) -> int:
    """Grava log Markdown idempotente."""
    pasta = workspace / "memorias" / "auditoria" / "checks-de-ferramenta"
    pasta.mkdir(parents=True, exist_ok=True)

    slug = _timestamp_to_slug(payload["timestamp-iso"])
    arquivo = pasta / f"check-{slug}.md"

    if arquivo.exists():
        return 0  # idempotente

    frontmatter_lines = [
        "---",
        "tipo: check-de-ferramenta",
        "status: concluido",
        f"data-execucao: {payload['timestamp-iso']}",
        f"os: {payload['os']}",
        f"package-manager: {payload['package-manager']}",
        "ferramentas-detectadas:",
    ]
    for tool, info in payload["ferramentas-detectadas"].items():
        frontmatter_lines.append(f"  {tool}: {json.dumps(info, ensure_ascii=True)}")
    frontmatter_lines.append(f"ferramentas-instaladas: {json.dumps(payload['ferramentas-instaladas'], ensure_ascii=True)}")
    frontmatter_lines.append(f"ferramentas-puladas: {json.dumps(payload['ferramentas-puladas'], ensure_ascii=True)}")
    frontmatter_lines.append(f"duracao-segundos: {payload['duracao-segundos']}")
    frontmatter_lines.append("---")
    frontmatter_lines.append("")
    frontmatter_lines.append(f"# Checagem de ferramentas — {payload['timestamp-iso']}")
    frontmatter_lines.append("")
    frontmatter_lines.append("Helper rodou em sessao de onboarding. Log preservado pra historico navegavel.")

    arquivo.write_text("\n".join(frontmatter_lines), encoding="utf-8")
    return 0


def cmd_log(workspace_path: str, json_inline: str) -> int:
    """Wrapper CLI."""
    workspace = Path(workspace_path)
    try:
        payload = json.loads(json_inline)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "json-invalido", "erro": str(e)}, ensure_ascii=True), file=sys.stderr)
        return 1
    rc = cmd_log_impl(workspace, payload)
    slug = _timestamp_to_slug(payload["timestamp-iso"])
    arquivo = workspace / "memorias" / "auditoria" / "checks-de-ferramenta" / f"check-{slug}.md"
    print(json.dumps({"status": "ok", "arquivo": str(arquivo)}, ensure_ascii=True))
    return rc


def cmd_detect() -> int:
    """Executa detect completo e emite JSON."""
    os_name = _detect_os()
    detect_obsidian = {
        "windows": detect_obsidian_windows,
        "macos": detect_obsidian_mac,
        "linux": detect_obsidian_linux,
    }.get(os_name, detect_obsidian_linux)
    payload = {
        "os": os_name,
        "package-manager": detect_package_manager(os_name),
        "ferramentas": {
            "python": detect_python(),
            "pandoc": detect_pandoc(),
            "libs": detect_libs(),
            "obsidian": detect_obsidian(),
        },
    }
    print(json.dumps(payload, ensure_ascii=True))
    sys.stdout.flush()
    return 0


def main():
    parser = argparse.ArgumentParser(description="Verificacoes de ferramenta pro Sistema Maestro.")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("detect")
    p_install = sub.add_parser("install")
    p_install.add_argument("ferramenta", choices=["python", "pandoc", "libs"])
    p_install.add_argument("--os", dest="os_name", choices=["windows", "macos", "linux"], required=True)
    p_log = sub.add_parser("log")
    p_log.add_argument("--workspace", required=True)
    p_log.add_argument("--json", dest="json_inline", required=True)
    args = parser.parse_args()

    if args.cmd == "detect":
        return cmd_detect()
    if args.cmd == "install":
        return cmd_install(args.ferramenta, args.os_name)
    if args.cmd == "log":
        return cmd_log(args.workspace, args.json_inline)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
