import os
import smtplib
import logging
from email.message import EmailMessage

from urllib.parse import urlencode

logger = logging.getLogger(__name__)

# Read settings from environment
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")
SMTP_FROM = os.environ.get("SMTP_FROM", "no-reply@healthtracker.local")

# Base verification URL (frontend or backend verify endpoint)
VERIFICATION_BASE = os.environ.get("VERIFICATION_BASE_URL") or os.environ.get("BACKEND_BASE_URL") or "http://localhost:5000"


def build_verification_link(token: str) -> str:
    params = urlencode({"token": token})
    return f"{VERIFICATION_BASE.rstrip('/')}/auth/verify?{params}"


def send_verification_email(email: str, token: str, username: str = None) -> bool:
    """Attempt to send a verification email. If SMTP is not configured, log the verification link for dev use.

    Returns True if a send (or log) was performed.
    """
    link = build_verification_link(token)
    subject = "Verify your HealthTracker account"
    body = f"Hi {username or ''},\n\nPlease verify your email by clicking the link below:\n\n{link}\n\nIf you didn't create an account, you can ignore this message. This link will expire in 24 hours.\n\nThanks,\nHealthTracker Team"

    # If SMTP configured, try to send
    if SMTP_HOST and SMTP_USER and SMTP_PASS:
        try:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = SMTP_FROM
            msg["To"] = email
            msg.set_content(body)

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as s:
                s.starttls()
                s.login(SMTP_USER, SMTP_PASS)
                s.send_message(msg)

            logger.info("Sent verification email to %s", email)
            return {"sent": True, "via": "smtp"}
        except Exception as e:
            logger.exception("Failed to send verification email: %s", e)
            # fall back to logging below

    # Dev fallback: log the link so a developer can copy it
    logger.warning("Verification email not sent via SMTP; verification link for %s: %s", email, link)
    # Return the link so callers can display it in dev
    return {"sent": False, "via": "log", "link": link}
