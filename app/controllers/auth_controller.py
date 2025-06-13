from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import uuid

#
from ..models.user import User
from ..schemas.auth_schema import *
from ..data.db import db
from ..services.jwt_service import generate_jwt


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("", methods=["GET"])
def hello():
    return jsonify({"message": "Welcome to auth!"})


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        print("request.json", request.json)
        data = RegisterRequestSchema().load(request.json)
        print("data", data)
        if User.query.filter(
            (User.email == data["email"]) | (User.username == data["username"])
        ).first():
            return jsonify({"message": "Username of email already in use."}), 400

        print("XXX")
        user = User(
            id=uuid.uuid4(),
            username=data["username"],
            email=data["email"],
            display_name=data.get("display_name"),
            avatar_url=data.get("avatar_url"),
            password_hash=generate_password_hash(data["password"]),
        )

        print("here!!")

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User register successfully"}), 201
    except ValidationError as ve:
        return jsonify({"message": "Invalid input", "errors": ve.messages}), 400

    except SQLAlchemyError as db_err:
        db.session.rollback()
        return jsonify({"message": "Database error", "details": str(db_err)}), 500

    except Exception as e:
        return jsonify({"message": "Unexpected error", "details": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        return (
            jsonify(
                {
                    "message": "hello",
                }
            ),
            200,
        )
    except Exception as ex:
        return jsonify({"message": f"Cannot login {ex}"}), 500
