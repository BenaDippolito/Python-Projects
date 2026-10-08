"""Check functions: one per control.

Every check takes the full config dict and returns a list of
resource-level results, so an auditor can see exactly WHICH
resources failed, not just that "something" failed.
"""
import ipaddress

# Build the common result shape returned by every resource-level check.
def _result(resource: str, passed: bool, detail: str) -> dict:
    return {"resource": resource, "passed": passed, "detail": detail}


def check_s3_encryption(config: dict) -> list[dict]:
    # Evaluate encryption at rest for each S3 bucket; missing evidence fails closed.
    results = []
    for bucket in config.get("s3_buckets", []):
        passed = bucket.get("encrypted", False)
        detail = "Encryption enabled" if passed else "Encryption NOT enabled"
        results.append(_result(bucket["name"], passed, detail))
    return results


def check_s3_public_access(config: dict) -> list[dict]:
    # Confirm that every S3 bucket has its public-access block enabled.
    results = []
    for bucket in config.get("s3_buckets", []):
        passed = bucket.get("public_access_blocked", False)
        detail = "Public access blocked" if passed else "Public access NOT blocked"
        results.append(_result(bucket["name"], passed, detail))
    return results


def check_iam_mfa(config: dict) -> list[dict]:
    # Verify that each IAM user has multi-factor authentication enabled.
    results = []
    for user in config.get("iam_users", []):
        passed = user.get("mfa_enabled", False)
        detail = "MFA enabled" if passed else "MFA NOT enabled"
        results.append(_result(user["username"], passed, detail))
    return results

def _is_open_to_internet(cidr) -> bool:
    # True for any "match everything" network, IPv4 or IPv6.
    # Unparseable or missing values fail closed (treated as open).
    try:
        return ipaddress.ip_network(cidr, strict=False).prefixlen == 0
    except (ValueError, TypeError):
        return True

def check_sg_ssh_open(config: dict) -> list[dict]:
    # Flag security groups exposing SSH to the whole internet (IPv4 or IPv6).
    results = []
    for sg in config.get("security_groups", []):
        ssh_open = any(
            rule.get("port") == 22 and _is_open_to_internet(rule.get("cidr"))
            for rule in sg.get("ingress", [])
        )
        detail = "SSH open to the internet" if ssh_open else "No public SSH rule"
        results.append(_result(f"{sg['name']} ({sg['id']})", not ssh_open, detail))
    return results

def check_cloudtrail_enabled(config: dict) -> list[dict]:
    # Confirm that each CloudTrail trail is actively recording events.
    results = []
    for trail in config.get("cloudtrails", []):
        passed = trail.get("is_logging", False)
        detail = "Logging active" if passed else "Logging NOT active"
        results.append(_result(trail["name"], passed, detail))
    return results


# Registry: maps names from controls.yaml to the deliberately allowed functions.
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