#!/usr/bin/env python3
"""Nuova sequenza Best of, costruita dopo la revisione delle 364 forti
e lo studio dei progetti #streetph e #talesoflamu.

Struttura:
  I   L'isola          1-12   arrivo, vicoli, street
  II  Il lavoro, il mare 13-23
  III L'istituzione    24-34   Anidan, scuola, ritratti
  IV  Il gioco         35-46   rugby, calcio, corpi
  V   La festa         47-56   BBQ, tamburi, danza (il colore prende il campo)
  VI  Partenza         57-58

Asini alle posizioni 1, 12, 23, 34, 45 (intervallo fisso di 11, mai accostati).
"""
import csv
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "_lavorazione", "selezione_foto.csv")
OUT = os.path.join(ROOT, "_lavorazione", "bestof_2026.csv")

# (numero, nota)  -- l'ordine della lista E' la sequenza
SEQUENZA = [
    # I. L'ISOLA
    (4528, "ASINO - nell'arco che si apre sul mare: l'isola in una foto"),
    (7077, "la bicicletta appoggiata al muro scritto - nessuno, solo forma"),
    (6662, "il corridoio buio che si apre sulla finestra di mare"),
    (5465, "la sagoma nera nel passaggio, la luce in fondo"),
    (7076, "la donna in arancio col bambino nel vicolo rosa"),
    (6275, "la bambina appoggiata al muro, il vicolo che fugge"),
    (5545, "la bambina in piedi in mezzo alla strada, piccola nel campo"),
    (7147, "gli uomini seduti lungo il muro, la figura che ci cammina sopra"),
    (5916, "l'uomo in kofia che attraversa, il mercato dietro"),
    (6459, "il muro ocra, le donne sui gradini, la frutta a terra"),
    (5344, "l'ombra della palma sulla sabbia, due figure minuscole"),
    # II. IL LAVORO, IL MARE
    (6777, "ASINO - la testa che esce dalla lamiera ondulata"),
    (7144, "l'uomo che porta il carico, la fatica dentro il vicolo"),
    (7063, "i banchi di scuola rotti ammucchiati nella stanza"),
    (6272, "le taniche gialle contro il cielo di tempesta"),
    (5909, "la rete metallica in primo piano, il motorino e i ragazzi dietro"),
    (6673, "gli uomini seduti sul cassone al porto"),
    (7078, "l'uomo che porta il blocco sulla testa"),
    (6919, "la vela del dhow vista dal basso, i pesci disegnati"),
    (4862, "il dhow sotto la diagonale della nostra vela"),
    (7085, "il tuffo dal dhow, il corpo teso contro le nuvole"),
    (4898, "la fila dei dhow sull'orizzonte"),
    # III. L'ISTITUZIONE
    (6800, "ASINO - inquadrato nella porta di pietra"),
    (6894, "la barchetta dipinta ferma nell'acqua, al crepuscolo"),
    (4780, "il bordo della vela e la linea del mangrovieto: quasi astratto"),
    (6912, "il canale fra le mangrovie, la vela in controluce, il cielo carico"),
    (7059, "il bambino solo sulla spiaggia, la citta' dietro"),
    (5904, "l'uomo seduto nell'apertura del muro bianco, l'albero, il vuoto"),
    (4921, "la ragazza sotto la mappa del Kenya dipinta sul muro"),
    (5901, "il dormitorio vuoto, le zanzariere annodate"),
    (7064, "l'aula quasi vuota, la luce dura, il bambino alla lavagna"),
    (5872, "CRAFT scritto sul muro, la freccia, le due figure in fondo"),
    (6926, "la maglietta gialla schiacciata nella fessura della porta"),
    (6991, "la ragazza all'angolo del muro, i piedi nudi sulla sabbia"),
    # IV. IL GIOCO
    (7152, "ASINO - a testa bassa sul lungomare"),
    (7180, "la ragazza con l'hijab bianco appoggiata al muro"),
    (4407, "il bambino seduto nella pozza di luce, il buio intorno"),
    (6943, "il piatto davanti al viso, incorniciato tra le due porte"),
    (6950, "il bambino che corre davanti alle arcate della scuola"),
    (6983, "i due pattinatori lungo il muro"),
    (4578, "il bambino disteso sulla sabbia, visto dall'alto"),
    (6680, "le due squadre schierate sotto la tettoia, il cielo grande"),
    (6690, "il cerchio di spalle, i numeri sulle maglie, la citta' in fondo"),
    (6770, "la corsa della squadra addosso alla macchina"),
    (6730, "il portiere dietro la rete: tutto il campo attraverso la maglia"),
    (4368, "ASINO - nel vicolo controluce, la testa che viene addosso"),
    (6784, "le donne coi cappelli di paglia che guardano la partita"),
    (6684, "la fila lunghissima dei ragazzi in maglia bianca sulla spiaggia"),
    (5694, "il campo lunghissimo, le figure minuscole, la sabbia e il cielo"),
    (6736, "il pubblico di spalle e l'asino fermo in mezzo al campo"),
    (6192, "la scivolata nella sabbia, lo spruzzo"),
    (5784, "il coach di spalle con i due palloni alzati"),
    (6215, "i palloni fermi tra i piedi nudi"),
    # V. LA FESTA
    (4734, "le mani alzate verso il coach, il cerchio che si chiude"),
    (6569, "la bambina che indica, il muro giallo"),
    (6519, "la carcassa sullo spiedo, il fuoco, il grembiule rosso"),
    (4483, "ASINO - a colori: l'uomo con la camicia a palme in mezzo al mercato"),
    (6885, "i due bambini fra i rami, appena visibili"),
    (6594, "le file di carne sulla griglia, dall'alto"),
    (6227, "il tamburino del Burundi in volo, la bacchetta alzata"),
    (6253, "i tamburi nell'ora blu, la folla, il mare in fondo"),
    (6350, "Anima Flow: la stanza intera aperta a stella"),
    (6158, "i corpi a terra in cerchio, il tappeto di stoffe"),
    # VI. PARTENZA
    (6838, "la testa del nuotatore nel mare vuoto, il banco di sabbia"),
    (7192, "la partenza: la strada mossa, il motorino che sparisce"),
]


