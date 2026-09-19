import numpy as np

from services.cost_model import calculate_project_cost_breakdown


def run_simulation(project, simulations=10_000):
    results = np.empty(simulations)

    categories = [
        "extension",
        "kitchen",
        "bathroom",
        "flooring",
        "landscaping",
        "electrical",
        "plumbing",
        "plastering",
        "painting",
        "windows_doors",
    ]

    breakdowns = {
        category: np.zeros(simulations)
        for category in categories
    }

    for i in range(simulations):
        breakdown = calculate_project_cost_breakdown(project)

        total_cost = sum(breakdown.values())

        results[i] = total_cost

        for category in categories:
            breakdowns[category][i] = breakdown.get(category, 0.0)

    return results, breakdowns