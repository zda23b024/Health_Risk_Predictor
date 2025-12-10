<<<<<<< HEAD
=======

from flask import Flask
from flask_cors import CORS

from database import init_db
from routes.health_routes import health_bp
from routes.stats_routes import stats_bp
from routes.predict_routes import predict_bp


def create_app():
    app = Flask(__name__)

    # Enable CORS for all origins (simplest for local dev)
    CORS(app)

    # Register blueprints
    app.register_blueprint(health_bp)

    return app


app = create_app()


if __name__ == "__main__":
    # Create tables if not exist
    init_db()
    # Run dev server
    app.run(host="0.0.0.0", port=5000, debug=True)
>>>>>>> f05f78b12de6668b546f2df13b1b5687f4682e92
