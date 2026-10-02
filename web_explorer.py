from __future__ import annotations

import html
import os
import textwrap
import time
from datetime import datetime
from typing import Any

import streamlit as st

from analysis_engine import build_report, run_agent_pipeline

APP_NAME = "YAPPINATOR"
SIGNATURE = "CYBER ULTRA ORC COW"
EXAMPLES = [
    "What changed in local-first AI tools this week?",
    "Compare WebAssembly runtimes for edge applications.",
    "Find the strongest evidence for small language model reasoning.",
]
LOCALE_COPY = {
    "Crnogorski": {"subtitle": "istraživački kokpit za napredne korisnike", "query": "istraživački upit", "run": "POKRENI ISTRAŽIVANJE  →", "empty": "NEMA AKTIVNOG SIGNALA", "empty_copy": "Unesi pitanje ili izaberi brzu probu. Forensic režim razdvaja dokaz, rizik i neizvjesnost.", "report": "PREUZMI AUTOMATSKI IZVJEŠTAJ", "demo": "demo mreža online", "hero_a": "PRESIJEČI", "hero_b": "ŠUM.", "hero_copy": "Pretraži, pročitaj i sabij web u dossier sa tragom izvora. Bez lažne sigurnosti. Samo oštriji kokpit za ljude koji traže signal."},
    "Romani (beta)": {"subtitle": "Đinđere Minđere · Romani jezički sloj u beta fazi", "query": "istraživački upit / Romani beta", "run": "POKRENI ISTRAŽIVANJE  →", "empty": "NEMA AKTIVNOG SIGNALA", "empty_copy": "Romani terminologija se uvodi postepeno; pregledaj rezultate i označi izraze za dalju lokalizaciju.", "report": "PREUZMI AUTOMATSKI IZVJEŠTAJ", "demo": "demo mreža online", "hero_a": "PRESIJEČI", "hero_b": "ŠUM.", "hero_copy": "Đinđere Minđere jezički sloj je u beta fazi. Rezultati ostaju transparentni i spremni za ljudsku jezičku reviziju."},
    "English": {"subtitle": "research cockpit for advanced users", "query": "research query", "run": "RUN RESEARCH  →", "empty": "NO ACTIVE SIGNAL", "empty_copy": "Enter a question or choose a quick probe. Forensic mode separates evidence, risk and uncertainty.", "report": "DOWNLOAD AUTO REPORT", "demo": "demo mesh online", "hero_a": "CUT THROUGH", "hero_b": "THE NOISE.", "hero_copy": "Search, read and compress the web into a source-aware dossier. No fake certainty. No hidden keys. Just a sharper cockpit for people who want the signal."},
}

