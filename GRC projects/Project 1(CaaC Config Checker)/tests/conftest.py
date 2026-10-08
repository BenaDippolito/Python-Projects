# Shared pytest fixtures and standard-library helpers.
import json
from pathlib import Path

import pytest
import yaml

# Resolve fixtures relative to the project instead of the test process cwd.
PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def mock_config() -> dict:
    # Provide the sample cloud configuration used by integration-style tests.
    with open(PROJECT_ROOT / "data" / "mock_aws_config.json") as f:
        return json.load(f)


@pytest.fixture
def controls() -> list[dict]:
    # Provide the YAML policy definitions used by engine and report tests.
    with open(PROJECT_ROOT / "controls" / "controls.yaml") as f:
        return yaml.safe_load(f)["controls"]