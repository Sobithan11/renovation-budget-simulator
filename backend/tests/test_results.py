import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.results import analyse_results


def test_mean_and_median_are_calculated_correctly():
    results = np.array([100, 200, 300, 400, 500])

    analysis = analyse_results(
        results,
        budget=350,
    )

    assert analysis["mean_cost"] == 300.0
    assert analysis["median_cost"] == 300.0


def test_percentiles_are_in_correct_order():
    results = np.arange(1, 101)

    analysis = analyse_results(
        results,
        budget=50,
    )

    assert analysis["p10"] < analysis["median_cost"]
    assert analysis["median_cost"] < analysis["p90"]


def test_budget_probabilities_are_between_zero_and_one():
    results = np.array([100, 200, 300, 400, 500])

    analysis = analyse_results(
        results,
        budget=300,
    )

    assert 0 <= analysis["over_budget_probability"] <= 1
    assert 0 <= analysis["under_budget_probability"] <= 1


def test_budget_probabilities_sum_to_one():
    results = np.array([100, 200, 300, 400, 500])

    analysis = analyse_results(
        results,
        budget=300,
    )

    total_probability = (
        analysis["over_budget_probability"]
        + analysis["under_budget_probability"]
    )

    assert total_probability == 1.0


def test_distribution_is_generated():
    results = np.arange(1, 101)

    analysis = analyse_results(
        results,
        budget=50,
    )

    assert "distribution" in analysis
    assert len(analysis["distribution"]) > 0

    for point in analysis["distribution"]:
        assert "cost" in point
        assert "count" in point