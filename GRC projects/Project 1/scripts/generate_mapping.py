"""Generate docs/control_mapping.md from controls/controls.yaml."""
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent

with open(PROJECT_ROOT / "controls" / "controls.yaml") as f:
    controls = yaml.safe_load(f)["controls"]

lines = [
    "# Control-to-Check Traceability Matrix",
    "",
    "_Generated from `controls/controls.yaml`. Do not edit by hand._",
    "",
    "| Control ID | Title | Severity | NIST 800-53 | CIS Ref | Check function |",
    "|---|---|---|---|---|---|",
]
for c in controls:
    cis = c.get("cis_ref") or "TBD"
    lines.append(
        f"| {c['id']} | {c['title']} | {c['severity']} | "
        f"{c['nist_80053']} | {cis} | `{c['check']}` |"
    )

out = PROJECT_ROOT / "docs" / "control_mapping.md"
out.parent.mkdir(exist_ok=True)
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {out.relative_to(PROJECT_ROOT)}")