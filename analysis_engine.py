from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

from connectors import classify_query, connector_snapshot, source_envelope


@dataclass(frozen=True)
class AgentSpec:
    key: str
    name: str
    role: str
    accent: str


AGENTS = (
    AgentSpec("scout", "SCOUT", "query expansion + entity map", "lime"),
    AgentSpec("forensics", "FORENSICS", "evidence weighting + provenance", "cyan"),
    AgentSpec("skeptic", "SKEPTIC", "contradictions + uncertainty", "amber"),
    AgentSpec("synth", "SYNTHESIZER", "thesis + decision signal", "violet"),
    AgentSpec("report", "REPORT SMITH", "automatic dossier assembly", "red"),
    AgentSpec("compute", "COMPUTE CORE", "programming + computational reasoning", "cyan"),
    AgentSpec("gateway", "GATEWAY", "connector routing + provenance", "amber"),
)


def _tokens(question: str) -> list[str]:
    words = re.findall(r"[A-Za-z0-9À-ž]{4,}", question.lower())
    return list(dict.fromkeys(words))[:8]


def _source_count(result: dict[str, Any]) -> int:
    return len(result.get("sources", []))


def _source_quality(result: dict[str, Any]) -> list[dict[str, Any]]:
    quality = []
    for index, source in enumerate(result.get("sources", []), 1):
        url = source.get("url", "")
        domain = urlparse(url).netloc.replace("www.", "") or "local-artifact"
        score = min(98, 58 + (14 if domain.endswith(".gov") or domain.endswith(".edu") else 7 if domain.endswith(".org") else 0) + max(0, 12 - index * 2))
        label = "PRIMARY" if score >= 80 else "SECONDARY"
        quality.append({"rank": index, "domain": domain, "score": score, "label": label, "title": source.get("title", "Untitled source")})
    return quality


def run_agent_pipeline(question: str, result: dict[str, Any], depth: str = "Deep") -> dict[str, Any]:
    terms = _tokens(question)
    query_class = classify_query(question)
    sources = _source_count(result)
    mode = result.get("mode", "DEMO")
    confidence = min(96, 52 + sources * 9 + (12 if mode == "LIVE" else 0) + (8 if depth == "Deep" else 0) + (12 if depth == "Forensic" else 0) + (4 if query_class["computational"] else 0))
    term_line = " · ".join(terms[:5]) or "no stable entities extracted"
    answer = str(result.get("answer", "")).replace("\n", " ").strip()
    answer_hint = answer[:150] + ("…" if len(answer) > 150 else "")
    caveat = "Provider-backed evidence is available, but source quality still needs human review." if mode == "LIVE" else "Demo evidence is simulated; connect providers before treating this as a factual briefing."
    source_quality = _source_quality(result)
    contradictions = [
        "Evidence count alone is not consensus; source independence is still unverified.",
        "A confident synthesis can still inherit a blind spot from the query wording.",
    ] if depth in ("Deep", "Forensic") else ["Scout pass has not run a contradiction sweep."]
    risk_flags = [
        "SIMULATED_EVIDENCE" if mode != "LIVE" else "PROVIDER_DEPENDENCY",
        "HUMAN_REVIEW_REQUIRED",
        "QUERY_BIAS_POSSIBLE",
    ]
    outputs = {
        "scout": f"Expanded target into {len(terms)} query atoms: {term_line}.",
        "forensics": f"Mapped {sources:02d} evidence nodes; runtime provenance is {mode.lower()} and traceable.",
        "skeptic": caveat,
        "synth": f"Working thesis: the strongest signal is the relationship between {terms[0] if terms else 'the target'} and the requested decision.",
        "report": f"Dossier assembled with {confidence}% internal confidence and a {depth.lower()} evidence pass.",
        "compute": f"Track classified as {query_class['track']}; {query_class['safety']}.",
        "gateway": f"Routed through {len(connector_snapshot())} declared connector lanes; onion gateway is explicit and opt-in.",
    }
    stages = []
    for index, spec in enumerate(AGENTS, 1):
        stages.append({
            "key": spec.key, "name": spec.name, "role": spec.role, "accent": spec.accent,
            "sequence": f"0{index}", "status": "COMPLETE", "output": outputs[spec.key],
            "pulse": min(99, confidence - index * 3),
        })
    return {
        "question": question, "mode": mode, "depth": depth, "confidence": confidence,
        "terms": terms, "stages": stages, "thesis": outputs["synth"], "caveat": caveat,
        "answer_hint": answer_hint, "query_plan": [f"Locate primary evidence for: {term}" for term in terms[:4]] or ["Clarify target and rerun with a more specific query."],
        "source_quality": source_quality, "contradictions": contradictions, "risk_flags": risk_flags,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "query_class": query_class,
        "connectors": connector_snapshot(), "evidence_envelope": source_envelope(result.get("sources", [])),
    }


