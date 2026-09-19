from flask import Blueprint, request, jsonify

from database import get_connection
from models.project import RenovationProject
from services.simulator import run_simulation
from services.results import analyse_results

projects_bp = Blueprint("projects", __name__)


@projects_bp.route("/projects", methods=["POST"])
def create_project():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing required field: name"}), 400

    if "budget" not in data:
        return jsonify({"error": "Missing required field: budget"}), 400

    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({"error": "Name must be a non-empty string"}), 400

    if not isinstance(data["budget"], (int, float)) or data["budget"] <= 0:
        return jsonify({"error": "Budget must be a positive number"}), 400

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO projects (
            name,
            budget,
            extension_size,
            kitchen_spec,
            bathroom_spec,
            flooring_area,
            electrical_work,
            plumbing_work,
            plastering_work,
            painting_work,
            windows_doors,
            structural_work,
            roofing_work,
            landscaping_area
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["name"],
            data["budget"],
            data.get("extension_size", 0),
            data.get("kitchen_spec", "standard"),
            data.get("bathroom_spec", "standard"),
            data.get("flooring_area", 0),
            data.get("electrical_work", False),
            data.get("plumbing_work", False),
            data.get("plastering_work", False),
            data.get("painting_work", False),
            data.get("windows_doors", 0),
            data.get("structural_work", False),
            data.get("roofing_work", False),
            data.get("landscaping_area", 0),
        ),
    )

    connection.commit()

    project_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Project created successfully",
        "project_id": project_id
    }), 201

@projects_bp.route("/projects", methods=["GET"])
def get_projects():
    connection = get_connection()

    projects = connection.execute(
        "SELECT * FROM projects ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return jsonify([dict(project) for project in projects])

@projects_bp.route("/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    connection = get_connection()

    project = connection.execute(
        "SELECT * FROM projects WHERE id = ?",
        (project_id,)
    ).fetchone()

    connection.close()

    if project is None:
        return jsonify({"error": "Project not found"}), 404

    return jsonify(dict(project))

@projects_bp.route("/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,)
    )

    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Project not found"}), 404

    return jsonify({
        "message": "Project deleted successfully"
    })

@projects_bp.route("/projects/<int:project_id>/simulate", methods=["POST"])
def simulate_project(project_id):
    connection = get_connection()

    project = connection.execute(
        "SELECT * FROM projects WHERE id = ?",
        (project_id,)
    ).fetchone()

    connection.close()

    if project is None:
        return jsonify({"error": "Project not found"}), 404

    project = RenovationProject(
        name=project["name"],
        budget=project["budget"],
        extension_size=project["extension_size"],
        kitchen_spec=project["kitchen_spec"],
        bathroom_spec=project["bathroom_spec"],
        flooring_area=project["flooring_area"],
        electrical_work=bool(project["electrical_work"]),
        plumbing_work=bool(project["plumbing_work"]),
        plastering_work=bool(project["plastering_work"]),
        painting_work=bool(project["painting_work"]),
        windows_doors=project["windows_doors"],
        structural_work=bool(project["structural_work"]),
        roofing_work=bool(project["roofing_work"]),
        landscaping_area=project["landscaping_area"],
    )

    results, breakdowns = run_simulation(project, 10_000)

    analysis = analyse_results(
        results,
        project.budget,
        breakdowns
    )

    return jsonify({
        "project_id": project_id,
        "project_name": project.name,
        "budget": project.budget,
        **analysis
    })