# YappinaTor — WWY// Explorer / Cyber Ultra Orc Cow

**YappinaTor** je glavni proizvodni sistem. **WWY// Explorer** je njegova napredna research-cockpit verzija: uneseš pitanje, dobiješ sažet signal, trag izvora i dossier koji možeš da sačuvaš. Interfejs radi odmah u **Demo** režimu, bez ključeva, a prelazi u live web research kada su Google CSE i OpenAI promenljive podešene.

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

YappinaTor sada ima WWY// command-center shell, Cyber Ultra Orc Cow branding, telemetry bar, demo/live status, quick probes, session history, depth switch, source evidence kartice, dossier download i reset. Originalni LangChain WebResearchRetriever tok ostaje kao live adapter, ali više nema hardkodovanih provider vrednosti.

## Agent mesh i deep analysis

Posle svakog research pass-a, `analysis_engine.py` pokreće pet transparentnih, bounded uloga nad istim result envelope-om: **Scout**, **Forensics**, **Skeptic**, **Synthesizer** i **Report Smith**. UI prikazuje svaku fazu, njen output, confidence telemetry i uncertainty boundary. U Demo režimu agenti su deterministički i rade nad jasno označenim simuliranim signalom; u Live režimu rade nad stvarno vraćenim odgovorom i source records.

`DOWNLOAD AUTO REPORT` generiše Markdown dossier sa executive signalom, radnom tezom, kompletnim agent trace-om, evidence nodovima i sledećim potezima. Ovo je namerno inspectable: nema skrivenih background agenata i nema tvrdnje da je demo signal pretražio web.

## Maksimalni research režim

Sidebar sada nudi tri dubine: **Scout**, **Deep** i **Forensic**. Forensic dodaje source-quality ranking, contradiction radar, query plan i risk flags. Jezički sloj je podrazumevano **Crnogorski**, uz **Romani (beta)** za postepenu lokalizaciju Đinđere Minđere sistema i English fallback. Romani terminologija je jasno označena kao beta da se ne bi izmišljala lokalna varijanta jezika bez ljudske revizije.

## YappinaTor agent orchestration

Agent mesh sada ima sedam bounded uloga: Scout, Forensics, Skeptic, Synthesizer, Report Smith, **Compute Core** i **Gateway**. Compute Core automatski klasifikuje programming/computational upite i jasno označava da je izvršavanje koda van ovog bezbednog analysis sloja. Gateway dodaje provenance i connector routing bez skrivenih agenata.

Rezultat se može izvesti kao Markdown, JSON evidence envelope ili samostalni HTML dossier. `connectors.py` uvodi stabilan `yappinator.evidence.v1` envelope sa ID-jevima, domenima, pagination poljima i connector snapshotom, što je priprema za bazu/API skaliranje bez menjanja trenutnog Streamlit UI-ja.

`data_store.py` dodaje lokalni SQLite ledger sa WAL journalingom, indeksom po vremenu i recent-runs prikazom. Research pass se čuva kao rezultat + agent analysis payload, bez provider ključeva; putanja se može promeniti kroz `YAPPINATOR_DB_PATH` kada se sistem prebaci na persistent volume ili eksternu bazu.

Onion pretraga je **opt-in connector**, ne podrazumevano uključena. Aktivira se tek kada administrator konfiguriše `TOR_PROXY_URL` i `ONION_SEARCH_URL`; aplikacija ne tvrdi da može da pristupi onion mreži bez tog gateway-a i ne zaobilazi autentikaciju, rate limite ili zaštite izvora.

`probe_onion_gateway()` sada radi stvarni HTTP probe kroz konfigurisan proxy i vraća `SKIPPED`, `ONLINE`, `OFFLINE` ili `ENDPOINT_ERROR`. U trenutnom sandboxu oba endpointa su namjerno **NOT_CONFIGURED**, pa je online test potvrđen kroz lokalni proxy stub, ne kroz izmišljeni javni onion servis.

Kompletan report iz SQLite baze generiše se ovako:

```bash
python generate_reports.py --out-dir reports
```

Dobijaju se `yappinator-latest.md`, `yappinator-latest.html` i `yappinator-connector-status.json`.

Ulazni ekran ima filmski Cyber Ultra Orc Cow access-lock. To je vizuelni operational gate, ne zamena za stvarni login, firewall ili account security.
