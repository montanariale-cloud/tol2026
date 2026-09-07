#!/usr/bin/env python3
"""Applica la revisione rugby validata a selezione_foto.csv.

Aggiunge due colonne:
  sottosezione : 'young' / 'boys' per la raccolta rugby, vuota per le altre
  in_pagina    : 'SI'/'NO' -> se la foto compare nella pagina della raccolta.
                 Le rugby con NO restano inclusa=SI: entrano comunque nello zip
                 completo per Martin (289 foto) e la derivata resta generata.
"""
import csv
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "_lavorazione", "selezione_foto.csv")
PROP_PATH = os.path.join(ROOT, "_lavorazione", "rugby_proposta.csv")
BACKUP = CSV_PATH + ".bak"


def main():
    with open(PROP_PATH, newline="", encoding="utf-8") as f:
        prop = {r["file"]: r for r in csv.DictReader(f)}

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    for col in ("sottosezione", "in_pagina"):
        if col not in fieldnames:
            fieldnames.append(col)

    n_rugby = n_pagina = n_solo_zip = 0
    for r in rows:
        p = prop.get(r["file"])
        if p:  # foto della raccolta rugby
            n_rugby += 1
            r["sottosezione"] = p["gruppo"]
            r["in_pagina"] = p["tenere"]
            if p["tenere"] == "SI":
                n_pagina += 1
            else:
                n_solo_zip += 1
        else:
            r["sottosezione"] = ""
            # tutte le altre raccolte: in pagina se incluse
            r["in_pagina"] = "SI" if r["inclusa"].strip().upper() == "SI" else "NO"

    shutil.copy(CSV_PATH, BACKUP)
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f"backup: {BACKUP}")
    print(f"rugby: {n_rugby} foto | in pagina {n_pagina} | solo zip {n_solo_zip}")

    from collections import Counter
    c = Counter((r["raccolta"], r["sottosezione"]) for r in rows
                if r["in_pagina"] == "SI" and r["inclusa"].strip().upper() == "SI")
    print("\nfoto in pagina per sezione:")
    tot = 0
    for (racc, sub), n in sorted(c.items()):
        etichetta = f"{racc} / {sub}" if sub else racc
        print(f"  {n:>3}  {etichetta}")
        tot += n
    print(f"  {tot:>3}  TOTALE (senza Lost in Lamu)")


if __name__ == "__main__":
    main()
