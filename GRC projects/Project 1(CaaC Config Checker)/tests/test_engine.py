# Test status classification, error isolation, and complete-scan behavior.
from checker.engine import ComplianceEngine


def make_control(check="check_iam_mfa"):
    # Construct the smallest valid control definition for engine tests.
    return {"id": "T-001", "title": "Test control", "severity": "high",
            "nist_80053": "IA-2", "check": check}


def run(config, check="check_iam_mfa"):
    # Run one synthetic control and return its structured result.
    return ComplianceEngine([make_control(check)], config).run_all()[0]


def test_pass_status():
    # All checked resources compliant produces PASS.
    result = run({"iam_users": [{"username": "a", "mfa_enabled": True}]})
    assert result["status"] == "PASS"
    assert result["failures"] == []
    assert result["resources_checked"] == 1


def test_fail_status_lists_failing_resources():
    # A mixed resource set produces FAIL with only failed resources listed.
    config = {"iam_users": [
        {"username": "a", "mfa_enabled": True},
        {"username": "b", "mfa_enabled": False},
    ]}
    result = run(config)
    assert result["status"] == "FAIL"
    assert [f["resource"] for f in result["failures"]] == ["b"]


def test_not_applicable_when_no_resources():
    # An empty scope is reported as N/A rather than an implicit pass.
    assert run({})["status"] == "N/A"


def test_unknown_check_name_is_error_not_crash():
    # Invalid registry references become explicit control errors.
    result = run({}, check="check_does_not_exist")
    assert result["status"] == "ERROR"
    assert "check_does_not_exist" in result["error"]


def test_check_that_raises_is_isolated_as_error():
    malformed = {"iam_users": [{"mfa_enabled": True}]}  # missing 'username'
    result = run(malformed)
    assert result["status"] == "ERROR"
    assert "KeyError" in result["error"]


def test_one_error_does_not_stop_other_controls():
    # One control error must not prevent later controls from running.
    controls = [make_control("check_does_not_exist"), make_control("check_iam_mfa")]
    config = {"iam_users": [{"username": "a", "mfa_enabled": True}]}
    statuses = [r["status"] for r in ComplianceEngine(controls, config).run_all()]
    assert statuses == ["ERROR", "PASS"]


def test_full_mock_scan_matches_expected_findings(controls, mock_config):
    """Golden test: the sample data must produce exactly the known violations."""
    results = {r["control_id"]: r for r in ComplianceEngine(controls, mock_config).run_all()}
    failing = {cid: sorted(f["resource"] for f in r["failures"]) for cid, r in results.items()}
    assert failing == {
        "GRC-001": ["marketing-assets"],
        "GRC-002": ["customer-backups", "marketing-assets"],
        "GRC-003": ["bob", "svc-deploy"],
        "GRC-004": ["admin-sg (sg-002)"],
        "GRC-005": ["legacy-trail"],
    }