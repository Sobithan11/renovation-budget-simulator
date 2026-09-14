import numpy as np

from services.cost_model import calculate_project_cost


def run_simulation(project, simulations=10_000):
    results = np.empty(simulations)

    for i in range(simulations):
        results[i] = calculate_project_cost(project)

    return results