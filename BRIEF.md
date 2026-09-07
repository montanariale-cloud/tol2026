# TOL 2026 — Brief di progetto

Documento di consegna. Contiene tutte le decisioni prese nella fase di curatela.
Chi costruisce il sito parte da qui: non serve rifare analisi né riguardare le foto.

---

## 1. Cos'è

Sito statico per condividere e far scaricare le foto del viaggio a Lamu (10–29 agosto 2026)
ai nove compagni di viaggio e ad Anidan. Selezione larga, non da mostra: è un archivio
consultabile, con dentro una vetrina d'autore.

- **Repo**: https://github.com/montanariale-cloud/tol2026 (pubblica)
- **URL previsto**: https://montanariale-cloud.github.io/tol2026
- **Autore**: Alessandro Montanari
- **Sorgenti**: `Foto/` (1023 JPG), `Lost in Lamu/` (32 JPG quadrati 1476px)

---

## 2. Struttura del sito

Sei raccolte più il Best of.

| # | Sezione | Foto | Note |
|---|---------|------|------|
| 1 | L'Isola — Street Photography | 104 | "L'Isola" e la raccolta street sono la stessa cosa — **non scaricabile**, lavoro d'autore |
| 2 | Scuola di Rugby con Martin | 199 in pagina (289 nello zip, diviso in 2 parti) | due sottosezioni: **Young** 105 (S014, S017, S024) e **Boys** 94 (S032, S035, S040, S041) |
| 3 | Anima Flow con Valeria De Chiara | 51 | tre giorni di lavoro, danza |
| 4 | Anidan e i suoi ragazzi | 299 (zip diviso in 2 parti) | include scuola pubblica e centro autismo (progetti paralleli Anidan) |
| 5 | Diario delle vacanze | 216 (zip diviso in 2 parti) | |
| 6 | Lost in Lamu | 32 | light painting, serie pluriennale 2023–2026 — **non scaricabile** |
| — | **Best of** (UI: "Tales of Lamu 2026") | 65 | sequenza d'autore, attinge a tutte le raccolte **tranne Lost in Lamu** — **non scaricabile** |

Il numero totale non è più mostrato in homepage (cambia troppo spesso con gli aggiustamenti):
991 foto incluse (959 in `Foto/` + 32 Lost in Lamu). **Non scaricabili**: L'Isola, Lost in Lamu,
Best of — sono il lavoro d'autore. Scaricabili in blocco o singolarmente: Anidan, Rugby,
Anima Flow, Diario — sono al servizio di chi le userà (Anidan, Martin, Valeria) o il ricordo
condiviso dei nove compagni.

Numeri aggiornati il 7/9/2026 dopo controllo di Alessandro sulle derivate: 124 foto erano
classificate nella raccolta sbagliata (vedi `scripts/reclassify_20260907.py`), corrette in
`selezione_foto.csv`.

**Rugby, revisione del 7/9/2026.** La raccolta è divisa in due sottosezioni, ciascuna con la
propria sequenza e la propria foto di gruppo finale:
- **Young** — 105 foto, sessioni S014 S017 S024 (12–15 agosto), chiude con `LM105305.jpg`
- **Boys** — 94 foto, sessioni S032 S035 S040 S041 (17–20 agosto), chiude con `LM106456.jpg`
  (nelle giornate dei Boys i bambini piccoli compaiono come contorno: restano nei Boys)
Unica eccezione alla divisione per sessione: `LM106018.jpg`, che sta negli Young.

90 foto rugby non vanno in pagina ma **restano nello zip completo per Martin (289)**:
`inclusa=SI`, `in_pagina=NO`. Le due nuove colonne di `selezione_foto.csv` sono
`sottosezione` (young/boys, vuota per le altre raccolte) e `in_pagina` (SI/NO).
Decisioni foto per foto con motivazione in `_lavorazione/rugby_proposta.csv`.

---

## 3. Regole non negoziabili

- **Anonimato Anidan**: nessun nome associato a ragazzi e ragazze dell'orfanotrofio,
  in nessun punto — non nelle didascalie, non nei nomi file, non nei metadati, non negli alt.
  I nomi si usano solo per i nove del gruppo di viaggio.
  L'autorizzazione all'uso delle foto da parte di Anidan c'è: il punto è chiuso.
- **Download per Martin Castrogiovanni**: deve poter scaricare in blocco **tutte le 289 foto
  selezionate della raccolta rugby** — comprese le 90 che non vanno in pagina. Sceglierà lui cosa veicolare sui canali
  Castro Academy (@castrorugbyacademy). Serve uno zip della raccolta, non una selezione ridotta.
