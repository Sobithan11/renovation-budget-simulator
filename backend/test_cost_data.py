from services.cost_model import load_cost_data, sample_cost


cost_data = load_cost_data()

print("Cost data loaded successfully!")
print(f"Categories: {list(cost_data.keys())}")

samples = sample_cost("flooring", 10)

print("\n10 simulated flooring costs:")
for cost in samples:
    print(f"£{cost:.2f}")