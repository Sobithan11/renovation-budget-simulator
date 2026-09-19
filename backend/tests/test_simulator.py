import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.project import RenovationProject
from services.simulator import run_simulation


def create_test_project():
    return RenovationProject(
        name="Test Project",
        budget=150_000,
        extension_size=36,
        kitchen_spec="standard",
        bathroom_spec="standard",
        flooring_area=20,
        painting_area=50,
        landscaping_area=30,
    )


def test_simulation_returns_10000_results():
    project = create_test_project()

    results, breakdowns = run_simulation(project, 10_000)

    assert len(results) == 10_000


def test_simulation_results_are_numeric():
    project = create_test_project()

    results, breakdowns = run_simulation(project, 10_000)

    assert isinstance(results, np.ndarray)
    assert np.issubdtype(results.dtype, np.number)


def test_simulation_costs_are_non_negative():
    project = create_test_project()

    results, breakdowns = run_simulation(project, 10_000)

    assert np.all(results >= 0)


def test_breakdowns_match_total_results():
    project = create_test_project()

    results, breakdowns = run_simulation(project, 10_000)

    breakdown_total = np.zeros(10_000)

    for values in breakdowns.values():
        breakdown_total += values

    assert np.allclose(results, breakdown_total)