import json
from pathlib import Path

import yaml

from checker.engine import ComplianceEngine

PROJECT_ROOT = Path(__file__).resolve().parent

def main():
    with open(PROJECT_ROOT / "controls" / "controls.yaml") as f:
        controls = yaml.safe_load(f)["controls"]

    with open(PROJECT_ROOT / "data" / "mock_aws_config.json") as f:
        config = json.load(f)

    engine = ComplianceEngine(controls, config)
    results = engine.run_all()

    print(f"\n{'ID':<9}{'STATUS':<8}{'SEVERITY':<10}TITLE")
    print("-" * 70)
    for r in results:
        print(f"{r['control_id']:<9}{r['status']:<8}{r['severity']:<10}{r['title']}")
        for failure in r["failures"]:
            print(f"           -> {failure['resource']}: {failure['detail']}")

    passed = sum(1 for r in results if r["status"] == "PASS")
    print(f"\n{passed}/{len(results)} controls passed")


if __name__ == "__main__":
    main()