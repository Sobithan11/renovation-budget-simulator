import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_simulate_valid_request(client):
    response = client.post(
        "/simulate",
        json={
            "name": "Test Project",
            "budget": 150_000,
            "extension_size": 36,
            "kitchen_spec": "standard",
            "bathroom_spec": "standard",
            "flooring_area": 20,
            "painting_area": 50,
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "mean_cost" in data
    assert "median_cost" in data
    assert "p10" in data
    assert "p90" in data
    assert "over_budget_probability" in data
    assert "under_budget_probability" in data
    assert "distribution" in data
    assert "cost_breakdown" in data


def test_simulate_missing_budget_returns_400(client):
    response = client.post(
        "/simulate",
        json={
            "name": "Test Project",
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data


def test_simulate_negative_extension_returns_400(client):
    response = client.post(
        "/simulate",
        json={
            "name": "Test Project",
            "budget": 150_000,
            "extension_size": -20,
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == (
        "extension_size must be a non-negative number"
    )


def test_simulate_negative_painting_area_returns_400(client):
    response = client.post(
        "/simulate",
        json={
            "name": "Test Project",
            "budget": 150_000,
            "painting_area": -50,
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == (
        "painting_area must be a non-negative number"
    )


def test_simulate_invalid_kitchen_spec_returns_400(client):
    response = client.post(
        "/simulate",
        json={
            "name": "Test Project",
            "budget": 150_000,
            "kitchen_spec": "luxury",
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid kitchen_spec"


def test_simulate_negative_budget_returns_400(client):
    response = client.post(
        "/simulate",
        json={
            "name": "Test Project",
            "budget": -100_000,
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Budget must be a positive number"