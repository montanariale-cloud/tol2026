# 2026 — Viaggio a Lamu

Materiale di lavoro del viaggio fotografico a Lamu, Kenya (10–29 agosto 2026),
da cui è nato il sito pubblicato **Tales of Lamu 2026** (`docs/` + `scripts/`
nella root della repo — vedi nota importante sotto).

## Contenuto

- `Foto/` — export originali del viaggio (lato lungo 25cm, 150 ppi)
- `_lavorazione/` — CSV di curatela, contact sheet, dati intermedi del sito
  - `selezione_foto.csv` — fonte di verità per raccolta/inclusione/sottosezione
  - `bestof_2026.csv` — sequenza finale della selezione d'autore
  - `site_data/` — manifest.json e bestof.json generati per il sito
- `0. Info Tales of Lamu 2026.pdf` — brief originale del progetto
- `BRIEF.md` — log delle decisioni prese durante costruzione del sito 2026
  (curatela, design, password, deploy). Superato dal sistema di memoria
  generale in `memoria/`, ma tenuto qui come archivio storico del progetto.

## ⚠️ Importante: il sito 2026 è congelato

Il sito pubblicato (root `docs/` + `scripts/`) è **live**, con password già
condivisa con 9 persone. Non va mai rigenerato o modificato in occasione di
lavori futuri su altri progetti/capitoli di Tales of Lamu.

Gli script in `scripts/` (root) referenziano questa cartella con path
relativi alla vecchia posizione in root (`_lavorazione/`, `Lost in Lamu/`).
Sono stati lasciati invariati di proposito. Se in futuro fosse necessario
rigenerare qualcosa del sito 2026, occorre prima ripristinare temporaneamente
quei path (o aggiornare le costanti negli script) — non farlo per errore.
