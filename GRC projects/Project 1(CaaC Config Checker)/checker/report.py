import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

CSV_COLUMNS = [
    "control_id", "title", "severity", "nist_80053", "cis_ref",
    "status", "resource", "detail",
]


def build_report(results: list[dict], source: str) -> dict:
    """Wrap raw results with metadata and a summary."""
    counts = Counter(r["status"] for r in results)
    return {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "config_source": source,
            "tool_version": "0.1.0",
        },
        "summary": {
            "total_controls": len(results),
            "pass": counts.get("PASS", 0),
            "fail": counts.get("FAIL", 0),
            "error": counts.get("ERROR", 0),
            "not_applicable": counts.get("N/A", 0),
        },
        "results": results,
    }


def write_json(report: dict, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return path


def _safe(value) -> str:
    """Neutralize spreadsheet formula injection (=, +, -, @ at the start)."""
    text = str(value)
    return "'" + text if text.startswith(("=", "+", "-", "@")) else text


def write_csv(results: list[dict], path: Path) -> Path:
    """One row per failing resource; one row for controls with no failures."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for r in results:
            base = {
                "control_id": r["control_id"],
                "title": _safe(r["title"]),
                "severity": r["severity"],
                "nist_80053": r["nist_80053"],
                "cis_ref": r["cis_ref"],
                "status": r["status"],
            }
            if r["failures"]:
                for failure in r["failures"]:
                    writer.writerow({
                        **base,
                        "resource": _safe(failure["resource"]),
                        "detail": _safe(failure["detail"]),
                    })
            else:
                writer.writerow({**base, "resource": "", "detail": _safe(r["error"] or "")})
    return path


def timestamped_name(prefix: str, extension: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}_{stamp}.{extension}"