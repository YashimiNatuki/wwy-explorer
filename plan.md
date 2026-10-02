# WWY Explorer — Cyber Ultra Orc Cow

## Cilj
Pretvoriti sirovi Streamlit Web Explorer u samostalan research cockpit za napredne korisnike: brz za demo bez ključeva, spreman za live web research kada su Google CSE i OpenAI kredencijali podešeni.

## Dizajn
- **Pokret:** cyber command-center / brutalist research terminal.
- **Principi:** signal pre dekoracije, jasna hijerarhija, transparentan runtime, rezultat kao dosije.
- **Paleta:** gotovo crna podloga, kiselo-lime signalna boja, acid-cyan za mrežu i amber za upozorenja; boje razdvajaju stanje sistema, ne služe samo ornamentu.
- **Layout:** sidebar kao instrument panel, centralni query runway, rezultat u split-view sa source evidence rail-om.
- **Motivi:** scanline/noise grid, monogram `WWY//`, status chips i Orc Cow terminal marker.
- **Interakcija:** svaka akcija daje stanje (idle / scanning / demo / live / error); query ostaje u istoriji sesije; demo je eksplicitno označen.
- **Animacija:** kratki shimmer na scan state, pulse na live signal, bez beskonačnih agresivnih animacija i uz reduced-motion fallback.
- **Tipografija:** system sans za čitljivost + monospace za telemetry, status i komande.
- **Brand:** WWY je research cockpit za ljude koji žele da vide signal, dokaze i sledeći potez; ličnost je hladna, radoznala, malo divlja.
- **Glas:** `CUT THROUGH THE NOISE.` / `Nema ključeva? Uđi u demo. Imaš ključeve? Otključaj mrežu.`
- **Wordmark:** `WWY//` kao tri kratka raster signala sa lomljenom kosom crtom.
- **Signature color:** Orc Lime `#c8ff3d`.

## Struktura
- `web_explorer.py`: Streamlit shell, settings, demo/live adapter, query history, agent telemetry i UI.
- `analysis_engine.py`: bounded Scout / Forensics / Skeptic / Synthesizer / Report Smith pipeline i Markdown report builder.
- Forensic depth: source quality ranking, contradiction radar, risk flags i query plan.
- Locale layer: Crnogorski default, Romani beta i English fallback za Đinđere Minđere.
- `.streamlit/config.toml`: dark theme i server podešavanja.
- `requirements.txt`: kompatibilne runtime zavisnosti.
- `README.md`: setup, bezbedno podešavanje ključeva, demo i live režim.
