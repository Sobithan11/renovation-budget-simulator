from flask import Blueprint, request, jsonify

from models.project import RenovationProject
from services.simulator import run_simulation
from services.results import analyse_results

simulation_bp = Blueprint("simulation", __name__)


@simulation_bp.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    # Required fields
    if "name" not in data:
        return jsonify({"error": "Missing required field: name"}), 400

    if "budget" not in data:
        return jsonify({"error": "Missing required field: budget"}), 400

    # Basic project validation
    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({"error": "Name must be a non-empty string"}), 400

    if (
        not isinstance(data["budget"], (int, float))
        or isinstance(data["budget"], bool)
        or data["budget"] <= 0
    ):
        return jsonify({"error": "Budget must be a positive number"}), 400

    # Numeric fields that cannot be negative
    non_negative_fields = [
        "extension_size",
        "flooring_area",
        "painting_area",
        "landscaping_area",
        "windows_doors",
    ]

    for field in non_negative_fields:
        value = data.get(field, 0)

        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or value < 0
        ):
            return jsonify({
                "error": f"{field} must be a non-negative number"
            }), 400

    # Windows and doors must be a whole number
    windows_doors = data.get("windows_doors", 0)

    if not isinstance(windows_doors, int) or isinstance(windows_doors, bool):
        return jsonify({
            "error": "windows_doors must be a non-negative integer"
        }), 400

    # Valid specification options
    valid_specs = {"none", "budget", "standard", "high"}

    kitchen_spec = data.get("kitchen_spec", "standard")
    bathroom_spec = data.get("bathroom_spec", "standard")

    if kitchen_spec not in valid_specs:
        return jsonify({
            "error": "Invalid kitchen_spec"
        }), 400

    if bathroom_spec not in valid_specs:
        return jsonify({
            "error": "Invalid bathroom_spec"
        }), 400

    project = RenovationProject(
        name=data["name"],
        budget=data["budget"],
        extension_size=data.get("extension_size", 0),
        kitchen_spec=kitchen_spec,
        bathroom_spec=bathroom_spec,
        flooring_area=data.get("flooring_area", 0),
        electrical_work=data.get("electrical_work", False),
        plumbing_work=data.get("plumbing_work", False),
        plastering_work=data.get("plastering_work", False),
        painting_area=data.get("painting_area", 0),
        windows_doors=windows_doors,
        structural_work=data.get("structural_work", False),
        roofing_work=data.get("roofing_work", False),
        landscaping_area=data.get("landscaping_area", 0),
    )

    results, breakdowns = run_simulation(project, 10_000)

    analysis = analyse_results(
        results,
        project.budget,
        breakdowns
    )

    return jsonify(analysis)