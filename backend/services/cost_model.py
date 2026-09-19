import json
from pathlib import Path

import numpy as np


DATA_FILE = Path(__file__).parent.parent / "data" / "cost_data.json"


def load_cost_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def sample_cost(category, simulations=1, option=None):
    cost_data = load_cost_data()
    category_data = cost_data[category]

    if option is not None:
        category_data = category_data["options"][option]

    minimum = category_data["minimum"]
    typical = category_data["typical"]
    maximum = category_data["maximum"]

    return np.random.triangular(
        minimum,
        typical,
        maximum,
        simulations
    )


def calculate_project_cost(project):
    total_cost = 0.0

    # Extension
    if project.extension_size > 0:
        extension_rate = sample_cost("extension")[0]
        total_cost += extension_rate * project.extension_size

    # Kitchen
    if project.kitchen_spec != "none":
        total_cost += sample_cost(
            "kitchen",
            option=project.kitchen_spec
        )[0]

    # Bathroom
    if project.bathroom_spec != "none":
        total_cost += sample_cost(
            "bathroom",
            option=project.bathroom_spec
        )[0]

    # Flooring
    if project.flooring_area > 0:
        flooring_rate = sample_cost("flooring")[0]
        total_cost += flooring_rate * project.flooring_area

    # Landscaping
    if project.landscaping_area > 0:
        landscaping_rate = sample_cost("landscaping")[0]
        total_cost += landscaping_rate * project.landscaping_area

    # Additional standalone work
    if project.extension_size == 0:

        if project.electrical_work:
            total_cost += sample_cost("electrical")[0]

        if project.plumbing_work:
            total_cost += sample_cost("plumbing")[0]

        if project.plastering_work:
            total_cost += sample_cost("plastering")[0]

        if project.painting_work:
            total_cost += sample_cost("painting")[0]

        if project.windows_doors > 0:
            window_door_cost = sample_cost("windows_doors")[0]
            total_cost += window_door_cost * project.windows_doors

    return total_cost


def calculate_project_cost_breakdown(project):
    breakdown = {}

    # Extension
    if project.extension_size > 0:
        extension_rate = sample_cost("extension")[0]
        breakdown["extension"] = extension_rate * project.extension_size
    else:
        breakdown["extension"] = 0.0

    # Kitchen
    if project.kitchen_spec != "none":
        breakdown["kitchen"] = sample_cost(
            "kitchen",
            option=project.kitchen_spec
        )[0]
    else:
        breakdown["kitchen"] = 0.0

    # Bathroom
    if project.bathroom_spec != "none":
        breakdown["bathroom"] = sample_cost(
            "bathroom",
            option=project.bathroom_spec
        )[0]
    else:
        breakdown["bathroom"] = 0.0

    # Flooring
    if project.flooring_area > 0:
        flooring_rate = sample_cost("flooring")[0]
        breakdown["flooring"] = flooring_rate * project.flooring_area
    else:
        breakdown["flooring"] = 0.0

    # Landscaping
    if project.landscaping_area > 0:
        landscaping_rate = sample_cost("landscaping")[0]
        breakdown["landscaping"] = (
            landscaping_rate * project.landscaping_area
        )
    else:
        breakdown["landscaping"] = 0.0

    # Standalone work
    if project.extension_size == 0:

        if project.electrical_work:
            breakdown["electrical"] = sample_cost("electrical")[0]
        else:
            breakdown["electrical"] = 0.0

        if project.plumbing_work:
            breakdown["plumbing"] = sample_cost("plumbing")[0]
        else:
            breakdown["plumbing"] = 0.0

        if project.plastering_work:
            breakdown["plastering"] = sample_cost("plastering")[0]
        else:
            breakdown["plastering"] = 0.0

        if project.painting_work:
            breakdown["painting"] = sample_cost("painting")[0]
        else:
            breakdown["painting"] = 0.0

        if project.windows_doors > 0:
            window_door_cost = sample_cost("windows_doors")[0]
            breakdown["windows_doors"] = (
                window_door_cost * project.windows_doors
            )
        else:
            breakdown["windows_doors"] = 0.0

    return breakdown