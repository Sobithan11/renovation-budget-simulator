import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.project import RenovationProject
from services.cost_model import calculate_project_cost_breakdown


def test_extension_cost_is_generated():
    project = RenovationProject(
        name="Test Project",
        budget=150_000,
        extension_size=36,
        kitchen_spec="none",
        bathroom_spec="none",
    )

    breakdown = calculate_project_cost_breakdown(project)

    assert breakdown["extension"] > 0


def test_kitchen_cost_is_generated_for_valid_spec():
    project = RenovationProject(
        name="Test Project",
        budget=150_000,
        kitchen_spec="standard",
        bathroom_spec="none",
    )

    breakdown = calculate_project_cost_breakdown(project)

    assert breakdown["kitchen"] > 0


def test_kitchen_none_has_zero_cost():
    project = RenovationProject(
        name="Test Project",
        budget=150_000,
        kitchen_spec="none",
        bathroom_spec="none",
    )

    breakdown = calculate_project_cost_breakdown(project)

    assert breakdown["kitchen"] == 0.0


def test_bathroom_cost_is_generated_for_valid_spec():
    project = RenovationProject(
        name="Test Project",
        budget=150_000,
        kitchen_spec="none",
        bathroom_spec="standard",
    )

    breakdown = calculate_project_cost_breakdown(project)

    assert breakdown["bathroom"] > 0


def test_flooring_cost_is_generated_for_positive_area():
    project = RenovationProject(
        name="Test Project",
        budget=150_000,
        kitchen_spec="none",
        bathroom_spec="none",
        flooring_area=20,
    )

    breakdown = calculate_project_cost_breakdown(project)

    assert breakdown["flooring"] > 0


def test_painting_cost_is_generated_for_positive_area():
    project = RenovationProject(
        name="Test Project",
        budget=150_000,
        kitchen_spec="none",
        bathroom_spec="none",
        painting_area=50,
    )

    breakdown = calculate_project_cost_breakdown(project)

    assert breakdown["painting"] > 0


def test_zero_area_work_has_zero_cost():
    project = RenovationProject(
        name="Test Project",
        budget=150_000,
        kitchen_spec="none",
        bathroom_spec="none",
        flooring_area=0,
        painting_area=0,
        landscaping_area=0,
    )

    breakdown = calculate_project_cost_breakdown(project)

    assert breakdown["flooring"] == 0.0
    assert breakdown["painting"] == 0.0
    assert breakdown["landscaping"] == 0.0