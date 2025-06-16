from flask import Flask, jsonify
from .config.config import Config
from .data.db import db
from flask_jwt_extended import JWTManager

jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)

    from .controllers import register_all_blueprints

    register_all_blueprints(app)

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"message": "Not Found", "status": 404}), 404

    @app.errorhandler(405)
    def handle_405(e):
        return jsonify({"message": "Method Not Allowed", "status": 405}), 405

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"message": "Internal Server Error", "status": 500}), 500

    @app.errorhandler(422)
    def handle_422(err):
        return (
            jsonify(
                {
                    "message": "Unprocessable Entity",
                    "status": 422,
                    "details": getattr(err, "description", str(err)),
                }
            ),
            422,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"message": "Invalid token", "details": reason}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return (
            jsonify({"message": "Missing or malformed token", "details": reason}),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has expired"}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has been revoked"}), 401

    return app
