# Test the individual resource-level compliance checks.
import pytest

from checker.checks import (
    check_cloudtrail_enabled,
    check_iam_mfa,
    check_s3_encryption,
    check_s3_public_access,
    check_sg_ssh_open,
)

# Parameter data for checks that evaluate one boolean compliance field.
BOOLEAN_CHECKS = [
    (check_s3_encryption, "s3_buckets", "name", "encrypted"),
    (check_s3_public_access, "s3_buckets", "name", "public_access_blocked"),
    (check_iam_mfa, "iam_users", "username", "mfa_enabled"),
    (check_cloudtrail_enabled, "cloudtrails", "name", "is_logging"),
]


@pytest.mark.parametrize("check, list_key, id_field, flag", BOOLEAN_CHECKS)
def test_compliant_resource_passes(check, list_key, id_field, flag):
    # A resource with affirmative evidence should pass.
    config = {list_key: [{id_field: "good", flag: True}]}
    results = check(config)
    assert len(results) == 1
    assert results[0]["passed"] is True
    assert results[0]["resource"] == "good"


@pytest.mark.parametrize("check, list_key, id_field, flag", BOOLEAN_CHECKS)
def test_noncompliant_resource_fails(check, list_key, id_field, flag):
    # An explicit negative value should produce a failure.
    config = {list_key: [{id_field: "bad", flag: False}]}
    assert check(config)[0]["passed"] is False


@pytest.mark.parametrize("check, list_key, id_field, flag", BOOLEAN_CHECKS)
def test_missing_field_fails_closed(check, list_key, id_field, flag):
    """No evidence of the control must count as a failure, never a pass."""
    config = {list_key: [{id_field: "unknown"}]}
    assert check(config)[0]["passed"] is False


@pytest.mark.parametrize("check, list_key, id_field, flag", BOOLEAN_CHECKS)
def test_empty_config_returns_no_results(check, list_key, id_field, flag):
    # No in-scope resources means the check has nothing to evaluate.
    assert check({}) == []


def test_mixed_resources_reported_individually():
    # Results must retain the outcome for each resource independently.
    config = {"iam_users": [
        {"username": "alice", "mfa_enabled": True},
        {"username": "bob", "mfa_enabled": False},
    ]}
    by_name = {r["resource"]: r["passed"] for r in check_iam_mfa(config)}
    assert by_name == {"alice": True, "bob": False}


# --- Security group SSH check -------------------------------------------

# Build a minimal security-group configuration for focused SSH scenarios.
def make_sg(*rules):
    return {"security_groups": [{"id": "sg-x", "name": "test", "ingress": list(rules)}]}


def test_ssh_open_to_internet_fails():
    # Port 22 from all IPv4 addresses is non-compliant.
    config = make_sg({"port": 22, "cidr": "0.0.0.0/0"})
    assert check_sg_ssh_open(config)[0]["passed"] is False


def test_ssh_restricted_cidr_passes():
    # A restricted source range is not flagged by this control.
    config = make_sg({"port": 22, "cidr": "10.0.0.0/8"})
    assert check_sg_ssh_open(config)[0]["passed"] is True


def test_https_open_to_internet_is_not_flagged():
    # The control targets SSH, so public HTTPS is outside its scope.
    config = make_sg({"port": 443, "cidr": "0.0.0.0/0"})
    assert check_sg_ssh_open(config)[0]["passed"] is True


def test_no_ingress_rules_passes():
    # A group with no ingress rules has no public SSH exposure.
    assert check_sg_ssh_open(make_sg())[0]["passed"] is True


def test_ssh_open_to_ipv6_internet_should_fail():
    # This documents the known IPv6 detection gap.
    config = make_sg({"port": 22, "cidr": "::/0"})
    assert check_sg_ssh_open(config)[0]["passed"] is False