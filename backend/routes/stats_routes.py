from flask import Blueprint, request, jsonify
from database import get_connection
from routes.auth_routes import get_current_user_id_from_request

stats_bp = Blueprint("stats", __name__)


def _to_float(x):
    try:
        if x is None or x == "":
            return None
        return float(x)
    except (TypeError, ValueError):
        return None


def _to_int(x):
    try:
        if x is None or x == "":
            return None
        return int(float(x))
    except (TypeError, ValueError):
        return None


def _avg(values):
    return sum(values) / len(values) if values else None


@stats_bp.route("/health/stats", methods=["GET"])
def get_health_stats():
    days = request.args.get("days", default=7, type=int)

    user_id = get_current_user_id_from_request()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT entry_date, weight, steps, water_intake, sleep_hours
        FROM health_logs
        WHERE user_id = ?
        ORDER BY entry_date DESC
        LIMIT ?
        """,
        (user_id, days),
    )
    rows = cur.fetchall()
    conn.close()

    data = [dict(r) for r in rows]
    data = list(reversed(data))  # chronological order

    if not data:
        return jsonify({
            "weight_trend": [],
            "steps_trend": [],
            "summary": {
                "data_points": 0,
            }
        }), 200

    # Numeric collections
    weights, steps_list, water_list, sleep_list = [], [], [], []

    weight_trend, steps_trend = [], []

    for d in data:
        entry_date = d.get("entry_date")

        weight = _to_float(d.get("weight"))
        steps = _to_int(d.get("steps"))
        water = _to_float(d.get("water_intake"))
        sleep = _to_float(d.get("sleep_hours"))

        weight_trend.append({"entry_date": entry_date, "weight": weight})
        steps_trend.append({"entry_date": entry_date, "steps": steps})

        if weight is not None: weights.append(weight)
        if steps is not None: steps_list.append(steps)
        if water is not None: water_list.append(water)
        if sleep is not None: sleep_list.append(sleep)

    summary = {
        # WEIGHT
        "avg_weight": _avg(weights),
        "min_weight": min(weights) if weights else None,
        "max_weight": max(weights) if weights else None,

        # STEPS
        "avg_steps": _avg(steps_list),
        "min_steps": min(steps_list) if steps_list else None,
        "max_steps": max(steps_list) if steps_list else None,

        # WATER
        "avg_water_intake": _avg(water_list),
        "min_water_intake": min(water_list) if water_list else None,
        "max_water_intake": max(water_list) if water_list else None,

        # SLEEP
        "avg_sleep_hours": _avg(sleep_list),
        "min_sleep_hours": min(sleep_list) if sleep_list else None,
        "max_sleep_hours": max(sleep_list) if sleep_list else None,

        "data_points": len(data),
    }

    return jsonify({
        "weight_trend": weight_trend,
        "steps_trend": steps_trend,
        "summary": summary,
    }), 200
