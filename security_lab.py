from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any

from connectors import connector_snapshot, probe_onion_gateway
from data_store import DB_PATH

SECRET_PATTERNS = [re.compile(r"sk-[A-Za-z0-9]{20,}"), re.compile(r"AIza[0-9A-Za-z_-]{20,}"), re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")]


def run_defensive_audit(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root)
    findings: list[dict[str, str]] = []
    scanned = 0
    for path in base.rglob("*"):
        if not path.is_file() or any(part in {".git", ".venv", "__pycache__", ".yappinator"} for part in path.parts):
            continue
        if path.suffix not in {".py", ".toml", ".md", ".json", ".env"}:
            continue
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append({"severity": "HIGH", "file": str(path), "detail": "Potential secret pattern found; rotate and remove from source."})
    required = ["web_explorer.py", "analysis_engine.py", "connectors.py", "data_store.py", "generate_reports.py"]
    missing = [item for item in required if not (base / item).exists()]
    if missing:
        findings.append({"severity": "HIGH", "file": ", ".join(missing), "detail": "Required YappinaTor module missing."})
    db_status = "NOT_INITIALIZED"
    if DB_PATH.exists():
        try:
            with sqlite3.connect(DB_PATH) as connection:
                db_status = str(connection.execute("PRAGMA integrity_check").fetchone()[0]).upper()
        except sqlite3.Error as exc:
            db_status = f"ERROR: {type(exc).__name__}"
    return {
        "mode": "DEFENSIVE_ONLY",
        "scanned_files": scanned,
        "secret_findings": findings,
        "db_integrity": db_status,
        "connectors": connector_snapshot(),
        "onion_probe": probe_onion_gateway(),
        "status": "PASS" if not findings and db_status in {"OK", "NOT_INITIALIZED"} else "REVIEW",
    }
