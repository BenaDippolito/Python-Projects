# Import the allow-listed control checks referenced by the YAML policy.
from checker.checks import CHECK_REGISTRY


class ComplianceEngine:
    """Runs every control against a config and collects structured results."""

    def __init__(self, controls: list[dict], config: dict):
        # Keep the policy definitions and configuration snapshot for the scan.
        self.controls = controls
        self.config = config

    def run_control(self, control: dict) -> dict:
        # Initialize stable metadata and result fields for one control.
        result = {
            "control_id": control["id"],
            "title": control["title"],
            "severity": control["severity"],
            "nist_80053": control.get("nist_80053", ""),
            "cis_ref": control.get("cis_ref", ""),
            "status": None,
            "resources_checked": 0,
            "failures": [],
            "error": None,
        }

        # Resolve only registered check names so configuration cannot invoke
        # arbitrary code.
        check_func = CHECK_REGISTRY.get(control["check"])
        if check_func is None:
            result["status"] = "ERROR"
            result["error"] = f"No check function named '{control['check']}'"
            return result

        # Isolate a broken check as an ERROR so the remaining controls can run.
        try:
            resource_results = check_func(self.config)
        except Exception as exc:  # one broken check shouldn't stop the whole scan
            result["status"] = "ERROR"
            result["error"] = f"{type(exc).__name__}: {exc}"
            return result

        # Separate failed resources from the complete set checked.
        result["resources_checked"] = len(resource_results)
        result["failures"] = [r for r in resource_results if not r["passed"]]

        # Classify the control based on scope and resource-level outcomes.
        if not resource_results:
            result["status"] = "N/A"
        elif result["failures"]:
            result["status"] = "FAIL"
        else:
            result["status"] = "PASS"

        return result

    def run_all(self) -> list[dict]:
        # Preserve control order while evaluating the complete policy set.
        return [self.run_control(c) for c in self.controls]