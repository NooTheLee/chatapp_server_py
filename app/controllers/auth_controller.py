from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import uuid

#
from app.models import User
from app.schemas.auth_schema import *
from app.data import db
from app.services.jwt_service import generate_jwt


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("", methods=["GET"])
def hello():
    return jsonify({"message": "Welcome to auth!"})


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = RegisterRequestSchema().load(request.json)
        if User.query.filter(
            (User.email == data["email"]) | (User.username == data["username"])
        ).first():
            return jsonify({"message": "Username of email already in use."}), 400

        user = User(
            id=uuid.uuid4(),
            username=data["username"],
            email=data["email"],
            display_name=data.get("display_name"),
            avatar_url=data.get("avatar_url"),
            password_hash=generate_password_hash(data["password"]),
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Register successfully"}), 201
    except ValidationError as ve:
        return jsonify({"message": "Invalid input", "errors": ve.messages}), 400

    except SQLAlchemyError as db_err:
        db.session.rollback()
        return jsonify({"message": "Database error", "details": str(db_err)}), 500

    except Exception as e:
        return jsonify({"message": "Unexpected error at register", "details": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = LoginRequestSchema().load(request.json)
        email, username = data.get('email'), data.get('username')
        if not email and not username:
            return jsonify({"message": "Missing username and email!"}), 400
        
        user = User.query.filter((User.email == email) | (User.username == username)).first()

        if not user or not check_password_hash(user.password_hash, data["password"]):
            return jsonify({"message": "Invalid credentials."}), 401
        
        token = generate_jwt(user)
        user.is_online = True
        result = AuthResponseSchema().dump(user)

        return jsonify({"token": token, "user": result}), 200
    except ValidationError as ve:
        return jsonify({"message": "Invalid input", "errors": ve.messages}), 400

    except SQLAlchemyError as db_err:
        db.session.rollback()
        return jsonify({"message": "Database error", "details": str(db_err)}), 500

    except Exception as e:
        return jsonify({"message": "Unexpected error at login", "details": str(e)}), 500

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({ "message": "Not found" }), 404
        
        return jsonify(ProfileResponseSchema().dump(user)), 200
    except Exception as ex:
        return jsonify({"message": "Unexpected error at login", "details": str(ex)}), 500