def build_report(result: dict[str, Any], analysis: dict[str, Any]) -> str:
    sources = result.get("sources", [])
    lines = [
        "# YappinaTor // Deep Analysis Dossier", "", f"> Generated by Cyber Ultra Orc Cow agent mesh · {analysis['generated_at']}", "",
        "## Mission", "", f"- Query: {analysis['question']}", f"- Runtime mode: {analysis['mode']}", f"- Depth: {analysis['depth']}", f"- Agent confidence: {analysis['confidence']}%", f"- Analysis track: {analysis['query_class']['track']}",
        "", "## Executive signal", "", result.get("answer", "No answer returned."), "", "## Working thesis", "", analysis["thesis"], "", "## Agent trace", "",
    ]
    for stage in analysis["stages"]:
        lines.extend([f"### {stage['sequence']} / {stage['name']}", "", f"**Role:** {stage['role']}", "", stage["output"], ""])
    lines.extend(["## Uncertainty boundary", "", analysis["caveat"], "", "## Contradiction radar", ""])
    lines.extend(f"- {item}" for item in analysis["contradictions"])
    lines.extend(["", "## Risk flags", ""])
    lines.extend(f"- `{item}`" for item in analysis["risk_flags"])
    lines.extend(["", "## Query plan", ""])
    lines.extend(f"- {item}" for item in analysis["query_plan"])
    lines.extend(["", "## Evidence nodes", ""])
    for index, source in enumerate(sources, 1):
        quality = analysis["source_quality"][index - 1] if index <= len(analysis["source_quality"]) else {"score": "n/a", "label": "UNRANKED"}
        lines.append(f"{index}. [{source.get('title', 'Untitled source')}]({source.get('url', '')}) — {source.get('meta', 'evidence record')} · {quality['label']} {quality['score']}/100")
    lines.extend(["", "## Next moves", "", "1. Verify the strongest source node.", "2. Challenge the thesis with a counter-query.", "3. Re-run in Deep mode before making a high-impact decision."])
    return "\n".join(lines)


def build_json_report(result: dict[str, Any], analysis: dict[str, Any]) -> str:
    return json.dumps({"product": "YappinaTor", "result": result, "analysis": analysis}, ensure_ascii=False, indent=2)


def build_html_report(result: dict[str, Any], analysis: dict[str, Any]) -> str:
    title = "YappinaTor // Deep Analysis Dossier"
    body = build_report(result, analysis).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"<!doctype html><html lang='sr-Latn'><head><meta charset='utf-8'><title>{title}</title><style>body{{background:#07090a;color:#edf3e9;font:16px system-ui;max-width:960px;margin:40px auto;padding:0 20px}}h1,h2{{color:#c8ff3d}}pre{{white-space:pre-wrap;border:1px solid #243235;padding:20px;background:#101416}}</style></head><body><h1>{title}</h1><h2>{analysis['question']}</h2><pre>{body}</pre></body></html>"
