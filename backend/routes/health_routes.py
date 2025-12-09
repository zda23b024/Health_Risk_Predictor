from flask import Blueprint, request, jsonify
from datetime import date
from database import get_connection


health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["POST"])
def add_health_entry():
    """
    Add a daily health entry.
    Expected JSON:
    {
        "entry_date": "YYYY-MM-DD"   # optional, defaults to today
        "weight": 70.5,
        "steps": 10000,
        "water_intake": 2.5,
        "sleep_hours": 7.0
    }
    """
    data = request.get_json() or {}

    entry_date = data.get("entry_date") or date.today().isoformat()
    weight = data.get("weight")
    steps = data.get("steps")
    water_intake = data.get("water_intake")
    sleep_hours = data.get("sleep_hours")

    # Basic validation (you can improve later)
    if weight is None or steps is None or water_intake is None or sleep_hours is None:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO health_logs (entry_date, weight, steps, water_intake, sleep_hours)
        VALUES (?, ?, ?, ?, ?)
        """,
        (entry_date, weight, steps, water_intake, sleep_hours),
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": "Entry created", "id": new_id}), 201


@health_bp.route("/health", methods=["GET"])
def get_health_entries():
    """
    Get health entries.
    Optional query: ?days=7 (default 7) to get last N days ordered by date desc.
    """
    days = request.args.get("days", default=7, type=int)

    conn = get_connection()
    cursor = conn.cursor()

    # Last N days based on created_at (simpler for now)
    cursor.execute(
        """
        SELECT id, entry_date, weight, steps, water_intake, sleep_hours, created_at
        FROM health_logs
        ORDER BY entry_date DESC
        LIMIT ?
        """,
        (days,),
    )

    rows = cursor.fetchall()
    conn.close()

    entries = [
        {
            "id": row["id"],
            "entry_date": row["entry_date"],
            "weight": row["weight"],
            "steps": row["steps"],
            "water_intake": row["water_intake"],
            "sleep_hours": row["sleep_hours"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]

    return jsonify(entries), 200
