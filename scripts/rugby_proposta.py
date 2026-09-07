#!/usr/bin/env python3
"""Proposta di scrematura + divisione Young/Boys per la raccolta rugby.

Genera _lavorazione/rugby_proposta.csv con, per ogni foto: gruppo, tenere, motivo.
Le liste sotto sono il risultato della revisione visiva dei 25 provini.
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "_lavorazione", "selezione_foto.csv")
OUT = os.path.join(ROOT, "_lavorazione", "rugby_proposta.csv")

# --- foto da TENERE (numero finale del file) ---
KEEP = {
    "S014": [4553, 4555, 4565, 4581, 4586, 4588, 4591, 4594, 4596, 4599, 4600, 4608,
             4613, 4623, 4624, 4627, 4628, 4631, 4634, 4642, 4660, 4662, 4669, 4678,
             4704, 4707, 4715, 4719, 4720, 4729, 4730, 4734],
    "S017": [4927, 4928, 4940, 4945, 4955, 4957, 4961, 4965, 4971, 4972, 4973, 4974,
             4975, 4980, 4983, 4984, 4990, 4991, 4993, 4995, 5017, 5030, 5044, 5062,
             5064, 5070, 5071, 5075, 5078, 5084, 5089, 5091, 5107, 5119, 5125, 5128,
             5130, 5132, 5138, 5140, 5153, 5157, 5163, 5165, 5176, 5183, 5190, 5208,
             5217, 5229, 5232, 5248, 5261, 5275, 5278, 5294, 5296, 5302],
    "S024": [5440, 5448],
    "S032": [5654, 5659, 5660, 5663, 5669, 5673, 5675, 5677, 5681, 5683, 5684, 5687,
             5688, 5692, 5694, 5697, 5700, 5702, 5705, 5707, 5709, 5710, 5717, 5727,
             5730, 5734, 5738, 5740, 5745, 5748, 5749, 5754, 5757, 5770, 5775, 5779,
             5784, 5792, 5794, 5796, 5798, 5804, 5807, 5820, 5821, 5833, 5836, 5840],
    "S035": [5981, 5986, 5994, 5999, 6000, 6006, 6013, 6018, 6019, 6023, 6027, 6032,
             6054, 6057, 6061, 6066, 6165, 6172, 6185, 6188, 6192, 6198, 6199, 6205,
             6210, 6215],
    "S040": [6326, 6330, 6409, 6414, 6419],
    "S041": [6428, 6433, 6439, 6446, 6456],
}

# --- motivo dello scarto, per numero ---
MOTIVI = {
    # S014
    4554: "doppione di 4553", 4561: "campo lungo vuoto, momento debole",
    4571: "campo lungo ripetitivo", 4572: "campo lungo ripetitivo",
    4574: "momento debole", 4580: "simile a 4581, meno forte",
    4582: "simile a 4581", 4583: "momento debole",
    4601: "doppione di 4600",
    4730: "doppione meno efficace di 4734 (scelta di Alessandro)",
    5302: "sostituita da 5305 come foto di gruppo Young",
    4614: "doppione di 4613", 4618: "stessa inquadratura di 4613",
    4620: "doppione di 4618", 4638: "momento debole",
    4639: "simile a 4642, meno forte", 4648: "momento debole",
    4665: "campo lungo ripetitivo", 4677: "campo lungo ripetitivo",
    4679: "non e' rugby, sta meglio nel diario", 4682: "momento debole",
    4689: "simile a 4707", 4691: "simile a 4642",
    4700: "campo lungo ripetitivo", 4706: "di spalle, momento debole",
    4709: "simile a 4707, meno forte", 4723: "doppione del cerchio (4715/4719)",
    4725: "doppione del cerchio",
    # S017
    4938: "campo lungo ripetitivo", 4944: "campo lungo, momento debole",
    4954: "simile a 4955", 4958: "gruppo statico, momento debole",
    4959: "campo lungo ripetitivo", 4960: "momento debole",
    4966: "simile a 4971", 4977: "doppione flessioni (4984)",
    4979: "momento debole", 4981: "doppione flessioni", 4982: "doppione flessioni",
    4986: "doppione a colori di 4984", 4989: "momento debole",
    4999: "gruppo statico", 5052: "campo lungo ripetitivo",
    5065: "simile a 5071", 5080: "momento debole", 5106: "simile a 5107, meno forte",
    5121: "doppione del cerchio", 5131: "doppione di 5130",
    5148: "campo lungo ripetitivo", 5152: "momento debole",
    5162: "doppione di 5163", 5164: "momento debole",
    5167: "simile a 5168", 5168: "simile a 5167", 5170: "campo lungo ripetitivo",
    5173: "gruppo statico", 5177: "doppione della serie palla in mano (tenute 5190/5217)",
    5185: "doppione della serie palla in mano (5190)",
    5187: "doppione della serie palla in mano", 5193: "simile a 5194",
    5194: "simile a 5193", 5199: "momento debole", 5201: "simile a 5232",
    5213: "doppione della serie palla in mano", 5228: "simile a 5229",
    5265: "gruppo statico", 5276: "doppione b/n di 5275",
    5283: "momento debole", 5286: "momento debole", 5289: "simile a 5292",
    5292: "simile a 5294, meno forte", 5305: "doppione della foto di gruppo (5302)",
    # S024
    5439: "doppione di 5440", 5442: "doppione di 5440",
    5446: "stessa scena, piu' debole", 5451: "doppione di 5448",
    # S032
    5651: "campo lungo ripetitivo", 5653: "doppione di 5654",
    5656: "doppione di 5654", 5679: "campo lungo ripetitivo",
    5685: "doppione della corsa (5688)", 5689: "doppione della corsa",
    5690: "doppione della corsa", 5699: "doppione di 5697",
    5706: "doppione del sollevamento (5707)", 5724: "doppione del cerchio",
    5731: "doppione di 5730", 5737: "campo lungo ripetitivo",
    5741: "doppione di 5740", 5756: "simile a 5757, meno forte",
    5759: "campo lungo ripetitivo", 5760: "campo lungo ripetitivo",
    5778: "momento debole", 5788: "doppione dell'azione controluce",
    5799: "momento debole", 5828: "doppione del cerchio", 5671: "doppione di 5669",
    # S035
    5988: "di spalle, momento debole", 5993: "simile a 6013",
    6002: "doppione delle flessioni (6000)", 6012: "gruppo statico",
    6014: "gruppo statico", 6020: "doppione di 6023",
    6058: "doppione del sollevamento (6057)", 6059: "doppione a colori di 6058",
    6169: "campo lungo, momento debole", 6183: "doppione delle flessioni",
    6193: "campo lungo ripetitivo", 6204: "doppione dell'azione (6205)",
    # S040
    6327: "momento debole", 6392: "momento debole", 6416: "campo lungo ripetitivo",
    # S041
    6427: "campo lungo ripetitivo", 6436: "campo lungo ripetitivo",
}

# --- gruppo: divisione confermata da Alessandro ---
# Young: dall'inizio fino a 5451 (fine provino 14) = S014 + S017 + S024
# Boys:  da 5651 in poi = S032 + S035 + S040 + S041 (i piccoli fanno da contorno)
# Foto di gruppo finale: Young -> S017 (5302), Boys -> S041 (6456)
GRUPPO_PER_SESSIONE = {
    "S014": "young",
    "S017": "young",
    "S024": "young",
    "S032": "boys",
    "S035": "boys",
    "S040": "boys",
    "S041": "boys",
}

INCERTE = set()

# --- revisione di Alessandro sulla proposta ---
# foto ripescate dagli scarti
RIENTRI = [4609, 4618, 4638, 4639, 4648, 4679, 4691, 4723, 5080, 5162, 5185, 5283,
           5292,
           5656, 5671, 5685, 5724, 5741, 5759, 5760, 5778, 5799, 5828, 6416,
           5305]  # 5305 e' la foto di gruppo finale degli Young
# foto tolte dalle tenute
RIMOSSE = [4730,   # doppione meno efficace di 4734
           5302]   # sostituita da 5305 come foto di gruppo Young
# eccezioni alla divisione per sessione
GRUPPO_OVERRIDE = {6018: "young"}


def gruppo_di(sessione, num):
    if num in GRUPPO_OVERRIDE:
        return GRUPPO_OVERRIDE[num]
    return GRUPPO_PER_SESSIONE.get(sessione, "?")


def main():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f)
                if r["raccolta_codice"] == "r" and r["inclusa"].strip().upper() == "SI"]
    rows.sort(key=lambda r: (r["scatto"], r["file"]))

    keep_all = {n for lst in KEEP.values() for n in lst}
    keep_all |= set(RIENTRI)
    keep_all -= set(RIMOSSE)

    out_rows = []
    n_keep = 0
    for r in rows:
        num = int(os.path.splitext(r["file"])[0][-4:])
        tenere = "SI" if num in keep_all else "NO"
        if tenere == "SI":
            n_keep += 1
        out_rows.append({
            "file": r["file"],
            "sessione": r["sessione"],
            "ora": r["scatto"].split()[-1][:5],
            "forte": r["forte"],
            "gruppo": gruppo_di(r["sessione"], num),
            "tenere": tenere,
            "eta_incerta": "SI" if num in INCERTE else "",
            "motivo_scarto": MOTIVI.get(num, "") if tenere == "NO" else "",
        })

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    from collections import Counter
    print(f"scritto {OUT}")
    print(f"totale {len(out_rows)} | tenere SI {n_keep} | tenere NO {len(out_rows)-n_keep}")
    c = Counter((r["gruppo"], r["tenere"]) for r in out_rows)
    for g in ("young", "boys", "?"):
        print(f"  {g:6} tenute {c[(g,'SI')]:>3}  scartate {c[(g,'NO')]:>3}")
    manca = [r["file"] for r in out_rows if r["tenere"] == "NO" and not r["motivo_scarto"]]
    if manca:
        print(f"ATTENZIONE: {len(manca)} scarti senza motivo: {manca}")


if __name__ == "__main__":
    main()
