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

    required_fields = ["name", "budget"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({"error": "Name must be a non-empty string"}), 400

    if not isinstance(data["budget"], (int, float)) or data["budget"] <= 0:
        return jsonify({"error": "Budget must be a positive number"}), 400

    project = RenovationProject(
        name=data["name"],
        budget=data["budget"],
        extension_size=data.get("extension_size", 0),
        kitchen_spec=data.get("kitchen_spec", "standard"),
        bathroom_spec=data.get("bathroom_spec", "standard"),
        flooring_area=data.get("flooring_area", 0),
        electrical_work=data.get("electrical_work", False),
        plumbing_work=data.get("plumbing_work", False),
        plastering_work=data.get("plastering_work", False),
        painting_work=data.get("painting_work", False),
        windows_doors=data.get("windows_doors", 0),
        structural_work=data.get("structural_work", False),
        roofing_work=data.get("roofing_work", False),
        landscaping_area=data.get("landscaping_area", 0),
    )

    results = run_simulation(project, 10_000)

    analysis = analyse_results(results, project.budget)

    return jsonify(analysis)