# Validate that policy data remains compatible with the check registry.
from checker.checks import CHECK_REGISTRY

# Fields required for every control to be auditable and executable.
REQUIRED_FIELDS = {"id", "title", "description", "nist_80053", "severity", "check"}
# Severity values accepted by the policy schema.
VALID_SEVERITIES = {"low", "medium", "high", "critical"}


def test_every_control_has_required_fields(controls):
    # Every control must contain its audit metadata and implementation link.
    for c in controls:
        missing = REQUIRED_FIELDS - c.keys()
        assert not missing, f"{c.get('id')} is missing {missing}"


def test_control_ids_are_unique(controls):
    # IDs are the stable identifiers used to distinguish controls in reports.
    ids = [c["id"] for c in controls]
    assert len(ids) == len(set(ids))


def test_every_check_name_exists_in_registry(controls):
    # Every YAML check reference must resolve to a registered function.
    for c in controls:
        assert c["check"] in CHECK_REGISTRY, f"{c['id']} references unknown check"


def test_severities_are_valid(controls):
    # Reject accidental or unsupported severity labels.
    for c in controls:
        assert c["severity"] in VALID_SEVERITIES, f"{c['id']} has bad severity"