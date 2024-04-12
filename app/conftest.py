import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """Fixture to provide a test client."""
    return TestClient(app)


@pytest.fixture()
def sample_tax_brackets() -> dict:
    """Fixture to provide sample tax brackets data."""
    return {
        "tax_brackets": [
            {"max": 50197, "min": 0, "rate": 0.15},
            {"max": 100392, "min": 50197, "rate": 0.205},
            {"max": 155625, "min": 100392, "rate": 0.26},
            {"max": 221708, "min": 155625, "rate": 0.29},
            {"min": 221708, "rate": 0.33},
        ]
    }


@pytest.fixture()
def sample_tax_calculation() -> dict:
    """Fixture to provide sample tax calculation response."""
    return {
        "total_taxes": 385587.65,
        "taxes_per_band": {
            "0 to 50197": 7529.55,
            "50197 to 100392": 10289.97,
            "100392 to 155625": 14360.58,
            "155625 to 221708": 19164.07,
            "More than 221708": 334243.47,
        },
        "effective_rate": 31.23,
    }