SLUG = {"s": "isola", "r": "rugby", "f": "animaflow", "a": "anidan", "d": "diario"}


def e_colore(row, soglia=8):
    """Colore o bianco e nero, misurato sul thumb: media di (max-min) fra i canali."""
    p = os.path.join(ROOT, "docs", "assets", "thumbs",
                     SLUG[row["raccolta_codice"]], row["file"])
    im = Image.open(p).convert("RGB")
    im.thumbnail((120, 120))
    px = list(im.getdata())
    return sum(max(q) - min(q) for q in px) / len(px) > soglia


def main():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = {r["file"]: r for r in csv.DictReader(f)}
    by_num = {os.path.splitext(k)[0][-4:]: v for k, v in rows.items()}

    out = []
    problemi = []
    for i, (num, nota) in enumerate(SEQUENZA, 1):
        r = by_num.get(str(num))
        if r is None:
            problemi.append(f"{num} non trovato")
            continue
        if r["inclusa"].strip().upper() != "SI":
            problemi.append(f"{num} non inclusa")
        if r["raccolta_codice"] == "r" and r["in_pagina"] == "NO":
            problemi.append(f"{num} rugby fuori pagina")
        out.append({
            "ordine": i,
            "file": r["file"],
            "raccolta": r["raccolta"],
            "sottosezione": r["sottosezione"],
            "colore": "SI" if e_colore(r) else "",
            "asino": "SI" if nota.startswith("ASINO") else "",
            "nota": nota,
        })

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    print(f"scritto {OUT}")
    print(f"totale: {len(out)}")
    if problemi:
        print("PROBLEMI:", problemi)

    from collections import Counter
    print("\nper raccolta:")
    for k, v in Counter(r["raccolta"] for r in out).most_common():
        print(f"  {v:>3}  {k}")
    col = [r["ordine"] for r in out if r["colore"]]
    asi = [r["ordine"] for r in out if r["asino"]]
    print(f"\ncolore: {len(col)}/{len(out)} -> posizioni {col}")
    print(f"asini: posizioni {asi}")
    intervalli = [b - a for a, b in zip(asi, asi[1:])]
    print(f"intervalli fra asini: {intervalli}")


if __name__ == "__main__":
    main()
