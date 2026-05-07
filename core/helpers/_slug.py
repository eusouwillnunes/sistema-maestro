#!/usr/bin/env python3
"""
Helper compartilhado de slugify pro Sistema Maestro.

Transforma texto livre num slug ASCII (lowercase, hifens, sem acentos):
  "Padaria do João" → "padaria-do-joao"
  "Açaí Aço" → "acai-aco"
  "🎉🎊" → ""  (vazio — caller decide se aceita)

Uso:
  from _slug import slugify
  slugify("Padaria do João")  # "padaria-do-joao"
"""
import re
import unicodedata


def slugify(text: str) -> str:
    """Converte texto em slug ASCII. Retorna string vazia pra entrada sem caracteres alfanuméricos."""
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(c for c in nfkd if not unicodedata.combining(c))
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text)
    ascii_text = ascii_text.strip("-")
    return ascii_text
