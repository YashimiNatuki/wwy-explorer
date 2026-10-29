# AGENTS.md — Base44 sandbox notes

YappinaTor / WWY// Explorer is a single-process **Streamlit** app (`web_explorer.py`).
It needs no database or cache service: the run ledger is local SQLite.

## Run it here

```bash
docker compose -f docker-compose.base44.yml up -d --build
```

- Web entry point: **host port 3000** → Streamlit on `0.0.0.0:3000` inside the container.
- Health check: `curl http://localhost:3000/_stcore/health` (returns `ok`).
- Source is bind-mounted at `/app`, so Python edits are picked up on the next Streamlit
  rerun. `--server.fileWatcherType poll` is set because bind mounts don't deliver inotify
  events in the sandbox.
- Python dependencies are **baked into the image** (`Dockerfile.base44`). Changing
  `requirements.txt` requires `up -d --build`.
- `.streamlit/config.toml` already disables CORS/XSRF, which the preview iframe needs.

## Non-obvious setup facts

- The project pins very old packages (`langchain==0.0.244`, `chromadb==0.4.3`,
  `faiss-cpu==1.7.4`, `openai==0.27.8`). They only install on **Python 3.11**, and
  `chroma-hnswlib` (pulled in by `chromadb`) has no cp311 wheel, so the image installs
  `g++ gcc python3-dev` and compiles it. Without those build tools the install fails with
  `Unsupported compiler -- at least C++11 support is needed!`.
- `chromadb` is listed in `requirements.txt` but never imported by the app. Leaving it
  installed keeps the manifest untouched; the heavy part is the build above.
- The app runs in **DEMO mode without any credentials** — that is intentional, not a
  broken integration. LIVE mode needs `GOOGLE_API_KEY`, `GOOGLE_CSE_ID` and
  `OPENAI_API_KEY`; `Auto` picks LIVE only when all three are present.
- `TOR_PROXY_URL` / `ONION_SEARCH_URL` are optional and unset; the onion connector reports
  `SKIPPED` / `OFF` by design. Never fake them.
- Provider keys are delivered by the platform at `/run/base44/app.env`. Empty
  placeholders live in `.env.base44-defaults`, listed first so real secrets always win.

## Tests / scripts

There is no test suite. Useful checks:

```bash
# defensive audit + connector snapshot + report generation from the SQLite ledger
docker compose -f docker-compose.base44.yml exec -T web python generate_reports.py --out-dir /tmp/reports
```

The ledger lives at `/app/.yappinator/yappinator.db` (gitignored, `YAPPINATOR_DB_PATH`
overrides it).

## Verifying the UI

- The landing screen is an **access-lock simulation**: click *UNLOCK RESEARCH COCKPIT*
  before any controls exist.
- Streamlit's text input only commits its value to the server on blur/Enter, so
  scripted typing easily lands empty and the run button does nothing. Use the sidebar
  **quick-probe** buttons (e.g. `What changed in local-first AI tools this week?`), which
  set the query through `st.session_state`, then click `POKRENI ISTRAŽIVANJE`.
- Section labels are uppercased by CSS, so `innerText` comparisons must be
  case-insensitive.
- A successful demo pass renders 7 `.agent-card` elements, `01 / SYNTHESIZED SIGNAL`,
  `02 / EVIDENCE TRACE` and the dossier actions.
