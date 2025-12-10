from flask import Blueprint, request, jsonify
from models.predictor import get_predictor

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/health/predict", methods=["POST"])
def predict_health_risk():
    """
    Predict health risk.

    Expected JSON:
    {
        "weight": 70.5,
        "steps": 8000,
        "water_intake": 2.5,
        "sleep_hours": 7.0
    }
    """
    data = request.get_json() or {}

    required = ["weight", "steps", "water_intake", "sleep_hours"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing field(s): {', '.join(missing)}"}), 400

    try:
        weight = float(data["weight"])
        steps = int(data["steps"])
        water_intake = float(data["water_intake"])
        sleep_hours = float(data["sleep_hours"])
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid data types"}), 400

    predictor = get_predictor()
    result = predictor.predict(weight, steps, water_intake, sleep_hours)

    return jsonify(result), 200
