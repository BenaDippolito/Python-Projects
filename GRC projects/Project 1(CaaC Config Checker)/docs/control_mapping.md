# Control-to-Check Traceability Matrix

_Generated from `controls/controls.yaml`. Do not edit by hand._

| Control ID | Title | Severity | NIST 800-53 | CIS Ref | Check function |
|---|---|---|---|---|---|
| GRC-001 | S3 buckets must have encryption at rest enabled | high | SC-28 | 2.1.1 | `check_s3_encryption` |
| GRC-002 | S3 buckets must block public access | critical | AC-3 | 2.1.5 | `check_s3_public_access` |
| GRC-003 | All IAM users must have MFA enabled | high | IA-2(1) | 1.1 | `check_iam_mfa` |
| GRC-004 | Security groups must not allow SSH from the internet | critical | SC-7 | 5.2 | `check_sg_ssh_open` |
| GRC-005 | CloudTrail logging must be enabled | high | AU-12 | 3.1 | `check_cloudtrail_enabled` |
