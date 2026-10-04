# YappinaTor — WWY// Explorer / Cyber Ultra Orc Cow

## Cilj
YappinaTor je master research sistem; WWY// Explorer je njegov napredni cockpit za korisnike kojima trebaju signal, dokazi i dossier: brz za demo bez ključeva, spreman za live web research kada su Google CSE i OpenAI kredencijali podešeni.

## Dizajn
- **Pokret:** cyber command-center / brutalist research terminal.
- **Principi:** signal pre dekoracije, jasna hijerarhija, transparentan runtime, rezultat kao dosije.
- **Paleta:** gotovo crna podloga, kiselo-lime signalna boja, acid-cyan za mrežu i amber za upozorenja; boje razdvajaju stanje sistema, ne služe samo ornamentu.
- **Layout:** sidebar kao instrument panel, centralni query runway, rezultat u split-view sa source evidence rail-om.
- **Motivi:** scanline/noise grid, monogram `WWY//`, status chips i Orc Cow terminal marker.
- **Interakcija:** svaka akcija daje stanje (idle / scanning / demo / live / error); query ostaje u istoriji sesije; demo je eksplicitno označen.
- **Animacija:** kratki shimmer na scan state, pulse na live signal, bez beskonačnih agresivnih animacija i uz reduced-motion fallback.
- **Tipografija:** system sans za čitljivost + monospace za telemetry, status i komande.
- **Brand:** YappinaTor je glavni inteligentni sistem; WWY// Explorer je njegov research cockpit za ljude koji žele da vide signal, dokaze i sledeći potez; ličnost je hladna, radoznala, malo divlja.
- **Glas:** `CUT THROUGH THE NOISE.` / `Nema ključeva? Uđi u demo. Imaš ključeve? Otključaj mrežu.`
- **Wordmark:** `YAPPINATOR//` kao master wordmark, sa `WWY//` kao podmodulskim raster signalom.
- **Signature color:** Orc Lime `#c8ff3d`.

## Struktura
- `web_explorer.py`: Streamlit shell, settings, demo/live adapter, query history, agent telemetry i UI.
- `analysis_engine.py`: bounded Scout / Forensics / Skeptic / Synthesizer / Report Smith pipeline i Markdown report builder.
- `connectors.py`: connector registry, evidence envelope, pagination metadata i programming/computational query classification.
- `data_store.py`: SQLite WAL evidence ledger za research runs, sa indeksiranim recent history i `YAPPINATOR_DB_PATH` migracionom tačkom.
- Forensic depth: source quality ranking, contradiction radar, risk flags i query plan.
- Locale layer: Srpski default, Romani beta i English fallback za Đinđere Minđere.
- `security_lab.py`: defensive Kali posture sa secret scanom, module auditom, SQLite integrity checkom i connector health proverom.
- YappinaTor orchestration: Compute Core i Gateway agenti, Markdown/JSON/HTML report outputs, optional onion gateway status.
- Filmski access-lock: UI-only gate sa jasnom napomenom da ne predstavlja stvarnu autentikaciju.
- `.streamlit/config.toml`: dark theme i server podešavanja.
- `requirements.txt`: kompatibilne runtime zavisnosti.
- `README.md`: setup, bezbedno podešavanje ključeva, demo i live režim.
