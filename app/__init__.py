from flask import Flask
from .config.config import Config
from .data.db import db
from flask_jwt_extended import JWTManager
from .controllers.auth_controller import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    return app
