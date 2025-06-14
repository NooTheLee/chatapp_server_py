from flask import Flask
from .config.config import Config
from .data.db import db
from flask_jwt_extended import JWTManager
from .controllers import register_all_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)

    register_all_blueprints(app)
    return app
