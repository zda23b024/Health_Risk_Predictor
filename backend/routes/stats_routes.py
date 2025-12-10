from flask import Blueprint, jsonify
from backend.database import get_connection

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/health/stats", methods=["GET"])
def get_health_stats():
    """
    Returns stats for the last 7 entries (usually last 7 days):
    - weight_trend: [{entry_date, weight}]
    - steps_trend: [{entry_date, steps}]
    - summary: averages, min, max
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT entry_date, weight, steps, water_intake, sleep_hours
        FROM health_logs
        ORDER BY entry_date DESC
        LIMIT 7
        """
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        # No data yet
        return jsonify(
            {
                "weight_trend": [],
                "steps_trend": [],
                "summary": {
                    "min_weight": None,
                    "max_weight": None,
                    "avg_weight": None,
                    "avg_steps": None,
                    "avg_water_intake": None,
                    "avg_sleep_hours": None,
                    "data_points": 0,
                },
            }
        ), 200

    weight_trend = []
    steps_trend = []

    weights = []
    steps_list = []
    water_list = []
    sleep_list = []

    for row in rows:
        entry_date = row["entry_date"]

        weight = row["weight"]
        steps = row["steps"]
        water = row["water_intake"]
        sleep = row["sleep_hours"]

        # For charts
        weight_trend.append(
            {
                "entry_date": entry_date,
                "weight": weight,
            }
        )
        steps_trend.append(
            {
                "entry_date": entry_date,
                "steps": steps,
            }
        )

        # For stats (only if not None)
        if weight is not None:
            weights.append(weight)
        if steps is not None:
            steps_list.append(steps)
        if water is not None:
            water_list.append(water)
        if sleep is not None:
            sleep_list.append(sleep)

    # Compute aggregates safely
    def avg(lst):
        return sum(lst) / len(lst) if lst else None

    summary = {
        "min_weight": min(weights) if weights else None,
        "max_weight": max(weights) if weights else None,
        "avg_weight": avg(weights),
        "avg_steps": avg(steps_list),
        "avg_water_intake": avg(water_list),
        "avg_sleep_hours": avg(sleep_list),
        "data_points": len(rows),
    }

    # Reverse to chronological order (oldest → newest)
    weight_trend = list(reversed(weight_trend))
    steps_trend = list(reversed(steps_trend))

    return jsonify(
        {
            "weight_trend": weight_trend,
            "steps_trend": steps_trend,
            "summary": summary,
        }
    ), 200
