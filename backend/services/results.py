import numpy as np


def analyse_results(results, budget, breakdowns=None):
    mean_cost = np.mean(results)
    median_cost = np.median(results)

    p10 = np.percentile(results, 10)
    p90 = np.percentile(results, 90)

    over_budget_probability = np.mean(results > budget)
    under_budget_probability = np.mean(results <= budget)

    # Create histogram data for the cost distribution chart.
    counts, bin_edges = np.histogram(results, bins=20)

    distribution = []

    for i in range(len(counts)):
        distribution.append({
            "cost": float(
                (bin_edges[i] + bin_edges[i + 1]) / 2
            ),
            "count": int(counts[i]),
        })

    analysis = {
        "mean_cost": float(mean_cost),
        "median_cost": float(median_cost),
        "p10": float(p10),
        "p90": float(p90),
        "over_budget_probability": float(over_budget_probability),
        "under_budget_probability": float(under_budget_probability),
        "distribution": distribution,
    }

    if breakdowns is not None:
        cost_breakdown = []

        for category, values in breakdowns.items():
            average_cost = np.mean(values)

            if average_cost > 0:
                cost_breakdown.append({
                    "category": category,
                    "average_cost": float(average_cost),
                })

        cost_breakdown.sort(
            key=lambda item: item["average_cost"],
            reverse=True
        )

        analysis["cost_breakdown"] = cost_breakdown

    return analysis