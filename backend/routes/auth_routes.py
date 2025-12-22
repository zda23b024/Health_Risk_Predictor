import os
import sqlite3
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from database import get_connection, init_db, is_postgres_url, get_db_url

auth_bp = Blueprint("auth", __name__)

# Use a real secret from env in production (Render)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
_SERIALIZER = URLSafeTimedSerializer(SECRET_KEY)

TOKEN_MAX_AGE_SECONDS = 60 * 60 * 24 * 7  # 7 days


def _issue_token(user_id: int, username: str) -> str:
    return _SERIALIZER.dumps({"user_id": user_id, "username": username})


def verify_token(token: str):
    try:
        return _SERIALIZER.loads(token, max_age=TOKEN_MAX_AGE_SECONDS)
    except (BadSignature, SignatureExpired):
        return None


def get_current_user_id_from_request():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth.replace("Bearer ", "", 1).strip()
    payload = verify_token(token)
    if not payload:
        return None
    return int(payload.get("user_id"))


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()

    if len(username) < 3 or len(password) < 4 or not email:
        return jsonify({"error": "username >= 3 chars, password >= 4 chars and valid email required"}), 400

    # Ensure tables exist
    init_db()

    conn = get_connection()
    try:
        cur = conn.cursor()

        if is_postgres_url(get_db_url()):
            # Postgres placeholders + returning id
            cur.execute(
                "INSERT INTO users (username, email, password_hash, is_verified) VALUES (%s, %s, %s, %s) RETURNING id",
                (username, email, generate_password_hash(password), True),
            )
            user_id = cur.fetchone()["id"] if isinstance(cur.fetchone, object) else None  # defensive
            # If fetchone() already consumed, re-read:
            if user_id is None:
                cur2 = conn.cursor()
                cur2.execute("SELECT id FROM users WHERE username=%s", (username,))
                user_id = cur2.fetchone()["id"]
            conn.commit()
        else:
            # SQLite placeholders
            cur.execute(
                "INSERT INTO users (username, email, password_hash, is_verified) VALUES (?, ?, ?, 1)",
                (username, email, generate_password_hash(password)),
            )
            conn.commit()
            user_id = cur.lastrowid

        token = _issue_token(int(user_id), username)
        return jsonify({
            "message": "Registered and logged in.",
            "token": token,
            "user": {"id": int(user_id), "username": username}
        }), 201

    except Exception as e:
        conn.rollback()
        # Handle unique errors for SQLite and Postgres
        msg = str(e).lower()
        if "unique" in msg or "duplicate" in msg:
            return jsonify({"error": "Username or email already exists"}), 409
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    finally:
        conn.close()


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    identifier = (data.get("username") or data.get("email") or "").strip()
    password = (data.get("password") or "").strip()

    if not identifier or not password:
        return jsonify({"error": "username/email and password required"}), 400

    # Ensure tables exist
    init_db()

    conn = get_connection()
    try:
        cur = conn.cursor()

        if is_postgres_url(get_db_url()):
            cur.execute(
                "SELECT id, username, password_hash, email FROM users WHERE username = %s OR email = %s",
                (identifier, identifier),
            )
            row = cur.fetchone()
        else:
            cur.execute(
                "SELECT id, username, password_hash, email FROM users WHERE username = ? OR email = ?",
                (identifier, identifier),
            )
            row = cur.fetchone()
            if row is not None and not isinstance(row, dict):
                # sqlite Row -> dict
                row = dict(row)

        if not row or not check_password_hash(row["password_hash"], password):
            return jsonify({"error": "Invalid username/email or password"}), 401

        token = _issue_token(int(row["id"]), row["username"])
        return jsonify({
            "message": "Logged in",
            "token": token,
            "user": {"id": int(row["id"]), "username": row["username"]}
        }), 200

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    finally:
        conn.close()