st.set_page_config(
    page_title="YappinaTor — WWY// Explorer Research Cockpit",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
        :root { --void:#07090a; --panel:#101416; --panel2:#151b1c; --line:#243235; --text:#edf3e9; --muted:#879694; --lime:#c8ff3d; --cyan:#63e6e0; --amber:#ffbe55; --red:#ff5d6c; }
        html, body, [data-testid="stAppViewContainer"] { background: radial-gradient(circle at 76% -12%, rgba(200,255,61,.08), transparent 28%), var(--void); color:var(--text); }
        [data-testid="stAppViewContainer"] { font-family:'Space Grotesk', sans-serif; }
        [data-testid="stHeader"] { background:transparent; }
        [data-testid="stSidebar"] { background:linear-gradient(180deg, #0b1011, #080a0b); border-right:1px solid var(--line); }
        [data-testid="stSidebarContent"] { padding: 1.2rem 1rem; }
        .block-container { max-width: 1480px; padding-top: 2rem; padding-bottom: 4rem; }
        .mono, code, .stCaption, [data-testid="stMetricLabel"], [data-testid="stMetricValue"] { font-family:'DM Mono', monospace !important; }
        .wwy-noise { position:fixed; inset:0; pointer-events:none; opacity:.035; z-index:0; background-image:linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px),linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px); background-size:38px 38px; mask-image:linear-gradient(to bottom, black, transparent 82%); }
        .wwy-top { position:relative; z-index:1; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--line); padding-bottom:1.1rem; margin-bottom:2rem; }
        .wwy-brand { display:flex; align-items:center; gap:.8rem; }
        .wwy-mark { display:grid; place-items:center; width:42px; height:42px; border:1px solid var(--lime); color:var(--lime); font:500 16px 'DM Mono',monospace; letter-spacing:-3px; padding-right:4px; box-shadow:0 0 28px rgba(200,255,61,.12); }
        .wwy-word { font-size:1.08rem; letter-spacing:.16em; font-weight:700; }
        .wwy-word span { color:var(--lime); }
        .wwy-sub { color:var(--muted); font:10px 'DM Mono', monospace; letter-spacing:.1em; text-transform:uppercase; margin-top:4px; }
        .wwy-status { display:flex; align-items:center; gap:.7rem; color:var(--muted); font:10px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:.1em; }
        .dot { width:7px; height:7px; border-radius:50%; background:var(--lime); box-shadow:0 0 0 5px rgba(200,255,61,.08), 0 0 18px var(--lime); }
        .dot.demo { background:var(--amber); box-shadow:0 0 0 5px rgba(255,190,85,.08), 0 0 18px var(--amber); }
        .dot.off { background:var(--red); box-shadow:0 0 0 5px rgba(255,93,108,.08); }
        .eyebrow { color:var(--lime); font:10px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:.16em; margin-bottom:1rem; }
        h1, h2, h3 { letter-spacing:-.045em; }
        .wwy-hero h1 { font-size:clamp(3rem, 6vw, 6.9rem); line-height:.87; margin:0; max-width:840px; }
        .wwy-hero h1 em { color:var(--lime); font-style:normal; }
        .wwy-hero p { color:#a1ada9; max-width:570px; font-size:1.05rem; line-height:1.55; margin:1.3rem 0 0; }
        .hero-grid { display:grid; grid-template-columns:1.2fr .8fr; gap:2.5rem; align-items:end; margin-bottom:2.4rem; }
        .signal-card { border:1px solid var(--line); background:linear-gradient(145deg, rgba(200,255,61,.07), rgba(255,255,255,.02)); padding:1.2rem; min-height:170px; position:relative; overflow:hidden; }
        .signal-card:after { content:'ORC // COW'; position:absolute; right:-15px; bottom:-11px; color:rgba(200,255,61,.08); font:700 45px 'DM Mono',monospace; transform:rotate(-12deg); }
        .signal-label { color:var(--muted); font:10px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:.12em; }
        .signal-value { color:var(--lime); font:500 2.6rem 'DM Mono',monospace; margin-top:1.3rem; }
        .signal-detail { color:#9aa7a4; font-size:.82rem; max-width:240px; line-height:1.4; }
        .panel { border:1px solid var(--line); background:rgba(16,20,22,.82); padding:1.1rem; }
        .panel-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; color:var(--muted); font:10px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:.12em; }
        .panel-head strong { color:var(--lime); font-weight:500; }
        .query-box { border:1px solid var(--lime); background:rgba(200,255,61,.035); padding:1rem; margin-bottom:1.1rem; box-shadow:0 0 32px rgba(200,255,61,.05); }
        .query-prefix { color:var(--lime); font:12px 'DM Mono',monospace; margin-bottom:.5rem; }
        .telemetry { display:grid; grid-template-columns:repeat(4,1fr); gap:.7rem; margin:1.2rem 0 2rem; }
        .metric { border-top:1px solid var(--line); padding-top:.7rem; }
        .metric b { display:block; color:var(--text); font:1.2rem 'DM Mono',monospace; }
        .metric span { color:var(--muted); font:9px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:.08em; }
        .section-label { color:var(--cyan); font:10px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:.15em; border-bottom:1px solid var(--line); padding-bottom:.7rem; margin:1.8rem 0 1rem; }
        .answer { font-size:1.05rem; line-height:1.65; color:#e7eee3; }
        .answer strong { color:var(--lime); }
        .source-card { border-left:2px solid var(--cyan); padding:.8rem 1rem; background:rgba(99,230,224,.035); margin-bottom:.6rem; }
        .source-card a { color:var(--text); text-decoration:none; font-weight:600; }
        .source-card a:hover { color:var(--lime); }
        .source-card small { color:var(--muted); display:block; margin-top:.35rem; font:10px 'DM Mono',monospace; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
        .empty-state { border:1px dashed #344347; padding:3.2rem 1.5rem; text-align:center; background:rgba(255,255,255,.015); }
        .empty-state .big { color:var(--lime); font:2.5rem 'DM Mono',monospace; }
        .empty-state p { color:var(--muted); max-width:560px; margin:.8rem auto 0; line-height:1.5; }
        .history-row { padding:.55rem 0; border-bottom:1px solid rgba(255,255,255,.06); color:#b3c0bc; font-size:.82rem; }
        .history-row span { color:var(--lime); font:10px 'DM Mono',monospace; margin-right:.5rem; }
        .sidebar-title { color:var(--lime); font:11px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:.14em; border-bottom:1px solid var(--line); padding-bottom:.75rem; margin:1rem 0; }
        .sidebar-copy { color:var(--muted); font-size:.78rem; line-height:1.5; }
        .pill { display:inline-block; border:1px solid var(--line); padding:.35rem .5rem; color:var(--muted); font:9px 'DM Mono',monospace; text-transform:uppercase; margin:.2rem .2rem 0 0; }
        .footer { border-top:1px solid var(--line); padding-top:1rem; margin-top:3rem; display:flex; justify-content:space-between; color:#5d6d69; font:9px 'DM Mono',monospace; text-transform:uppercase; }
        div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button { border:1px solid var(--line); background:#12191a; color:var(--text); border-radius:0; font-family:'DM Mono',monospace; text-transform:uppercase; letter-spacing:.07em; font-size:10px; min-height:2.4rem; }
        div[data-testid="stButton"] button:hover, div[data-testid="stDownloadButton"] button:hover { border-color:var(--lime); color:var(--lime); }
        div[data-testid="stTextInput"] input { background:#0c1112; border:1px solid #304043; border-radius:0; color:var(--text); font-family:'DM Mono',monospace; }
        div[data-testid="stTextInput"] input:focus { border-color:var(--lime); box-shadow:0 0 0 1px var(--lime); }
        div[data-testid="stAlert"] { border-radius:0; }
        .agent-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:.55rem; margin:1rem 0 1.4rem; }
        .agent-card { position:relative; min-height:126px; border:1px solid var(--line); padding:.72rem; background:linear-gradient(150deg,rgba(255,255,255,.045),rgba(255,255,255,.01)); overflow:hidden; animation:agentIn .45s both; }
        .agent-card:after { content:""; position:absolute; width:90px; height:90px; right:-38px; bottom:-42px; border:1px solid rgba(200,255,61,.16); border-radius:50%; box-shadow:0 0 0 12px rgba(200,255,61,.03),0 0 0 24px rgba(200,255,61,.02); }
        .agent-card.cyan { border-top:2px solid var(--cyan); }.agent-card.amber { border-top:2px solid var(--amber); }.agent-card.violet { border-top:2px solid #b39cff; }.agent-card.red { border-top:2px solid var(--red); }.agent-card.lime { border-top:2px solid var(--lime); }
        .agent-seq { color:var(--muted); font:9px 'DM Mono',monospace; }.agent-name { color:var(--text); font:600 11px 'DM Mono',monospace; letter-spacing:.08em; margin-top:.55rem; }.agent-role { color:var(--muted); font-size:.68rem; line-height:1.25; margin-top:.25rem; }.agent-state { color:var(--lime); font:8px 'DM Mono',monospace; position:absolute; right:.65rem; top:.72rem; }.agent-output { color:#b9c5c0; font-size:.7rem; line-height:1.3; margin-top:.7rem; max-width:190px; }
        .agent-progress { height:2px; background:#27302f; margin-top:.7rem; }.agent-progress span { display:block; height:100%; background:var(--lime); box-shadow:0 0 12px var(--lime); animation:scanPulse 2s ease-in-out infinite; }
        .orbit-core { position:relative; display:grid; place-items:center; width:112px; height:112px; margin:0 auto 1rem; border:1px solid rgba(200,255,61,.5); border-radius:50%; color:var(--lime); font:500 13px 'DM Mono',monospace; box-shadow:0 0 32px rgba(200,255,61,.13), inset 0 0 25px rgba(200,255,61,.07); }
        .orbit-core:before,.orbit-core:after { content:""; position:absolute; inset:-12px; border:1px solid rgba(99,230,224,.25); border-radius:50%; transform:rotate(32deg); animation:orbit 8s linear infinite; }.orbit-core:after { inset:-24px; border-color:rgba(255,190,85,.18); transform:rotate(-25deg); animation-duration:11s; animation-direction:reverse; }.orbit-core b { font-size:1.8rem; letter-spacing:-.1em; }.orbit-core small { position:absolute; bottom:14px; font-size:7px; color:var(--muted); letter-spacing:.14em; }
        .deep-panel { border:1px solid var(--line); background:rgba(16,20,22,.82); padding:1rem; margin-top:1rem; }.deep-panel p { color:#a6b2ad; font-size:.86rem; line-height:1.5; }.confidence-track { height:5px; background:#28302f; margin:.7rem 0; }.confidence-track span { display:block; height:100%; background:linear-gradient(90deg,var(--amber),var(--lime),var(--cyan)); box-shadow:0 0 14px rgba(200,255,61,.4); }.report-chip,.risk-chip { display:inline-block; color:var(--lime); border:1px solid rgba(200,255,61,.35); padding:.35rem .55rem; font:9px 'DM Mono',monospace; text-transform:uppercase; margin:.15rem .15rem .15rem 0; }.risk-chip { color:var(--amber); border-color:rgba(255,190,85,.35); }.qa-grid { display:grid; grid-template-columns:1fr 1fr; gap:.7rem; }.qa-box { border:1px solid var(--line); background:rgba(255,255,255,.018); padding:.85rem; }.qa-box h4 { color:var(--cyan); font:10px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:.1em; margin:0 0 .7rem; }.quality-row,.plan-item { display:flex; justify-content:space-between; gap:.6rem; padding:.42rem 0; border-bottom:1px solid rgba(255,255,255,.06); color:#aebbb5; font-size:.72rem; }.quality-row b { color:var(--lime); font:9px 'DM Mono',monospace; }.plan-item { display:block; }.plan-item:before { content:'› '; color:var(--lime); font-family:'DM Mono',monospace; }
        @keyframes agentIn { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } } @keyframes scanPulse { 0%,100% { opacity:.65; } 50% { opacity:1; } } @keyframes orbit { to { transform:rotate(392deg); } }
        @media (max-width:1100px) { .agent-grid { grid-template-columns:repeat(3,1fr); } } @media (max-width:650px) { .agent-grid { grid-template-columns:1fr 1fr; } }
        @media (max-width:900px) { .hero-grid { grid-template-columns:1fr; gap:1.2rem; } .telemetry { grid-template-columns:repeat(2,1fr); } .wwy-status { display:none; } }
        @media (prefers-reduced-motion:reduce) { *,*:before,*:after { animation:none!important; transition:none!important; } }
        </style>
        <div class="wwy-noise"></div>
        """,
        unsafe_allow_html=True,
    )


def has_live_credentials() -> bool:
    return all(os.getenv(key) for key in ("GOOGLE_API_KEY", "GOOGLE_CSE_ID", "OPENAI_API_KEY"))


def demo_research(question: str, depth: str) -> dict[str, Any]:
    now = datetime.now().strftime("%H:%M:%S")
    answer = (
        f"**Demo signal:** The query is mapped to a {depth.lower()} research pass. "
        "WWY found a strong starting pattern, but this is a local simulation because live provider keys are not configured. "
        "Switch on Google CSE + OpenAI credentials to replace this signal with web-grounded evidence."
    )
    sources = [
        {"title": "WWY // Local signal protocol", "url": "https://github.com/YashimiNatuki/wwy-explorer", "meta": f"session artifact · generated {now}"},
        {"title": "LangChain WebResearchRetriever", "url": "https://python.langchain.com/docs/integrations/retrievers/web_research", "meta": "retrieval architecture reference"},
        {"title": "Query anatomy // next move", "url": "https://docs.streamlit.io/", "meta": "runtime and interface reference"},
    ]
    return {"answer": answer, "sources": sources, "mode": "DEMO", "elapsed": 0.42, "query": question}


def live_research(question: str, depth: str) -> dict[str, Any]:
    try:
        from langchain.callbacks.base import BaseCallbackHandler
        from langchain.chains import RetrievalQAWithSourcesChain
        from langchain.embeddings.openai import OpenAIEmbeddings
        from langchain.chat_models import ChatOpenAI
        from langchain.docstore import InMemoryDocstore
        from langchain.retrievers.web_research import WebResearchRetriever
        from langchain.utilities import GoogleSearchAPIWrapper
        from langchain.vectorstores import FAISS
        import faiss

        class StreamHandler(BaseCallbackHandler):
            def __init__(self, placeholder: Any) -> None:
                self.placeholder = placeholder
                self.text = ""

            def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
                self.text += token
                self.placeholder.markdown(self.text + " ▌")

        started = time.perf_counter()
        embeddings = OpenAIEmbeddings()
        index = faiss.IndexFlatL2(1536)
        vectorstore = FAISS(embeddings.embed_query, index, InMemoryDocstore({}), {})
        llm = ChatOpenAI(model_name=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-16k"), temperature=0, streaming=True)
        search = GoogleSearchAPIWrapper()
        retriever = WebResearchRetriever.from_llm(vectorstore=vectorstore, llm=llm, search=search, num_search_results=5 if depth == "Deep" else 3)
        qa = RetrievalQAWithSourcesChain.from_chain_type(llm, retriever=retriever)
        placeholder = st.empty()
        result = qa({"question": question}, callbacks=[StreamHandler(placeholder)])
        sources = []
        for raw in str(result.get("sources", "")).splitlines():
            raw = raw.strip()
            if raw:
                sources.append({"title": raw, "url": raw if raw.startswith("http") else "", "meta": "live retrieval source"})
        return {"answer": result.get("answer", "No answer returned."), "sources": sources, "mode": "LIVE", "elapsed": round(time.perf_counter() - started, 2), "query": question}
    except Exception as exc:
        return {"answer": f"**Live connector error:** `{type(exc).__name__}: {exc}`\n\nThe UI is still online. Check provider credentials and dependency installation, then retry.", "sources": [], "mode": "ERROR", "elapsed": 0.0, "query": question}


def render_sources(sources: list[dict[str, str]]) -> None:
    if not sources:
        st.caption("No source records returned by this pass.")
        return
    for index, source in enumerate(sources, 1):
        title = html.escape(source.get("title", "Untitled source"))
        url = source.get("url", "")
        safe_url = html.escape(url, quote=True)
        label = f"{index:02d} // {title}"
        link = f'<a href="{safe_url}" target="_blank">{label}</a>' if url.startswith("http") else label
        meta = html.escape(source.get("meta", "evidence record"))
        st.markdown(f'<div class="source-card">{link}<small>{meta}</small></div>', unsafe_allow_html=True)


def render_forensic_panel(analysis: dict[str, Any]) -> None:
    quality_rows = "".join(
        f'<div class="quality-row"><span>{html.escape(item["domain"])}</span><b>{item["label"]} {item["score"]}/100</b></div>'
        for item in analysis.get("source_quality", [])
    ) or '<div class="quality-row"><span>no source nodes</span><b>UNRANKED</b></div>'
    contradiction_rows = "".join(f'<div class="plan-item">{html.escape(item)}</div>' for item in analysis.get("contradictions", []))
    query_rows = "".join(f'<div class="plan-item">{html.escape(item)}</div>' for item in analysis.get("query_plan", []))
    risks = "".join(f'<span class="risk-chip">{html.escape(item)}</span>' for item in analysis.get("risk_flags", []))
    st.markdown('<div class="section-label">02B / forensic QA</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="qa-grid"><div class="qa-box"><h4>source quality radar</h4>{quality_rows}</div><div class="qa-box"><h4>contradiction radar</h4>{contradiction_rows}</div><div class="qa-box"><h4>query plan</h4>{query_rows}</div><div class="qa-box"><h4>risk flags</h4><div>{risks}</div></div></div>', unsafe_allow_html=True)


def dossier_markdown(result: dict[str, Any]) -> str:
    lines = [f"# WWY// Research Dossier", "", f"- Query: {result['query']}", f"- Mode: {result['mode']}", f"- Elapsed: {result['elapsed']}s", "", "## Signal", "", result["answer"], "", "## Evidence", ""]
    lines.extend(f"- {item.get('title')} — {item.get('url', '')}" for item in result.get("sources", []))
    return "\n".join(lines)


inject_styles()

if "history" not in st.session_state:
    st.session_state.history = []
if "result" not in st.session_state:
    st.session_state.result = None

locale = st.sidebar.selectbox("Language layer / jezički sloj", list(LOCALE_COPY), index=0)
copy = LOCALE_COPY[locale]

with st.sidebar:
    st.markdown('<div class="wwy-mark">YT</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Runtime controls</div>', unsafe_allow_html=True)
    mode = st.selectbox("Signal mode", ["Auto", "Demo", "Live"], index=0, help="Auto uses live mode only when all provider credentials are configured.")
    depth = st.radio("Research depth", ["Scout", "Deep", "Forensic"], horizontal=True)
    st.markdown('<div class="sidebar-title">Capability matrix</div>', unsafe_allow_html=True)
    live_ready = has_live_credentials()
    st.markdown(f'<span class="pill">{"LIVE READY" if live_ready else "DEMO READY"}</span><span class="pill">LOCAL HISTORY</span><span class="pill">SOURCE TRACE</span>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-copy">WWY never ships API keys in source. Demo mode is intentional: it keeps the cockpit usable before the web provider layer is connected.</p>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Agent mesh</div>', unsafe_allow_html=True)
    st.markdown('<span class="pill">SCOUT</span><span class="pill">FORENSICS</span><span class="pill">SKEPTIC</span><span class="pill">SYNTH</span><span class="pill">REPORT SMITH</span>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-copy">Five bounded roles inspect the same evidence envelope. Their trace is rendered after every pass; no hidden background agent is claimed.</p>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Quick probes</div>', unsafe_allow_html=True)
    for example in EXAMPLES:
        if st.button(example, key=f"example_{example}", use_container_width=True):
            st.session_state.query = example
            st.rerun()
    if st.session_state.history:
        st.markdown('<div class="sidebar-title">Session history</div>', unsafe_allow_html=True)
        for item in reversed(st.session_state.history[-6:]):
            st.markdown(f'<div class="history-row"><span>{html.escape(item["mode"])}</span>{html.escape(item["query"][:58])}</div>', unsafe_allow_html=True)
    if st.button("Clear session", use_container_width=True):
        st.session_state.history = []
        st.session_state.result = None
        st.rerun()

st.markdown(
    '<div class="wwy-top"><div class="wwy-brand"><div class="wwy-mark">YT</div><div><div class="wwy-word">YAPPINATOR<span>//</span></div><div class="wwy-sub">WWY// EXPLORER · ĐINĐERE MINĐERE · ' + copy["subtitle"] + '</div></div></div><div class="wwy-status"><span class="dot ' + ("" if live_ready else "demo") + '"></span>' + ("provider mesh online" if live_ready else copy["demo"]) + ' <span>v.5.0</span></div></div>',
    unsafe_allow_html=True,
)

st.markdown(f'<div class="hero-grid"><div class="wwy-hero"><div class="eyebrow">◈ signal intake / 001</div><h1>{copy["hero_a"]}<br /><em>{copy["hero_b"]}</em></h1><p>{copy["hero_copy"]}</p></div><div class="signal-card"><div class="signal-label">ORC COW // CORE STATUS</div><div class="signal-value">READY_</div><div class="signal-detail">The interface runs in demo mode without credentials, then upgrades to live retrieval when the provider mesh is connected.</div></div></div>', unsafe_allow_html=True)

st.markdown('<div class="query-box"><div class="query-prefix">WWY://research --target web --depth ' + depth.lower() + ' --lang ' + locale.lower().replace(" ", "-") + '</div>', unsafe_allow_html=True)
query = st.text_input(copy["query"], key="query", placeholder="Ask a question worth tracing…", label_visibility="collapsed")
run = st.button(copy["run"], type="primary", use_container_width=False)
st.markdown('</div>', unsafe_allow_html=True)

if run and query.strip():
    selected_mode = "live" if mode == "Live" or (mode == "Auto" and live_ready) else "demo"
    with st.status("Scanning the signal field…", expanded=False) as status:
        if selected_mode == "live":
            result = live_research(query.strip(), depth)
        else:
            result = demo_research(query.strip(), depth)
        status.update(label=f"{result['mode']} pass complete", state="complete" if result["mode"] != "ERROR" else "error")
    st.session_state.result = result
    st.session_state.history.append({"query": query.strip(), "mode": result["mode"]})

result = st.session_state.result
if result:
    analysis = run_agent_pipeline(result["query"], result, depth)
    st.markdown('<div class="telemetry"><div class="metric"><b>' + result["mode"] + '</b><span>runtime mode</span></div><div class="metric"><b>' + str(result["elapsed"]) + 's</b><span>latency</span></div><div class="metric"><b>' + str(len(result.get("sources", []))).zfill(2) + '</b><span>evidence nodes</span></div><div class="metric"><b>' + str(len(st.session_state.history)).zfill(2) + '</b><span>session passes</span></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">00 / agent mesh telemetry</div>', unsafe_allow_html=True)
    cards = []
    for stage in analysis["stages"]:
        cards.append(
            f'<div class="agent-card {stage["accent"]}"><span class="agent-seq">{stage["sequence"]} / MESH</span><span class="agent-state">{stage["status"]}</span><div class="agent-name">{stage["name"]}</div><div class="agent-role">{stage["role"]}</div><div class="agent-output">{html.escape(stage["output"])}</div><div class="agent-progress"><span style="width:{stage["pulse"]}%"></span></div></div>'
        )
    st.markdown('<div class="agent-grid">' + "".join(cards) + "</div>", unsafe_allow_html=True)
    left, right = st.columns([1.45, .85], gap="large")
    with left:
        st.markdown('<div class="section-label">01 / synthesized signal</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="panel"><div class="answer">{result["answer"]}</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">02 / evidence trace</div>', unsafe_allow_html=True)
        render_sources(result.get("sources", []))
        render_forensic_panel(analysis)
    with right:
        st.markdown('<div class="section-label">03 / dossier actions</div>', unsafe_allow_html=True)
        st.markdown('<div class="orbit-core"><b>WWY</b><small>AGENT MESH</small></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="deep-panel"><div class="panel-head"><span>Deep analysis confidence</span><strong>{analysis["confidence"]}%</strong></div><div class="confidence-track"><span style="width:{analysis["confidence"]}%"></span></div><p>{html.escape(analysis["thesis"])}</p><span class="report-chip">AUTO REPORT READY</span></div>', unsafe_allow_html=True)
        st.download_button(copy["report"], build_report(result, analysis), file_name="yappinator-deep-analysis-dossier.md", mime="text/markdown", use_container_width=True)
        if st.button("NEW SIGNAL", use_container_width=True):
            st.session_state.result = None
            st.rerun()
        st.markdown('<div class="panel"><div class="panel-head"><span>Current target</span><strong>LOCKED</strong></div><p class="sidebar-copy">' + html.escape(result["query"]) + '</p><p class="sidebar-copy">Mode: ' + html.escape(result["mode"]) + '<br />Depth: ' + html.escape(depth) + '</p></div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="empty-state"><div class="big">◈_</div><h3>{copy["empty"]}</h3><p>{copy["empty_copy"]}</p></div>', unsafe_allow_html=True)

st.markdown('<div class="footer"><span>YAPPINATOR · WWY// EXPLORER · cyber ultra orc cow</span><span>truthful telemetry // local-first by default</span></div>', unsafe_allow_html=True)
