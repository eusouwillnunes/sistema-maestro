"""Testes para _slug.slugify."""
import sys
from pathlib import Path

# Permite import sem instalação como pacote
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _slug import slugify  # noqa: E402


def test_slugify_caso_normal():
    assert slugify("Padaria do João") == "padaria-do-joao"


def test_slugify_acentos():
    assert slugify("Açaí Aço") == "acai-aco"


def test_slugify_simbolos_e_pontuacao():
    assert slugify("L'Oréal & Co.") == "l-oreal-co"


def test_slugify_espacos_multiplos():
    assert slugify("  Casa   Verde  ") == "casa-verde"


def test_slugify_so_emojis_retorna_vazio():
    assert slugify("🎉🎊") == ""


def test_slugify_idempotente():
    s1 = slugify("Padaria do João")
    s2 = slugify(s1)
    assert s1 == s2
