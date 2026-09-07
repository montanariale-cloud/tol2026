#!/usr/bin/env python3
"""Genera tutte le pagine statiche del sito in docs/ a partire da:
  _lavorazione/site_data/manifest.json   (foto per raccolta, con w/h)
  _lavorazione/site_data/bestof.json     (sequenza Best of)
"""
import json
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_lavorazione", "site_data")
DOCS = os.path.join(ROOT, "docs")

SEZIONI = [
    {"slug": "isola", "titolo": "L'Isola", "sottotitolo": "Street Photography",
     "tag": "01", "size": "wide", "intro": "isola", "no_download": True},
    {"slug": "rugby", "titolo": "Scuola di Rugby", "sottotitolo": "con Martin Castrogiovanni e Daniela Marzulli",
     "tag": "02", "size": "big", "sub": True, "intro": "rugby", "split": 2},
    {"slug": "animaflow", "titolo": "Anima Flow", "sottotitolo": "con Valeria De Chiara",
     "tag": "03", "size": "narrow", "intro": "animaflow"},
    {"slug": "anidan", "titolo": "Anidan", "sottotitolo": "e i suoi ragazzi",
     "tag": "04", "size": "wide", "intro": "anidan", "split": 2},
    {"slug": "diario", "titolo": "Diario", "sottotitolo": "delle vacanze",
     "tag": "05", "size": "narrow", "intro": "diario", "split": 2},
    {"slug": "lostinlamu", "titolo": "Lost in Lamu", "sottotitolo": "light painting",
     "tag": "06", "size": "big", "art": True, "intro": "lostinlamu", "no_closer": True,
     "no_download": True},
]

# introduzioni testuali per raccolta (punto 4 del brief).
INTRO_BLOCKS = {
    "isola": {
        "lede": "Camminare e basta",
        "desc": "Nessun appuntamento, nessuna scaletta: solo il grandangolo da 21mm "
                "e le stesse strade percorse a orari diversi<br>"
                "Gli asini ci sono sempre, a Lamu fanno tutto loro",
    },
    "rugby": {
        "lede": "Due squadre, sette allenamenti",
        "desc": "Martin e Daniela hanno allenato sulla sabbia due gruppi, "
                "i piccoli e i grandi<br>La squadra è nata",
    },
    "animaflow": {
        "lede": "Valeria ha portato la sua energia alle ragazze di Anidan",
        "desc": "Movimenti in cui il gesto diventa un flusso naturale",
    },
    "anidan": {
        "lede": "La casa, il nido",
        "desc": "Il miglior tempo passato sull'Isola",
    },
    "diario": {
        "lede": "Tutto il resto",
        "desc": "Le barche, le cene, il mare, i ricordi",
    },
    "lostinlamu": {
        "lede": "Disegnare con la luce",
        "desc": "Quattro LED diventano pennelli durante una lunga esposizione<br>"
                "Il gesto resta sospeso nel buio e trasforma un'esperienza personale "
                "in una traccia di luce<br>Since 2023",
        "rules": [
            "Osserva gli esempi qualche giorno prima",
            "Pensa a cosa ha significato per te l'esperienza a Lamu",
            "Usa i quattro LED dei guanti come pennelli di luce",
            "Disegna durante una lunga esposizione di 8 secondi",
            "Hai al massimo tre tentativi",
        ],
    },
}


def intro_html(key):
    b = INTRO_BLOCKS.get(key)
    if not b:
        return ""
    if not b.get("rules"):
        return f"""
<div class="coll-intro coll-intro-simple">
  <div class="lede">{b['lede']}</div>
  <p class="desc">{b['desc']}</p>
</div>
"""
    rules = "".join(
        f'<li><span class="num">{i:02d}</span><span class="txt">{r}</span></li>'
        for i, r in enumerate(b["rules"], 1)
    )
    return f"""
<div class="coll-intro">
  <div class="intro-left">
    <div class="lede">{b['lede']}</div>
    <p class="desc">{b['desc']}</p>
  </div>
  <ul class="rules-list">{rules}</ul>
</div>
"""

# override della copertina scelta automaticamente dal Best of
COVER_OVERRIDE = {
    "anidan": "LM106923.jpg",
    "isola": "LM105337.jpg",
}

GRUPPI_RUGBY = [("young", "Young"), ("boys", "Boys")]

