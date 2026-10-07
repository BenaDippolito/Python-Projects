import json
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def mock_config() -> dict:
    with open(PROJECT_ROOT / "data" / "mock_aws_config.json") as f:
        return json.load(f)


@pytest.fixture
def controls() -> list[dict]:
    with open(PROJECT_ROOT / "controls" / "controls.yaml") as f:
        return yaml.safe_load(f)["controls"]