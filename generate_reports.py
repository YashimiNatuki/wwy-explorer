from __future__ import annotations

import argparse
import json
from pathlib import Path

from analysis_engine import build_html_report, build_report
from connectors import connector_snapshot, probe_onion_gateway
from data_store import load_run


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate YappinaTor reports from SQLite")
    parser.add_argument("--run-id", type=int, default=None)
    parser.add_argument("--out-dir", default="reports")
    args = parser.parse_args()
    payload = load_run(args.run_id)
    if not payload:
        raise SystemExit("No SQLite research run found")
    result, analysis = payload["result"], payload["analysis"]
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "yappinator-latest.md").write_text(build_report(result, analysis), encoding="utf-8")
    (out / "yappinator-latest.html").write_text(build_html_report(result, analysis), encoding="utf-8")
    (out / "yappinator-connector-status.json").write_text(json.dumps({"connectors": connector_snapshot(), "onion_probe": probe_onion_gateway()}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"run_id": payload["run_id"], "markdown": str(out / "yappinator-latest.md"), "html": str(out / "yappinator-latest.html"), "onion": probe_onion_gateway()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
