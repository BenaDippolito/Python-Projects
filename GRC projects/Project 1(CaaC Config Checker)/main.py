# Standard-library imports for JSON parsing, process exit handling, and paths.
import json
import sys
from pathlib import Path

# Third-party and project-specific imports used to load controls and create reports.
import yaml

from checker.engine import ComplianceEngine
from checker.report import build_report, timestamped_name, write_csv, write_json

# Resolve project files relative to this script so the checker works from any
# current working directory.
PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "output"
CONFIG_PATH = PROJECT_ROOT / "data" / "mock_aws_config.json"


def print_summary(results: list[dict]) -> None:
    """Print each control's status and the resources that caused failures."""
    print(f"\n{'ID':<9}{'STATUS':<8}{'SEVERITY':<10}TITLE")
    print("-" * 70)
    for r in results:
        print(f"{r['control_id']:<9}{r['status']:<8}{r['severity']:<10}{r['title']}")
        for failure in r["failures"]:
            print(f"           -> {failure['resource']}: {failure['detail']}")


def main() -> int:
    # Load the compliance controls that define what the configuration must satisfy.
    with open(PROJECT_ROOT / "controls" / "controls.yaml") as f:
        controls = yaml.safe_load(f)["controls"]

    # Load the configuration snapshot that will be evaluated.
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    # Create the compliance engine, run every control, and assemble a report
    # containing the results and the source configuration name.
    engine = ComplianceEngine(controls, config)
    results = engine.run_all()
    report = build_report(results, source=CONFIG_PATH.name)

    # Show a human-readable result summary in the console.
    print_summary(results)

    # Persist machine-readable JSON and CSV reports with unique timestamped names.
    json_path = write_json(report, OUTPUT_DIR / timestamped_name("report", "json"))
    csv_path = write_csv(results, OUTPUT_DIR / timestamped_name("report", "csv"))

    # Display aggregate results and the locations of the generated report files.
    s = report["summary"]
    print(f"\n{s['pass']}/{s['total_controls']} controls passed "
          f"({s['fail']} failed, {s['error']} errors, {s['not_applicable']} N/A)")
    print(f"JSON report: {json_path.relative_to(PROJECT_ROOT)}")
    print(f"CSV report:  {csv_path.relative_to(PROJECT_ROOT)}")

    # Return a non-zero exit code when controls fail or error so CI can block
    # a non-compliant configuration.
    return 0 if s["fail"] == 0 and s["error"] == 0 else 1


# Run the checker when this file is executed directly, not when it is imported.
if __name__ == "__main__":
    sys.exit(main())