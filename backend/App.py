from flask import Flask
from flask_cors import CORS
from database import init_db
from routes.health_routes import health_bp
from routes.stats_routes import stats_bp


def create_app():
    app = Flask(__name__)

    # Enable CORS for all origins (simplest for local dev)
    CORS(app)

    # Initialize DB tables
    init_db()

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(stats_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
