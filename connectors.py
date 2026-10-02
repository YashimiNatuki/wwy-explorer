from __future__ import annotations

import hashlib
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse


@dataclass(frozen=True)
class ConnectorStatus:
    key: str
    label: str
    kind: str
    status: str
    detail: str
    endpoint: str = ""


def connector_registry() -> list[ConnectorStatus]:
    """Return an inspectable connector map; no provider keys are ever returned."""
    live = all(os.getenv(key) for key in ("GOOGLE_API_KEY", "GOOGLE_CSE_ID", "OPENAI_API_KEY"))
    tor_endpoint = os.getenv("TOR_PROXY_URL", "")
    onion_search = os.getenv("ONION_SEARCH_URL", "")
    return [
        ConnectorStatus("web", "Web research", "provider", "READY" if live else "DEMO", "Google CSE + LLM adapter"),
        ConnectorStatus("local", "Local signal cache", "storage", "READY", "session-safe, ephemeral cache"),
        ConnectorStatus("onion", "Onion gateway", "optional", "READY" if tor_endpoint and onion_search else "OFF", "Optional Tor gateway; disabled until an approved proxy/search endpoint is configured", tor_endpoint),
    ]


def connector_snapshot() -> list[dict[str, Any]]:
    return [asdict(item) for item in connector_registry()]


def source_envelope(sources: list[dict[str, Any]], *, page: int = 1, page_size: int = 25) -> dict[str, Any]:
    """Normalize evidence for future DB/API pagination without changing current UI shape."""
    clean = []
    for index, source in enumerate(sources[: max(1, page_size)], 1):
        url = str(source.get("url", ""))
        domain = urlparse(url).netloc.replace("www.", "") or "local-artifact"
        clean.append({
            "id": hashlib.sha1(f"{url}|{source.get('title', '')}".encode()).hexdigest()[:12],
            "rank": index,
            "title": str(source.get("title", "Untitled source")),
            "url": url,
            "domain": domain,
            "meta": str(source.get("meta", "evidence record")),
        })
    return {
        "schema": "yappinator.evidence.v1",
        "items": clean,
        "page": page,
        "page_size": page_size,
        "has_next": len(sources) > page * page_size,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def classify_query(question: str) -> dict[str, Any]:
    text = question.lower()
    programming = bool(re.search(r"\b(code|program|python|javascript|typescript|api|debug|algorithm|sql|compile|function|repo|repository|architecture|webassembly|runtime|frontend|backend|database|edge)\b", text))
    computational = programming or bool(re.search(r"\b(calculate|compute|model|benchmark|complexity|formula|data|statistics|optimize)\b", text))
    return {
        "programming": programming,
        "computational": computational,
        "track": "PROGRAMMING + COMPUTATIONAL" if computational else "RESEARCH",
        "safety": "analysis-only; execution sandbox not enabled",
    }
