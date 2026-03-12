import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions import db


def create_app():
    # Load environment variables from backend/.env (if present),
    # regardless of where the server is started from.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(dotenv_path=os.path.join(base_dir, ".env"))

    app = Flask(__name__)
    app.config.from_object(Config())

    # Allow frontend (localhost:3000) to call the API during development
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize extensions
    db.init_app(app)

    # Import models so that SQLAlchemy is aware of them
    from models.user_model import User  # noqa: F401
    from models.note_model import Note  # noqa: F401

    # Local-dev convenience: auto-create tables when using SQLite.
    # This avoids "no such table" errors when running without migrations.
    if str(app.config.get("SQLALCHEMY_DATABASE_URI", "")).startswith("sqlite:"):
        with app.app_context():
            db.create_all()

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.notes_routes import notes_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(notes_bp, url_prefix="/api")

    # Health check route
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok"}), 200

    # Generic error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"error": "Unauthorized", "message": str(error)}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({"error": "Forbidden", "message": str(error)}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": str(error)}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred."}), 500

    return app


if __name__ == "__main__":
    flask_app = create_app()
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port, debug=flask_app.config.get("DEBUG", False))

