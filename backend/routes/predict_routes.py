from flask import Blueprint, request, jsonify
import os
import numpy as np
import joblib

from routes.auth_routes import get_current_user_id_from_request

predict_bp = Blueprint("predict", __name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "random_forest.pkl")


def calc_bmi(weight_kg: float, height_cm: float) -> float:
    h_m = height_cm / 100.0
    return weight_kg / (h_m * h_m)


def validate_inputs(weight, height, steps, water_intake, sleep_hours):
    # type checks
    if weight is None or height is None or steps is None or water_intake is None or sleep_hours is None:
        return "Missing one or more required fields."

    # no negatives
    if weight <= 0 or height <= 0 or steps < 0 or water_intake < 0 or sleep_hours < 0:
        return "Negative or zero values are not allowed (weight/height must be > 0)."

    # realistic ranges (you can adjust)
    if not (30 <= weight <= 250):
        return "Weight out of realistic range (30–250 kg)."
    if not (120 <= height <= 230):
        return "Height out of realistic range (120–230 cm)."
    if not (0 <= steps <= 50000):
        return "Steps out of realistic range (0–50000)."
    if not (0 <= water_intake <= 10):
        return "Water intake out of realistic range (0–10 liters)."
    if not (0 <= sleep_hours <= 16):
        return "Sleep hours out of realistic range (0–16 hours)."

    return None


def generate_recommendations(weight, height, steps, water_intake, sleep_hours, bmi, risk_label):
    """Return a list of short, actionable recommendations based on inputs and risk."""
    recs = []

    # BMI category
    if bmi < 18.5:
        bmi_cat = "Underweight"
        recs.append(f"Your BMI is {bmi:.1f} ({bmi_cat}). Consider a nutrient-dense diet and consult a provider if unintentional weight loss.")
    elif bmi < 25:
        bmi_cat = "Normal"
        recs.append(f"Your BMI is {bmi:.1f} ({bmi_cat}). Keep up balanced nutrition and regular activity to maintain this range.")
    elif bmi < 30:
        bmi_cat = "Overweight"
        recs.append(f"Your BMI is {bmi:.1f} ({bmi_cat}). Aim for gradual weight loss (0.5–1 kg/week) through diet and activity changes.")
    else:
        bmi_cat = "Obese"
        recs.append(f"Your BMI is {bmi:.1f} ({bmi_cat}). See a healthcare provider for a personalized plan; small consistent changes can help.")

    # Steps recommendations
    if steps < 3000:
        recs.append("Increase daily physical activity: start with short walks and aim to add 500–1,000 steps/day each week until reaching 7,000–10,000 steps.")
    elif steps < 7000:
        recs.append("Good activity level — try to increase to 7,000–10,000 steps/day or add structured aerobic sessions 3×/week.")
    else:
        recs.append("Great job on your activity — maintain this and include strength training 2×/week for overall health.")

    # Sleep recommendations
    if sleep_hours < 6:
        recs.append("Improve sleep: aim for 7–9 hours nightly, establish a consistent bedtime, and minimize screens before bed.")
    elif sleep_hours > 9:
        recs.append("You sleep more than typical recommendations; if you feel excessively tired despite long sleep, discuss with your provider.")
    else:
        recs.append("Your sleep duration is in the healthy range — keep consistent sleep routines for recovery and metabolism.")

    # Water intake
    if water_intake < 1.5:
        recs.append("Increase hydration toward ~2 liters/day (adjust for activity/heat); carry a water bottle and sip regularly.")
    elif water_intake > 4:
        recs.append("Your reported water intake is high — ensure this is intentional and consider medical advice if very high or if experiencing symptoms.")
    else:
        recs.append("Hydration looks adequate — continue targeting about 2–3 liters depending on activity.")

    # Risk-based closing suggestions
    if risk_label == "High":
        recs.append("High risk: schedule a check-up with your healthcare provider; consider working with a dietitian or exercise professional for a personalized plan.")
    elif risk_label == "Medium":
        recs.append("Medium risk: adopt the suggested lifestyle changes and re-check progress in 4–8 weeks; small consistent changes make a difference.")
    else:
        recs.append("Low risk: continue healthy habits and monitor weight, activity, and sleep periodically.")

    return recs


@predict_bp.route("/health/predict", methods=["POST"])
def predict_health_risk():
    """
    POST /health/predict
    JSON:
    {
      "weight": 70.5,
      "height": 170,
      "steps": 8000,
      "water_intake": 2.5,
      "sleep_hours": 7.0
    }
    """
    user_id = get_current_user_id_from_request()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}

    try:
        weight = float(data.get("weight"))
        height = float(data.get("height"))
        steps = int(data.get("steps"))
        water_intake = float(data.get("water_intake"))
        sleep_hours = float(data.get("sleep_hours"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid data types. Use numbers only."}), 400

    err = validate_inputs(weight, height, steps, water_intake, sleep_hours)
    if err:
        return jsonify({"error": err}), 400

    bmi = calc_bmi(weight, height)

    # Features must match training order:
    # ["weight", "height", "bmi", "steps", "water_intake", "sleep_hours"]
    X = np.array([[weight, height, bmi, steps, water_intake, sleep_hours]], dtype=float)

    if not os.path.exists(MODEL_PATH):
        return jsonify({"error": "Model not found. Train the model first."}), 500

    # If the file exists but is empty/corrupted, return a helpful error
    try:
        if os.path.getsize(MODEL_PATH) == 0:
            return jsonify({"error": "Model file is empty or corrupted. Run 'backend/ml/train_model_rf.py' to regenerate the model."}), 500
    except OSError:
        # Fall back to joblib.load which will raise an import/load error if needed
        pass

    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    le = bundle["label_encoder"]

    pred_class = model.predict(X)[0]
    risk_label = le.inverse_transform([pred_class])[0]

    # Optional: show probability confidence
    probs = None
    if hasattr(model, "predict_proba"):
        p = model.predict_proba(X)[0]
        probs = {cls: float(p[i]) for i, cls in enumerate(le.classes_)}

    # Generate real-world, actionable recommendations
    recommendations = generate_recommendations(weight, height, steps, water_intake, sleep_hours, bmi, risk_label)

    return jsonify({
        "risk_label": risk_label,
        "bmi": round(float(bmi), 2),
        "probabilities": probs,
        "inputs": {
            "weight": weight,
            "height": height,
            "steps": steps,
            "water_intake": water_intake,
            "sleep_hours": sleep_hours
        },
        "used_model": os.path.basename(MODEL_PATH),
        "recommendations": recommendations
    }), 200
