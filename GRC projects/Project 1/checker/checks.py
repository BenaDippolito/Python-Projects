"""Check functions: one per control.

Every check takes the full config dict and returns a list of
resource-level results, so an auditor can see exactly WHICH
resources failed, not just that "something" failed.
"""


def _result(resource: str, passed: bool, detail: str) -> dict:
    return {"resource": resource, "passed": passed, "detail": detail}


def check_s3_encryption(config: dict) -> list[dict]:
    results = []
    for bucket in config.get("s3_buckets", []):
        passed = bucket.get("encrypted", False)
        detail = "Encryption enabled" if passed else "Encryption NOT enabled"
        results.append(_result(bucket["name"], passed, detail))
    return results


def check_s3_public_access(config: dict) -> list[dict]:
    results = []
    for bucket in config.get("s3_buckets", []):
        passed = bucket.get("public_access_blocked", False)
        detail = "Public access blocked" if passed else "Public access NOT blocked"
        results.append(_result(bucket["name"], passed, detail))
    return results


def check_iam_mfa(config: dict) -> list[dict]:
    results = []
    for user in config.get("iam_users", []):
        passed = user.get("mfa_enabled", False)
        detail = "MFA enabled" if passed else "MFA NOT enabled"
        results.append(_result(user["username"], passed, detail))
    return results


def check_sg_ssh_open(config: dict) -> list[dict]:
    results = []
    for sg in config.get("security_groups", []):
        ssh_open = any(
            rule.get("port") == 22 and rule.get("cidr") == "0.0.0.0/0"
            for rule in sg.get("ingress", [])
        )
        detail = "SSH open to the internet" if ssh_open else "No public SSH rule"
        results.append(_result(f"{sg['name']} ({sg['id']})", not ssh_open, detail))
    return results


def check_cloudtrail_enabled(config: dict) -> list[dict]:
    results = []
    for trail in config.get("cloudtrails", []):
        passed = trail.get("is_logging", False)
        detail = "Logging active" if passed else "Logging NOT active"
        results.append(_result(trail["name"], passed, detail))
    return results


# Registry: maps the name used in controls.yaml to the actual function.
CHECK_REGISTRY = {
    func.__name__: func
    for func in (
        check_s3_encryption,
        check_s3_public_access,
        check_iam_mfa,
        check_sg_ssh_open,
        check_cloudtrail_enabled,
    )
}