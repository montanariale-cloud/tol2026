# Tales of Lamu — istruzioni per agenti

Questa repo è lavorata da più agenti (Claude Code, Codex, altri). Queste
istruzioni valgono per tutti, indipendentemente da chi la sta leggendo.

## Prima di fare qualunque cosa

Leggi `memoria/PROGETTO.md` per lo stato attuale del progetto. Se hai appena
finito un blocco di lavoro rilevante, aggiungi una riga a `memoria/LOG.md` e
aggiorna `memoria/PROGETTO.md` se lo stato è cambiato.

## Regola non negoziabile: il sito 2026 è congelato

`docs/` e `scripts/` nella root sono il sito pubblicato **Tales of Lamu 2026**
(https://montanariale-cloud.github.io/tol2026/), live, con password già
condivisa con 9 persone reali. **Non modificarli, non rigenerarli, non
toccarli** per nessun lavoro relativo ad altri progetti/capitoli. Se un
compito riguarda esplicitamente quel sito (bug riportato dall'utente, fix
richiesto), va bene — altrimenti restano intoccati. Dettagli in
`progetti/2026-viaggio/README.md`.

## Materiale grezzo: mai in git

Foto originali, RAW, export, contact sheet, CSV di curatela: tutto ciò che
vive dentro `progetti/*/` resta locale, escluso da `.gitignore`. Non forzare
mai `git add -f` su quel materiale. Solo i `README.md` di ogni sottocartella
di progetto sono tracciati.

Se un progetto arriva a produrre un output pubblico (un sito, un PDF, un
pacchetto editoriale), quell'output finito — non il materiale grezzo — può
diventare una nuova cartella tracciata in root, seguendo lo stesso pattern
usato per `docs/` + `scripts/` del 2026.

## Privacy e anonimato

Qualunque materiale riguardi i bambini di Anidan non deve mai includere nomi
o altri identificatori nei testi, nei nomi file pubblici o nei metadati
esposti pubblicamente. Regola valida per tutti i progetti futuri, non solo
per il 2026.

## Stile di lavoro con l'utente

- Un blocco alla volta, validato prima di passare al successivo — non
  anticipare fasi successive senza conferma.
- Se il brief/le istruzioni sono ambigue, chiedi prima di agire — non
  indovinare, soprattutto su operazioni distruttive o irreversibili
  (cancellazioni, push, force).
- L'utente è il fotografo/autore: le decisioni creative (selezione,
  sequenza, taglio) sono sue. L'agente propone, l'utente decide.
