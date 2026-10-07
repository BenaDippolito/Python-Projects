import json
import yaml

with open("controls/controls.yaml") as f:
    controls = yaml.safe_load(f)["controls"]

with open("data/mock_aws_config.json") as f:
    config = json.load(f)

print(f"Loaded {len(controls)} controls")
print(f"Loaded {len(config['s3_buckets'])} S3 buckets")

for c in controls:
    print(f"{c['id']} | {c['severity']:<8} | {c['title']}")