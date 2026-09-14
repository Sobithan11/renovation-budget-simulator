import numpy as np


def analyse_results(results, budget):
    mean_cost = np.mean(results)
    median_cost = np.median(results)

    p10 = np.percentile(results, 10)
    p90 = np.percentile(results, 90)

    over_budget_probability = np.mean(results > budget)
    under_budget_probability = np.mean(results <= budget)

    return {
        "mean_cost": float(mean_cost),
        "median_cost": float(median_cost),
        "p10": float(p10),
        "p90": float(p90),
        "over_budget_probability": float(over_budget_probability),
        "under_budget_probability": float(under_budget_probability),
    }