#!/usr/bin/env python3
"""Riclassificazione foto errate individuata durante il controllo di Alessandro
sulle derivate generate (7 sett 2026). Aggiorna selezione_foto.csv e sposta
i file gia' generati in docs/assets/web|thumbs/<sezione>/ nella sezione corretta.
"""
import csv
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "_lavorazione", "selezione_foto.csv")
OUT_WEB = os.path.join(ROOT, "docs", "assets", "web")
OUT_THUMB = os.path.join(ROOT, "docs", "assets", "thumbs")

RACCOLTA_BY_CODICE = {
    "s": "1. L'Isola - Street Photography",
    "r": "2. Scuola di Rugby con Martin",
    "f": "3. Anima Flow con Valeria De Chiara",
    "a": "4. Anidan e i suoi ragazzi",
    "d": "5. Diario delle vacanze",
}
SLUG_BY_CODICE = {"s": "isola", "r": "rugby", "f": "animaflow", "a": "anidan", "d": "diario"}

# (numeri LM..., codice_destinazione)
MOVES = [
    ([104361], "d"),
    ([104535, 104540, 104542], "s"),
    ([105439, 105440, 105442, 105446, 105448, 105451, 106392], "r"),
    ([106551, 106556], "d"),
    ([106578, 106582, 106599, 106615, 106618, 106619], "a"),
    ([104848, 106919, 107084, 107085, 107086, 107091, 105332, 105337, 105344, 105362], "s"),
    (
        [105012, 106470, 106471, 106475, 106477, 106478, 106481, 106484, 106487, 106488,
         106491, 106495, 106501, 106502, 106504, 106506, 106512, 106514, 106517, 106519,
         106521, 106536, 106553, 106554, 106562, 106586, 106591, 106594, 106596, 106600,
         106602, 106607, 106628, 106635, 106641, 106647, 106650, 106655, 106657, 106658,
         106659, 106661],
        "a",
    ),
    (
        [104377, 104470, 105316, 105548, 105549, 105952, 106296, 106299, 106309, 106466,
         107141, 105518, 105521, 105522, 105524, 105525, 105527, 105532, 105533, 105536,
         105537, 105540, 105541, 105542, 105543, 106797, 106862, 106864, 107079],
        "d",
    ),
    ([105617, 106285, 106781, 106784, 107100, 107101, 107180, 106703, 106715, 106726, 106736], "a"),
    ([104564, 104578, 104931, 104949, 104950, 104953, 105808, 106004, 106011, 106067], "a"),
    ([105311, 105746, 106034], "d"),
]


def main():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    by_num = {}
    for r in rows:
        base = os.path.splitext(r["file"])[0]
        by_num[base] = r

    changes = []
    for numbers, target_codice in MOVES:
        for n in numbers:
            key = f"LM{n}"
            row = by_num.get(key)
            if row is None:
                print(f"ATTENZIONE: {key} non trovato in CSV, salto")
                continue
            old_codice = row["raccolta_codice"]
            if old_codice == target_codice:
                print(f"  {key}: gia' {target_codice}, nessun cambiamento")
                continue
            row["raccolta_codice"] = target_codice
            row["raccolta"] = RACCOLTA_BY_CODICE[target_codice]
            changes.append((row["file"], old_codice, target_codice))

    print(f"\nTotale foto riclassificate: {len(changes)}")

    # riscrivi il CSV
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV aggiornato: {CSV_PATH}")

    # sposta i file derivati gia' generati
    moved, missing = 0, 0
    for fname, old_codice, new_codice in changes:
        old_slug = SLUG_BY_CODICE[old_codice]
        new_slug = SLUG_BY_CODICE[new_codice]
        for base_dir in (OUT_WEB, OUT_THUMB):
            src = os.path.join(base_dir, old_slug, fname)
            dst = os.path.join(base_dir, new_slug, fname)
            if os.path.exists(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(src, dst)
                moved += 1
            else:
                print(f"MANCA derivata: {src}")
                missing += 1

    print(f"File derivati spostati: {moved}, mancanti: {missing}")


if __name__ == "__main__":
    main()
