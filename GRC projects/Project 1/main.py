import json
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent

with (PROJECT_ROOT / "controls" / "controls.yaml").open() as f:
    controls = yaml.safe_load(f)["controls"]

with (PROJECT_ROOT / "data" / "mock_aws_config.json").open() as f:
    config = json.load(f)

print(f"Loaded {len(controls)} controls")
print(f"Loaded {len(config['s3_buckets'])} S3 buckets")

for c in controls:
    print(f"{c['id']} | {c['severity']:<8} | {c['title']}")