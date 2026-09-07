#!/usr/bin/env python3
"""Genera le derivate web (re-encode q90, stessa risoluzione) e thumb (480px, q80)
per le foto incluse. Fonte di verita: _lavorazione/selezione_foto.csv.

Uscita: docs/assets/web/<sezione>/<file> e docs/assets/thumbs/<sezione>/<file>
"""
import csv
import os
import sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "_lavorazione", "selezione_foto.csv")
FOTO_DIR = os.path.join(ROOT, "Foto")
LOSTINLAMU_DIR = os.path.join(ROOT, "Lost in Lamu")
OUT_WEB = os.path.join(ROOT, "docs", "assets", "web")
OUT_THUMB = os.path.join(ROOT, "docs", "assets", "thumbs")

THUMB_LONG_SIDE = 480
WEB_QUALITY = 90
THUMB_QUALITY = 80

SLUG_BY_CODICE = {
    "s": "isola",
    "r": "rugby",
    "f": "animaflow",
    "a": "anidan",
    "d": "diario",
}


def make_web(src_path, dst_path):
    im = Image.open(src_path)
    if im.mode != "RGB":
        im = im.convert("RGB")
    im.save(dst_path, "JPEG", quality=WEB_QUALITY, optimize=True)


def make_thumb(src_path, dst_path):
    im = Image.open(src_path)
    if im.mode != "RGB":
        im = im.convert("RGB")
    w, h = im.size
    scale = THUMB_LONG_SIDE / max(w, h)
    if scale < 1:
        im = im.resize(
            (max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS
        )
    im.save(dst_path, "JPEG", quality=THUMB_QUALITY, optimize=True)


def process_foto():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    included = [r for r in rows if r["inclusa"].strip().upper() == "SI"]
    print(f"Foto/ incluse: {len(included)}")

    for slug in SLUG_BY_CODICE.values():
        os.makedirs(os.path.join(OUT_WEB, slug), exist_ok=True)
        os.makedirs(os.path.join(OUT_THUMB, slug), exist_ok=True)

    n = len(included)
    for i, row in enumerate(included, 1):
        codice = row["raccolta_codice"].strip()
        slug = SLUG_BY_CODICE.get(codice)
        if slug is None:
            print(f"ATTENZIONE: codice raccolta sconosciuto '{codice}' per {row['file']}, salto")
            continue

        fname = row["file"]
        src = os.path.join(FOTO_DIR, fname)
        web_dst = os.path.join(OUT_WEB, slug, fname)
        thumb_dst = os.path.join(OUT_THUMB, slug, fname)

        if not os.path.exists(src):
            print(f"MANCA sorgente: {src}")
            continue

        make_web(src, web_dst)
        make_thumb(src, thumb_dst)

        if i % 100 == 0 or i == n:
            print(f"  {i}/{n}")

    return len(included)


def process_lostinlamu():
    slug = "lostinlamu"
    os.makedirs(os.path.join(OUT_WEB, slug), exist_ok=True)
    os.makedirs(os.path.join(OUT_THUMB, slug), exist_ok=True)

    files = sorted(
        f for f in os.listdir(LOSTINLAMU_DIR) if f.lower().endswith(".jpg")
    )
    print(f"Lost in Lamu: {len(files)}")

    for fname in files:
        src = os.path.join(LOSTINLAMU_DIR, fname)
        web_dst = os.path.join(OUT_WEB, slug, fname)
        thumb_dst = os.path.join(OUT_THUMB, slug, fname)

        # gia' finita: copia as-is per il web, genera solo il thumb
        with open(src, "rb") as fsrc, open(web_dst, "wb") as fdst:
            fdst.write(fsrc.read())
        make_thumb(src, thumb_dst)

    return len(files)


def main():
    n_foto = process_foto()
    n_lil = process_lostinlamu()
    print(f"Totale derivate generate: {n_foto + n_lil}")


if __name__ == "__main__":
    sys.exit(main())
