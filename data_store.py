from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(os.getenv("YAPPINATOR_DB_PATH", ".yappinator/yappinator.db"))


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA busy_timeout=3000")
    connection.execute("CREATE TABLE IF NOT EXISTS research_runs (id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT NOT NULL, mode TEXT NOT NULL, depth TEXT NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
    connection.execute("CREATE INDEX IF NOT EXISTS idx_research_runs_created ON research_runs(created_at DESC)")
    return connection


def save_run(result: dict[str, Any], analysis: dict[str, Any]) -> int:
    payload = json.dumps({"result": result, "analysis": analysis}, ensure_ascii=False)
    with _connect() as connection:
        cursor = connection.execute("INSERT INTO research_runs(query, mode, depth, payload) VALUES (?, ?, ?, ?)", (result.get("query", ""), result.get("mode", "DEMO"), analysis.get("depth", "Deep"), payload))
        return int(cursor.lastrowid)


def recent_runs(limit: int = 20) -> list[dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute("SELECT id, query, mode, depth, created_at FROM research_runs ORDER BY created_at DESC, id DESC LIMIT ?", (max(1, min(limit, 100)),)).fetchall()
    return [{"id": row[0], "query": row[1], "mode": row[2], "depth": row[3], "created_at": row[4]} for row in rows]


def load_run(run_id: int | None = None) -> dict[str, Any] | None:
    with _connect() as connection:
        if run_id is None:
            row = connection.execute("SELECT id, payload FROM research_runs ORDER BY created_at DESC, id DESC LIMIT 1").fetchone()
        else:
            row = connection.execute("SELECT id, payload FROM research_runs WHERE id = ?", (run_id,)).fetchone()
    if not row:
        return None
    payload = json.loads(row[1])
    payload["run_id"] = row[0]
    return payload
