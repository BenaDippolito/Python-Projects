from checker.checks import CHECK_REGISTRY

REQUIRED_FIELDS = {"id", "title", "description", "nist_80053", "severity", "check"}
VALID_SEVERITIES = {"low", "medium", "high", "critical"}


def test_every_control_has_required_fields(controls):
    for c in controls:
        missing = REQUIRED_FIELDS - c.keys()
        assert not missing, f"{c.get('id')} is missing {missing}"


def test_control_ids_are_unique(controls):
    ids = [c["id"] for c in controls]
    assert len(ids) == len(set(ids))


def test_every_check_name_exists_in_registry(controls):
    for c in controls:
        assert c["check"] in CHECK_REGISTRY, f"{c['id']} references unknown check"


def test_severities_are_valid(controls):
    for c in controls:
        assert c["severity"] in VALID_SEVERITIES, f"{c['id']} has bad severity"