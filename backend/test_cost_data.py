from models.project import RenovationProject
from services.simulator import run_simulation
from services.results import analyse_results


project = RenovationProject(
    name="Test Renovation",
    budget=150000,
    extension_size=40,
    kitchen_spec="standard",
    bathroom_spec="standard",
    flooring_area=80,
    electrical_work=True,
    plumbing_work=True,
    plastering_work=True,
    painting_work=True,
    windows_doors=4,
    landscaping_area=30,
)

results = run_simulation(project, 10_000)

print("Monte Carlo simulation completed!")
print(f"Number of simulations: {len(results)}")
print(f"Minimum simulated cost: £{results.min():,.2f}")
print(f"Maximum simulated cost: £{results.max():,.2f}")
print(f"Average simulated cost: £{results.mean():,.2f}")

analysis = analyse_results(results, project.budget)

print("\nSimulation analysis:")
print(f"Mean cost: £{analysis['mean_cost']:,.2f}")
print(f"Median cost: £{analysis['median_cost']:,.2f}")
print(f"P10: £{analysis['p10']:,.2f}")
print(f"P90: £{analysis['p90']:,.2f}")
print(
    f"Probability of exceeding budget: "
    f"{analysis['over_budget_probability'] * 100:.2f}%"
)
print(
    f"Probability of staying within budget: "
    f"{analysis['under_budget_probability'] * 100:.2f}%"
)