- **Gli asini sono il fil rouge dell'isola.** Nella sequenza del Best of compaiono
  a intervalli regolari, mai raggruppati — ma **l'intervallo non deve essere matematicamente
  fisso**: Alessandro ha esplicitamente rilasciato quel vincolo (8/9/2026) quando l'aggiunta
  di nuove foto lo avrebbe reso troppo rigido da mantenere. Posizioni attuali: 1, 12, 23, 35,
  46, 57 (intervalli 11-11-12-11-11). Ce n'è un settimo "nascosto" fra questi (l'asino fermo
  in mezzo al campo durante la partita): è voluto.
- **Ordine di Lost in Lamu**: la sequenza è decisa, sta in `_lavorazione/lostinlamu_ordine.txt`.
  Non ordinare alfabeticamente né per data.
- **Lost in Lamu non entra nel Best of.** È un capitolo a sé: light painting, astrazione pura,
  serie pluriennale. Decisione di Alessandro, confermata il 7/9/2026.
- **Best of**: l'ordine in `_lavorazione/bestof_2026.csv` è una sequenza, non una classifica.
  Va rispettato.

---

## 4. Dati tecnici delle immagini

- Fotocamera: Leica M10.
- Obiettivi reali: **Voigtländer 21mm f/4** su quasi tutto; **Leica 35mm a f/8** per Lost in Lamu;
  **Leica 90mm f/2.8** su alcune foto della partita di calcio (sessione S048, da identificare).
- **L'EXIF dei JPG riporta erroneamente "Summicron-M 35" su tutto.** Se si mostrano i dati
  di scatto sul sito, usare la colonna `obiettivo_reale` del CSV, non l'EXIF.
- Date di scatto: 10–28 agosto 2026. Le date di modifica file sono l'export da Lightroom, inutili.
- Orientamento: 905 orizzontali, 118 verticali. Il layout deve reggere entrambi.

---

## 5. File di lavoro (cartella `_lavorazione/`)

| File | Contenuto |
|------|-----------|
| `selezione_foto.csv` | una riga per foto: sessione, data/ora scatto, obiettivo reale, raccolta, flag "forte", inclusa sì/no, **sottosezione** (young/boys per il rugby), **in_pagina** sì/no |
| `bestof_2026.csv` | **i 65 del Best of in sequenza**, con nota, flag colore e flag asino — fonte di verità |
| `rugby_proposta.csv` | decisione foto per foto sul rugby: gruppo, tenere sì/no, motivo dello scarto |
| `bestof_50.csv` | *superata* — la prima proposta da 50, tenuta solo come storico |
| `BESTOF_50_sequenza.jpg` | *superato* — provino della vecchia sequenza |
| `sheets_lavoro/` | provini di lavoro: rugby, proposte, sequenza Best of (`BESTOF2026_*.jpg`) |
| `lostinlamu_ordine.txt` | ordine di pubblicazione delle 32 di Lost in Lamu |
| `mappatura_sessioni.csv` | le 71 sessioni di scatto con orari e contenuto |
| `exif_tol2026.csv` | EXIF grezzo di tutte le 1023 |
| `sheets_full/` | provini di tutte le foto (43 fogli) |
| `sheets_forti/` | provini delle 364 foto marcate forti (16 fogli) |

**Fonte di verità: `selezione_foto.csv`.** 64 foto sono marcate `inclusa=NO`: 45 scarti
(raffiche identiche, mosse, doppioni) più le 18 light painting dentro `Foto/` (escluse
perché valgono i file rifiniti in `Lost in Lamu/`) più `LM106860.jpg` (esclusa l'8/9/2026,
vedi sezione 8).

---

## 6. Build — cosa resta da fare

