#!/usr/bin/env python3
"""Genera provini (contact sheet) da una lista di file, a partire dai thumb gia' generati.

Uso:
    make_sheets.py <sezione> <out_prefix> [--cols N] [--rows N] [--cell PX] [--files f1,f2,...]

Se --files non e' passato, prende tutte le foto della sezione dal CSV, in ordine cronologico.
"""
import argparse
import csv
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "_lavorazione", "selezione_foto.csv")
THUMB_DIR = os.path.join(ROOT, "docs", "assets", "thumbs")
WEB_DIR = os.path.join(ROOT, "docs", "assets", "web")

SLUG_BY_CODICE = {"s": "isola", "r": "rugby", "f": "animaflow", "a": "anidan", "d": "diario"}

BG = (255, 255, 255)
LABEL_H = 26
PAD = 10


def load_font(size):
    for p in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def build_sheet(entries, cell, cols, rows, out_path, source_dir):
    """entries: lista di (path, label). Disegna una griglia cols x rows."""
    sheet_w = cols * cell + (cols + 1) * PAD
    sheet_h = rows * (cell + LABEL_H) + (rows + 1) * PAD
    sheet = Image.new("RGB", (sheet_w, sheet_h), BG)
    draw = ImageDraw.Draw(sheet)
    font = load_font(17)

    for i, (path, label) in enumerate(entries):
        c, r = i % cols, i // cols
        x = PAD + c * (cell + PAD)
        y = PAD + r * (cell + LABEL_H + PAD)

        im = Image.open(path)
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.thumbnail((cell, cell), Image.LANCZOS)
        ox = x + (cell - im.size[0]) // 2
        # allinea in basso nella cella, cosi' l'etichetta resta attaccata alla foto
        oy = y + (cell - im.size[1])
        sheet.paste(im, (ox, oy))
        draw.text((ox, y + cell + 4), label, fill=(0, 0, 0), font=font)

    sheet.save(out_path, "JPEG", quality=88, optimize=True)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sezione")
    ap.add_argument("out_prefix")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--rows", type=int, default=4)
    ap.add_argument("--cell", type=int, default=420)
    ap.add_argument("--files", default=None, help="lista di file separati da virgola")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--source", default="web", choices=["web", "thumb"])
    ap.add_argument("--outdir", default=os.path.join(ROOT, "_lavorazione", "sheets_lavoro"))
    args = ap.parse_args()

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows_csv = list(csv.DictReader(f))

    codice = {v: k for k, v in SLUG_BY_CODICE.items()}[args.sezione]
    photos = [
        r for r in rows_csv
        if r["raccolta_codice"] == codice and r["inclusa"].strip().upper() == "SI"
    ]
    photos.sort(key=lambda r: (r["scatto"], r["file"]))

    if args.files:
        wanted = [x.strip() for x in args.files.split(",")]
        idx = {r["file"]: r for r in photos}
        photos = [idx[w] for w in wanted if w in idx]

    photos = photos[args.offset:]
    if args.limit:
        photos = photos[: args.limit]

    source_dir = THUMB_DIR if args.source == "thumb" else WEB_DIR
    os.makedirs(args.outdir, exist_ok=True)

    per_sheet = args.cols * args.rows
    made = []
    for s in range(0, len(photos), per_sheet):
        chunk = photos[s : s + per_sheet]
        entries = []
        for r in chunk:
            path = os.path.join(source_dir, args.sezione, r["file"])
            num = os.path.splitext(r["file"])[0][-4:]
            forte = "*" if r["forte"].strip().upper() == "SI" else " "
            ora = r["scatto"].split()[-1][:5] if " " in r["scatto"] else ""
            entries.append((path, f"{num}{forte} {r['sessione']} {ora}"))
        n = s // per_sheet + 1
        out = os.path.join(args.outdir, f"{args.out_prefix}_{n:02d}.jpg")
        build_sheet(entries, args.cell, args.cols, args.rows, out, source_dir)
        made.append(out)
        print(out, len(chunk))

    print(f"\n{len(made)} provini, {len(photos)} foto")


if __name__ == "__main__":
    main()