# foto di gruppo finale scelte in fase di curatela (vedi BRIEF.md) — non e'
# detto siano le ultime in ordine di file, vanno chiuse esplicitamente li'
RUGBY_CLOSER = {"young": "LM105305.jpg", "boys": "LM106456.jpg"}

# "Best of" resta il nome tecnico (slug, CSV, cartella); in UI il racconto
# continua col titolo del progetto stesso, come fosse il libro finale.
BESTOF_TITOLO_UI = "Tales of Lamu 2026"
BESTOF_TAG_UI = "La Storia continua"

NAV_ITEMS = [{"slug": "bestof", "titolo": BESTOF_TITOLO_UI}] + [
    {"slug": s["slug"], "titolo": s["titolo"]} for s in SEZIONI
]


def load_json(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def head(title, depth=0, no_download=False):
    root = "../" * depth
    body_attr = ' data-no-download="1"' if no_download else ""
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="{root}favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,500;1,9..144,400;1,9..144,500&family=Archivo:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}css/style.css">
</head>
<body{body_attr}>
{gate_html(depth)}
<script>if(localStorage.getItem('tol_unlocked')==='1'){{document.getElementById('gate').classList.add('unlocked');}}</script>
"""


def gate_html(depth=0):
    root = "../" * depth
    return f"""<div id="gate" class="gate">
  <div class="gate-box">
    <div class="wordmark">Tales of Lamu <small>Archivio 2026</small></div>
    <p class="gate-lede">Il viaggio a Lamu, in foto<br>Riservato a chi c'era</p>
    <form id="gate-form" autocomplete="off">
      <input type="password" id="gate-input" placeholder="Password" autocomplete="off">
      <button type="submit" class="btn btn-primary">Entra &#8594;</button>
    </form>
    <p class="gate-error" id="gate-error">Password sbagliata, riprova</p>
    <div class="gate-credit">{credit_html(depth)}</div>
    <a class="gate-logo" href="https://www.anidanitalia.it" target="_blank" rel="noopener">
      <img src="{root}assets/logo-anidan.png" alt="Anidan"></a>
  </div>
</div>"""


def nav_overlay(depth=0):
    root = "../" * depth
    items = "\n".join(
        f'<li><a href="{root}{it["slug"]}/"><span class="num">{i+1:02d}</span>{it["titolo"]}</a></li>'
        for i, it in enumerate(NAV_ITEMS)
    )
    return f"""
<div class="nav-overlay">
  <button class="close-btn" data-menu-close>&times;</button>
  <ul class="nav-list">
    <li><a href="{root}">Home</a></li>
    {items}
  </ul>
</div>
"""


def site_header(depth=0):
    root = "../" * depth
    return f"""
<header class="site-header">
  <a class="wordmark" href="{root}">Tales of Lamu <small>Archivio 2026</small></a>
  <button class="menu-btn" data-menu-open><span class="bars"><span></span><span></span><span></span></span>Indice</button>
</header>
"""


# testo condiviso fra footer e schermata della password (vedi BRIEF.md, punto 3)
def credit_html(depth=0):
    return """Foto di Alessandro Montanari · <a href="https://www.instagram.com/atnomela" target="_blank" rel="noopener">@atnomela</a> · <a href="https://www.alessandromontanari.com" target="_blank" rel="noopener">www.alessandromontanari.com</a><br>
    Condividile per far conoscere Anidan · <a href="https://www.anidanitalia.it" target="_blank" rel="noopener">www.anidanitalia.it</a>"""


BOOK_URL = "https://www.anidanitalia.it/donations/libro-tales-of-lamu/"


def footer(depth=0):
    root = "../" * depth
    return f"""
<footer class="site-footer">
  <div class="footer-left">
    <div class="eyebrow">Lamu, Kenya · 10–29 agosto 2026</div>
    <div class="credit">{credit_html(depth)}</div>
    <a class="btn btn-primary footer-book" href="{BOOK_URL}" target="_blank" rel="noopener">Il libro Tales of Lamu &#8594;</a>
  </div>
  <a class="footer-logo" href="https://www.anidanitalia.it" target="_blank" rel="noopener">
    <img src="{root}assets/logo-anidan.png" alt="Anidan">
  </a>
</footer>
"""


def scripts(depth=0):
    root = "../" * depth
    return f'<script src="{root}js/site.js"></script>\n</body>\n</html>\n'


def figure_html(slug, p, depth):
    root = "../" * depth
    return f"""
    <figure data-full="{root}assets/web/{slug}/{p['file']}" data-alt="">
      <img src="{root}assets/thumbs/{slug}/{p['file']}" alt="" loading="lazy">
    </figure>"""


def closing_shot_html(slug, p, depth, art=False):
    """Ultima foto di un blocco (o di un gruppo), tirata fuori dal masonry
    a colonne e chiusa in grande — come i riquadri della home. E' mostrata
    molto piu' grande di una cella di griglia: usa la web (1476px), non il
    thumb (480px), altrimenti risulta sfocata."""
    root = "../" * depth
    cls = "closing-shot art" if art else "closing-shot"
    return f"""
<figure class="{cls}" data-full="{root}assets/web/{slug}/{p['file']}" data-alt="">
  <div class="frame"><img src="{root}assets/web/{slug}/{p['file']}" alt="" loading="lazy"></div>
</figure>"""


def grid_with_closer(slug, photos, depth, art=False, closer_file=None):
    """Griglia masonry con una foto staccata come chiusura grande: quella
    indicata da closer_file se data (foto di gruppo scelta in curatela),
    altrimenti l'ultima della lista."""
    if not photos:
        return ""
    if closer_file:
        last = next(p for p in photos if p["file"] == closer_file)
        body = [p for p in photos if p["file"] != closer_file]
    else:
        body, last = photos[:-1], photos[-1]
    figs = "".join(figure_html(slug, p, depth) for p in body)
    grid = f'<div class="grid">{figs}</div>' if body else ""
    return grid + closing_shot_html(slug, last, depth, art=art)


def build_homepage():
    manifest = load_json("manifest.json")
    bestof = load_json("bestof.json")

    tiles = []
    bo_cover = bestof[0]
    tiles.append(f"""
    <a class="tile big" href="bestof/">
      <img src="assets/web/{bo_cover['slug']}/{bo_cover['file']}" alt="">
      <div class="tile-info">
        <span class="tile-title">{BESTOF_TITOLO_UI}</span>
        <span class="tile-count">{len(bestof)} fotografie</span>
      </div>
    </a>""")

    covers = {}
    for r in bestof:
        covers.setdefault(r["slug"], r["file"])
    covers.update(COVER_OVERRIDE)

    for s in SEZIONI:
        photos = manifest[s["slug"]]
        n_pagina = sum(1 for p in photos if p.get("in_pagina", True))
        cover = covers.get(s["slug"], photos[0]["file"])
        classes = f"tile {s['size']}" + (" tile-art" if s.get("art") else "")
        tiles.append(f"""
    <a class="{classes}" href="{s['slug']}/">
      <img src="assets/web/{s['slug']}/{cover}" alt="">
      <div class="tile-info">
        <span class="tile-title">{s['titolo']}</span>
        <span class="tile-count">{n_pagina} fotografie</span>
      </div>
    </a>""")

    html = head("Tales of Lamu — Alessandro Montanari") + nav_overlay() + site_header() + f"""
<section class="hero">
  <div class="eyebrow">Lamu, Kenya · 10 – 29 agosto 2026</div>
  <h1>L'archivio del <em>viaggio</em></h1>
  <p>Sei raccolte<br>
  L'Isola, Scuola di Rugby, Anima Flow, Anidan, Diario, Lost in Lamu<br>
  Anidan, Rugby, Anima Flow e Diario si scaricano in blocco o singolarmente<br>
  L'Isola e Lost in Lamu restano solo da guardare</p>
</section>
<section class="mosaic">
  {"".join(tiles)}
</section>
""" + footer() + scripts()

    with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("scritto index.html")


def build_collection(slug):
    manifest = load_json("manifest.json")
    meta = next(s for s in SEZIONI if s["slug"] == slug)
    all_photos = manifest[slug]
    photos = [p for p in all_photos if p.get("in_pagina", True)]

    if meta.get("sub"):
        subnav = "".join(
            f'<a href="#{g}">{label}</a>' for g, label in GRUPPI_RUGBY
        )
        sections = ""
        for g, label in GRUPPI_RUGBY:
            grp = [p for p in photos if p.get("sottosezione") == g]
            sections += f"""
<div class="group-heading" id="{g}">
  <h2>{label}</h2>
  <span class="count">{len(grp)} fotografie</span>
</div>
{grid_with_closer(slug, grp, 1, closer_file=RUGBY_CLOSER.get(g))}
"""
        body = f'<div class="subnav">{subnav}</div>' + sections
    elif meta.get("no_closer"):
        subnav = ""
        figs = "".join(figure_html(slug, p, 1) for p in photos)
        body = f'<div class="grid">{figs}</div>'
    else:
        subnav = ""
        body = grid_with_closer(slug, photos, 1, art=meta.get("art", False))

    intro = intro_html(meta["intro"]) if meta.get("intro") else ""
    no_download = meta.get("no_download", False)
    split = meta.get("split")
    if no_download:
        actions = ""
    elif split:
        btns = "".join(
            f'<a class="btn btn-primary" href="../assets/zip/{slug}-{i}.zip" download>'
            f'Scarica parte {i}/{split} &#8595;</a>'
            for i in range(1, split + 1)
        )
        actions = f'\n  <div class="coll-actions coll-actions-split">{btns}</div>'
    else:
        actions = f"""
  <div class="coll-actions">
    <a class="btn btn-primary" href="../assets/zip/{slug}.zip" download>Scarica tutte &#8595;</a>
  </div>"""

    html = head(f"{meta['titolo']} — Tales of Lamu", depth=1, no_download=no_download) + nav_overlay(depth=1) + site_header(depth=1) + f"""
<div class="coll-header">
  <div>
    <a class="back-link" href="../">&#8592; Tutte le raccolte</a>
    <h1>{meta['titolo']}</h1>
    <p class="coll-meta">{meta['sottotitolo']} · {len(photos)} fotografie</p>
  </div>{actions}
</div>
{intro}
{body}
""" + footer(depth=1) + scripts(depth=1)

    outdir = os.path.join(DOCS, slug)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    zip_note = "non scaricabile" if no_download else f"{len(all_photos)} nello zip"
    print(f"scritto {slug}/index.html ({len(photos)} foto in pagina, {zip_note})")


def build_bestof():
    bestof = load_json("bestof.json")
    body_photos, last = bestof[:-1], bestof[-1]
    figs = []
    for r in body_photos:
        figs.append(f"""
    <figure data-full="../assets/web/{r['slug']}/{r['file']}" data-alt="{r['nota']}">
      <img src="../assets/thumbs/{r['slug']}/{r['file']}" alt="" loading="lazy">
    </figure>""")
    closer = closing_shot_html(last["slug"], last, 1)

    html = head(f"{BESTOF_TITOLO_UI} — Tales of Lamu", depth=1, no_download=True) + nav_overlay(depth=1) + site_header(depth=1) + f"""
<div class="coll-header">
  <div>
    <a class="back-link" href="../">&#8592; Tutte le raccolte</a>
    <h1>{BESTOF_TITOLO_UI}</h1>
    <p class="coll-meta">{BESTOF_TAG_UI} · {len(bestof)} fotografie</p>
  </div>
</div>
<div class="grid">
  {"".join(figs)}
</div>
{closer}
""" + footer(depth=1) + scripts(depth=1)

    outdir = os.path.join(DOCS, "bestof")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"scritto bestof/index.html ({len(bestof)} foto)")