1. ~~Derivate.~~ **Fatte il 7/9/2026** (`scripts/generate_derivatives.py`).
   Nota: il brief chiedeva 2048px lato lungo, ma i file in `Foto/` sono già export a
   **1476px** lato lungo (25 cm a 150 ppi) e non esistono originali a risoluzione piena
   in questa cartella: era un refuso. Le derivate web sono quindi a 1476px, solo
   ricompresse a qualità 90 (da ~1 MB a ~400 KB l'una), più i thumb a 480px qualità 80.
   In `docs/assets/web/<sezione>/` e `docs/assets/thumbs/<sezione>/`: 992 + 992 file, **432 MB**.
   Lost in Lamu è copiata così com'è, con il solo thumb generato.
2. **Sito**: indice, sei pagine raccolta, pagina Best of, lightbox, download singolo e zip
   per raccolta. Griglia che regge orizzontali e verticali senza tagliare.
3. **Accesso**: Alessandro vuole una password all'ingresso, come ha già fatto per un sito
   di foto di matrimonio. Va implementata come gate client-side (JS) + `noindex`.
   **Da sapere e da dirgli, non da nascondere**: con repo pubblica su GitHub Pages
   quella password è una cortesia, non una protezione. Le immagini restano raggiungibili
   per URL diretto e il repo è navigabile da chiunque. Va bene se lo scopo è "non voglio
   che ci capiti dentro un estraneo per caso". Se invece serve protezione vera,
   le due strade sono Cloudflare Pages + Access (gratis) o l'hosting Aruba con .htaccess:
   in entrambi i casi la build non cambia, cambia solo il deploy.
4. **Testi**: le raccolte non hanno ancora un'introduzione. Da scrivere.
5. ~~Rivedere il Best of.~~ **Fatto il 7/9/2026** — vedi sezione 8.

---

## 7. Come lavora Alessandro

Un blocco alla volta, validato, prima di passare al successivo. Niente grandi consegne
monolitiche. Il punto debole dichiarato è l'ultimo miglio: chiudere e pubblicare.
Spingere lì.

---

## 8. Il Best of — impianto della sequenza (7/9/2026)

**65 foto** (63 originarie + 2 aggiunte l'8/9/2026, vedi in fondo). Fonte di verità:
`_lavorazione/bestof_2026.csv`. Provino (non aggiornato alle ultime 2): `sheets_lavoro/BESTOF2026_*.jpg`.

**Criterio: portfolio puro, non memoria.** La memoria condivisa del viaggio sta nel Diario;
il Best of è vetrina d'autore e regge il confronto con #streetph. Fuori quindi i ritratti
di gruppo, le foto dei nove compagni, il ricordo caldo ma ordinario.

**Riferimento di stile**: i progetti pubblicati su alessandromontanari.com — #streetph
(76 foto, tutte in bianco e nero) e #talesoflamu. Ricorrono: la figura piccola dentro un campo
grafico grande, la luce e l'ombra come struttura, le cornici dentro la cornice (porte, finestre,
reti, specchi), i neri profondi, l'ironia per accostamento, i ritratti a sguardo diretto isolati
dal contesto. Costruisce per capitoli titolati e **chiude in sottrazione** (Tales of Lamu finisce
su un mare vuoto). Nel suo lavoro il colore non è mai sparso: è un capitolo dichiarato.

**Il colore qui è la tesi della sequenza.** Decisione di Alessandro: il bianco e nero è la sua
storia, il colore è dove si trova oggi — la sequenza deve rappresentare l'evoluzione, senza
cadenze fisse. Quindi: 14 foto a colori su 63, rade e occasionali nella prima metà
(pos. 5, 10, 15, 23, 24, 29, 32), poi un blocco denso nel movimento finale della festa
(54, 55, 56, 58, 59, 60, 61), e ritorno al bianco e nero per le due foto di chiusura.
Il colore non decora: cresce fino a prendersi il campo, poi lascia.

**I sei movimenti**, scanditi dagli asini:

| Movimento | Pos. |
|---|---|
| I — L'isola (vicoli, muri, street) | 1–11 |
| II — Il lavoro e il mare | 12–22 |
| III — L'istituzione (Anidan, scuola, ritratti) | 23–33 |
| IV — Il gioco (calcio e rugby) | 34–52 |
| V — La festa (BBQ, tamburi, danza) | 53–61 |
| VI — Partenza | 62–63 |

Chiude su `LM106838.jpg` (il nuotatore nel mare vuoto) e `LM107192.jpg` (la strada mossa,
il motorino che sparisce).

**Aggiornamento 8/9/2026.** Tre foto passate da Diario a L'Isola (`LM106885.jpg`,
`LM106894.jpg`, `LM106912.jpg`) ed entrate anche nel Best of — la sequenza sale a 65.
`LM106912.jpg` (canale fra le mangrovie) è entrata vicino a `LM104780.jpg` nella sezione
"il lavoro e il mare"; `LM106885.jpg` (i due bambini fra i rami) è finita dopo l'ultimo
asino, in coda alla sezione "la festa", proprio per non rompere l'intervallo fra gli
asini precedenti. Una quarta foto, `LM106860.jpg`, è stata esclusa del tutto dal sito
(`inclusa=NO`), non solo tolta da Diario.

---
