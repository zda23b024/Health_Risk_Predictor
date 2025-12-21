from flask import Blueprint, request, jsonify, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from database import get_connection
from utils.email_utils import send_verification_email

import os
import secrets
from datetime import datetime, timedelta


auth_bp = Blueprint("auth", __name__)

# NOTE: For a class project this is fine; for production, store in env var.
_SERIALIZER = URLSafeTimedSerializer("dev-secret-change-me")
TOKEN_MAX_AGE_SECONDS = 60 * 60 * 24 * 7  # 7 days

# Verification token expiry in hours
VERIFICATION_EXPIRY_HOURS = int(os.environ.get("VERIFICATION_EXPIRY_HOURS", "24"))


def _issue_token(user_id: int, username: str) -> str:
    return _SERIALIZER.dumps({"user_id": user_id, "username": username})


def verify_token(token: str):
    """Return payload dict or None."""
    try:
        payload = _SERIALIZER.loads(token, max_age=TOKEN_MAX_AGE_SECONDS)
        return payload
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

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, email, password_hash, is_verified) VALUES (?, ?, ?, 1)",
            (username, email, generate_password_hash(password)),
        )
        conn.commit()
        user_id = cur.lastrowid
    except Exception as e:
        conn.close()
        # Could be constraint error on username or email
        return jsonify({"error": "Username or email already exists"}), 409

    conn.close()

    # Auto-issue auth token (no email verification required)
    token = _issue_token(user_id, username)
    return jsonify({"message": "Registered and logged in.", "token": token, "user": {"id": user_id, "username": username}}), 201


@auth_bp.route("/auth/verify", methods=["GET"])
def verify():
    # Verification flow disabled — email verification is not required in this deployment.
    return jsonify({"error": "Email verification disabled"}), 410


@auth_bp.route("/auth/resend-verification", methods=["POST"])
def resend_verification():
    # Verification not in use; this endpoint is disabled.
    return jsonify({"error": "Email verification disabled"}), 410


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    identifier = (data.get("username") or data.get("email") or "").strip()
    password = (data.get("password") or "").strip()

    conn = get_connection()
    cur = conn.cursor()
    # Allow login by username or email
    cur.execute("SELECT id, username, password_hash, is_verified, email FROM users WHERE username = ? OR email = ?", (identifier, identifier))
    row = cur.fetchone()
    conn.close()

    if not row or not check_password_hash(row["password_hash"], password):
        return jsonify({"error": "Invalid username/email or password"}), 401

    token = _issue_token(row["id"], row["username"])
    return jsonify({"message": "Logged in", "token": token, "user": {"id": row["id"], "username": row["username"]}}), 200


@auth_bp.route('/auth/test-email', methods=['POST'])
def test_email():
    return jsonify({"error": "Email verification not supported in this deployment"}), 410

@auth_bp.route("/auth/me", methods=["GET"])
def me():
    user_id = get_current_user_id_from_request()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, created_at FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": row["id"], "username": row["username"], "created_at": row["created_at"]}), 200