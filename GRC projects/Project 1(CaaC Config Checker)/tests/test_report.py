# Test report structure, serialization, and spreadsheet-safe output.
import csv
import json
import re

from checker.report import (
    CSV_COLUMNS, _safe, build_report, timestamped_name, write_csv, write_json,
)
from checker.engine import ComplianceEngine


def test_build_report_summary_counts(controls, mock_config):
    # Summary totals must reflect the complete engine result set.
    results = ComplianceEngine(controls, mock_config).run_all()
    summary = build_report(results, source="mock.json")["summary"]
    assert summary["total_controls"] == 5
    assert summary["fail"] == 5
    assert summary["pass"] == 0


def test_report_metadata_has_utc_timestamp(controls, mock_config):
    # Report timestamps are required to be explicit UTC ISO 8601 values.
    results = ComplianceEngine(controls, mock_config).run_all()
    meta = build_report(results, source="mock.json")["metadata"]
    assert meta["config_source"] == "mock.json"
    assert meta["generated_at"].endswith("+00:00")  # UTC


def test_json_roundtrip(tmp_path, controls, mock_config):
    # JSON serialization must preserve the report structure exactly.
    results = ComplianceEngine(controls, mock_config).run_all()
    report = build_report(results, source="mock.json")
    path = write_json(report, tmp_path / "nested" / "report.json")
    assert json.loads(path.read_text(encoding="utf-8")) == report


def test_csv_has_one_row_per_failure(tmp_path, controls, mock_config):
    # CSV output flattens failures while retaining the expected header order.
    results = ComplianceEngine(controls, mock_config).run_all()
    path = write_csv(results, tmp_path / "report.csv")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert reader.fieldnames == CSV_COLUMNS
    assert len(rows) == 7


def test_csv_formula_injection_is_neutralized(tmp_path):
    # Spreadsheet formulas from untrusted values must be rendered harmless.
    results = [{
        "control_id": "T-1", "title": "t", "severity": "high",
        "nist_80053": "", "cis_ref": "", "status": "FAIL", "error": None,
        "failures": [{"resource": "=HYPERLINK(\"http://evil\")", "detail": "bad"}],
    }]
    path = write_csv(results, tmp_path / "r.csv")
    with open(path, newline="", encoding="utf-8") as f:
        row = next(csv.DictReader(f))
    assert row["resource"].startswith("'=")


def test_safe_leaves_normal_text_alone():
    # Normal resource text should not be modified.
    assert _safe("finance-reports") == "finance-reports"


def test_timestamped_name_format():
    # Generated filenames must contain a sortable UTC timestamp.
    assert re.fullmatch(r"report_\d{8}T\d{6}Z\.json", timestamped_name("report", "json"))