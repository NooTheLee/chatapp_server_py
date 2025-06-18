from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
#
from app.models import User
from app.schemas.chatroom_schema import ChatRoomUserSchema

user_bp = Blueprint("user", __name__)


@user_bp.route("", methods=["GET"])
def index():
    return jsonify({"message": "Hello from user API!"}), 200


@user_bp.route("/search", methods=["GET"])
@jwt_required()
def search_users():
    try:
        query = request.args.get("q", "").strip()

        if not query:
            return jsonify({"message": "Missing query"}), 400

        users = (
            User.query.filter(
                or_(
                    User.username.ilike(f"%{query}%"),
                    User.email.ilike(f"%{query}%"),
                    User.display_name.like(f"%{query}%"),
                )
            )
            .limit(20)
            .all()
        )

        return jsonify(ChatRoomUserSchema(many=True).dump(users)), 200
    except Exception as e:
        return jsonify({"message": f"Search failed: {str(e)}"}), 500
