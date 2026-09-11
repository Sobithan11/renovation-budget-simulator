import json
from pathlib import Path

import numpy as np


DATA_FILE = Path(__file__).parent.parent / "data" / "cost_data.json"


def load_cost_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def sample_cost(category, simulations=1):
    cost_data = load_cost_data()
    category_data = cost_data[category]

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

    if project.extension_size > 0:
        extension_rate = sample_cost("extension")[0]
        total_cost += extension_rate * project.extension_size

    if project.flooring_area > 0:
        flooring_rate = sample_cost("flooring")[0]
        total_cost += flooring_rate * project.flooring_area

    if project.landscaping_area > 0:
        landscaping_rate = sample_cost("landscaping")[0]
        total_cost += landscaping_rate * project.landscaping_area

    if project.windows_doors > 0:
        window_door_cost = sample_cost("windows_doors")[0]
        total_cost += window_door_cost * project.windows_doors

    if project.kitchen_spec != "none":
        total_cost += sample_cost("kitchen")[0]

    if project.bathroom_spec != "none":
        total_cost += sample_cost("bathroom")[0]

    if project.electrical_work:
        total_cost += sample_cost("electrical")[0]

    if project.plumbing_work:
        total_cost += sample_cost("plumbing")[0]

    if project.plastering_work:
        plastering_rate = sample_cost("plastering")[0]

        # Temporary area assumption; we'll improve the project
        # inputs later.
        total_cost += plastering_rate * project.extension_size

    if project.painting_work:
        painting_rate = sample_cost("painting")[0]

        # Temporary area assumption; we'll improve the project
        # inputs later.
        total_cost += painting_rate * project.extension_size

    return total_cost