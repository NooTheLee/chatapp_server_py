from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, UTC, timezone
from sqlalchemy.exc import SQLAlchemyError
import uuid

#
from ..schemas.chatroom_schema import *
from ..models import *
from ..data import *

chatroom_bp = Blueprint("chatroom", __name__)


# @chatroom_bp.route("/")
# def index():
#     return "Hello world from ChatRoom API", 200


@chatroom_bp.route("/create", methods=["POST"])
@jwt_required()
def create_chatroom():
    try:
        user_id = get_jwt_identity()
        data = CreateChatRoomRequestSchema().load(request.json)

        if not data["userIds"]:
            return jsonify({"message": "Missing members id"}), 400

        members = User.query.filter(User.id.in_(data["userIds"])).all()
        if not members:
            return jsonify({"message": "Cannot find these members!"}), 404

        chatroom = ChatRoom(
            id=uuid.uuid4(),
            name=data["name"],
            description=data.get("description"),
            is_group=data.get("isGroup", False),
            created_by=user_id,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            users=members,
        )

        db.session.add(chatroom)
        db.session.commit()

        return jsonify(ChatRoomResponseSchema().dump(chatroom)), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"message": f"Cannot create chat room: {str(e)}"}), 500


@chatroom_bp.route("", methods=["GET"])
@jwt_required()
def get_all_chatrooms():
    try:
        user_id = get_jwt_identity()
        rooms = (
            ChatRoom.query.filter(ChatRoom.users.any(User.id == user_id))
            .options(
                db.joinedload(ChatRoom.users),
                db.subqueryload(ChatRoom.messages).joinedload(Message.user),
            )
            .all()
        )

        sorted_rooms = sorted(
            rooms,
            key=lambda cr: max(
                [m.created_at for m in cr.messages], 
                default=datetime.min.replace(tzinfo=timezone.utc)
            ),
            reverse=True,
        )

        return jsonify(ChatRoomResponseSchema(many=True).dump(sorted_rooms)), 200
    except Exception as e:
        return jsonify({"message": f"Cannot fetch chat rooms: {str(e)}"}), 500


@chatroom_bp.route("/<uuid:room_id>", methods=["GET"])
@jwt_required()
def get_chatroom_by_id(room_id):
    try:
        user_id = get_jwt_identity()
        cr = (
            ChatRoom.query.filter(ChatRoom.id == room_id)
            .options(
                db.joinedload(ChatRoom.users),
                db.subqueryload(ChatRoom.messages).joinedload(Message.user),
            )
            .first()
        )
        if cr is None:
            return jsonify({"message": "Room not found"}), 400
        if user_id not in [str(u.id) for u in cr.users]:
            return jsonify({"message": "Unauthorized"}), 404

        return jsonify(ChatRoomResponseSchema().dump(cr)), 200
    except Exception as e:
        return jsonify({"message": f"Error getting room: {str(e)}"}), 500


@chatroom_bp.route("/<uuid:room_id>", methods=["DELETE"])
@jwt_required()
def delete_chatroom(room_id):
    try:
        user_id = get_jwt_identity()
        cr = ChatRoom.query.get(room_id)
        if not cr:
            return jsonify({"message": "Room not found"}), 404

        if str(user_id) != str(cr.created_by):
            return jsonify({"message": "You are not allowed to delete this room."}), 403
        db.session.delete(cr)
        db.session.commit()
        return "", 204
    except Exception as e:
        return jsonify({"message": f"Error deleting room: {str(e)}"}), 500
