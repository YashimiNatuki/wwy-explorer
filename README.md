# WWY// Explorer — Cyber Ultra Orc Cow

WWY// Explorer je research cockpit za napredne korisnike: uneseš pitanje, dobiješ sažet signal, trag izvora i dossier koji možeš da sačuvaš. Interfejs radi odmah u **Demo** režimu, bez ključeva, a prelazi u live web research kada su Google CSE i OpenAI promenljive podešene.

## Pokretanje

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run web_explorer.py
```

Otvori `http://localhost:8501`.

## Demo i live režim

Demo režim je nameran: prikazuje kompletan tok cockpit-a i jasno označava da izvori nisu live-pretraženi. Za live režim postavi promenljive u shell-u ili Streamlit secrets fajlu; ključevi se ne čuvaju u source kodu:

```bash
export GOOGLE_API_KEY="..."
export GOOGLE_CSE_ID="..."
export OPENAI_API_KEY="..."
export OPENAI_API_BASE="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-3.5-turbo-16k"
```

U sidebar-u izaberi `Auto` ili `Live`. Ako provider sloj nije dostupan, UI ostaje živ i vraća čitljiv connector error umesto da padne cela aplikacija.

## Šta je unapređeno

Nova verzija ima WWY// command-center shell, Cyber Ultra Orc Cow branding, telemetry bar, demo/live status, quick probes, session history, depth switch, source evidence kartice, dossier download i reset. Originalni LangChain WebResearchRetriever tok ostaje kao live adapter, ali više nema hardkodovanih provider vrednosti.

## Agent mesh i deep analysis

Posle svakog research pass-a, `analysis_engine.py` pokreće pet transparentnih, bounded uloga nad istim result envelope-om: **Scout**, **Forensics**, **Skeptic**, **Synthesizer** i **Report Smith**. UI prikazuje svaku fazu, njen output, confidence telemetry i uncertainty boundary. U Demo režimu agenti su deterministički i rade nad jasno označenim simuliranim signalom; u Live režimu rade nad stvarno vraćenim odgovorom i source records.

`DOWNLOAD AUTO REPORT` generiše Markdown dossier sa executive signalom, radnom tezom, kompletnim agent trace-om, evidence nodovima i sledećim potezima. Ovo je namerno inspectable: nema skrivenih background agenata i nema tvrdnje da je demo signal pretražio web.

## Maksimalni research režim

Sidebar sada nudi tri dubine: **Scout**, **Deep** i **Forensic**. Forensic dodaje source-quality ranking, contradiction radar, query plan i risk flags. Jezički sloj je podrazumevano **Crnogorski**, uz **Romani (beta)** za postepenu lokalizaciju Đinđere Minđere sistema i English fallback. Romani terminologija je jasno označena kao beta da se ne bi izmišljala lokalna varijanta jezika bez ljudske revizije.
