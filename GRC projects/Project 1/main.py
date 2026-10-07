import json
import sys
from pathlib import Path

import yaml

from checker.engine import ComplianceEngine
from checker.report import build_report, timestamped_name, write_csv, write_json

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "output"
CONFIG_PATH = PROJECT_ROOT / "data" / "mock_aws_config.json"


def print_summary(results: list[dict]) -> None:
    print(f"\n{'ID':<9}{'STATUS':<8}{'SEVERITY':<10}TITLE")
    print("-" * 70)
    for r in results:
        print(f"{r['control_id']:<9}{r['status']:<8}{r['severity']:<10}{r['title']}")
        for failure in r["failures"]:
            print(f"           -> {failure['resource']}: {failure['detail']}")


def main() -> int:
    with open(PROJECT_ROOT / "controls" / "controls.yaml") as f:
        controls = yaml.safe_load(f)["controls"]

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    engine = ComplianceEngine(controls, config)
    results = engine.run_all()
    report = build_report(results, source=CONFIG_PATH.name)

    print_summary(results)

    json_path = write_json(report, OUTPUT_DIR / timestamped_name("report", "json"))
    csv_path = write_csv(results, OUTPUT_DIR / timestamped_name("report", "csv"))

    s = report["summary"]
    print(f"\n{s['pass']}/{s['total_controls']} controls passed "
          f"({s['fail']} failed, {s['error']} errors, {s['not_applicable']} N/A)")
    print(f"JSON report: {json_path.relative_to(PROJECT_ROOT)}")
    print(f"CSV report:  {csv_path.relative_to(PROJECT_ROOT)}")

    # Non-zero exit code when anything fails: lets CI pipelines block on it later.
    return 0 if s["fail"] == 0 and s["error"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())