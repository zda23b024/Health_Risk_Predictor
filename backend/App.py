import os
from flask import Flask
from flask_cors import CORS

from database import init_db
from routes.health_routes import health_bp
from routes.stats_routes import stats_bp
from routes.predict_routes import predict_bp
from routes.auth_routes import auth_bp


def create_app():
    app = Flask(__name__)

    # Optional: keep config centralized
    app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")

    # CORS (Render + local)
    allowed_origins = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173"
    )
    CORS(app, resources={r"/*": {"origins": allowed_origins.split(",")}})

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(auth_bp)

    # Initialize DB (safe to call on startup)
    with app.app_context():
        init_db()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