def _write_zip(path, slug, photos):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_STORED) as z:
        for p in photos:
            src = os.path.join(DOCS, "assets", "web", slug, p["file"])
            z.write(src, p["file"])
    print(f"zip {os.path.basename(path)}: {len(photos)} file, {os.path.getsize(path)//1024//1024} MB")


def build_zips():
    """Best of e L'Isola non si scaricano (lavoro d'autore, come Lost in Lamu).
    Rugby/Anidan/Diario sono divisi in 2 parti: da interi superavano i 100MB,
    il limite hard di GitHub per singolo file (vedi BRIEF.md)."""
    manifest = load_json("manifest.json")
    zipdir = os.path.join(DOCS, "assets", "zip")
    os.makedirs(zipdir, exist_ok=True)

    for s in SEZIONI:
        slug = s["slug"]
        if s.get("no_download"):
            print(f"salto {slug}.zip (raccolta non scaricabile)")
            continue
        photos = manifest[slug]  # tutte le incluse, non solo in_pagina (rugby: 289)
        split = s.get("split")
        if split:
            n = len(photos)
            size = -(-n // split)  # ceil
            for i in range(split):
                chunk = photos[i * size : (i + 1) * size]
                path = os.path.join(zipdir, f"{slug}-{i+1}.zip")
                _write_zip(path, slug, chunk)
        else:
            path = os.path.join(zipdir, f"{slug}.zip")
            _write_zip(path, slug, photos)


if __name__ == "__main__":
    build_homepage()
    for s in SEZIONI:
        build_collection(s["slug"])
    build_bestof()
    build_zips()
