from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, UTC
import uuid

#
from app.data import db
from app.models import *
from app.schemas.message_schema import *
from app.schemas.chatroom_schema import ChatRoomResponseSchema, ChatRoomUserSchema

message_bp = Blueprint("message_bp", __name__)


@message_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to message API!"})


@message_bp.route("/create", methods=["POST"])
@jwt_required()
def create_message():
    try:
        data = CreateMessageRequestSchema().load(request.json)
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        chat_room = ChatRoom.query.filter_by(id=data["chat_room_id"]).first()
        if not chat_room:
            return (
                jsonify(
                    {
                        "message": f"ChatRoom with ID '{data['chat_room_id']}' does not exist."
                    }
                ),
                400,
            )

        if user_id not in [str(u.id) for u in chat_room.users]:
            return jsonify({"message": "You cannot create message in this room!"}), 400

        message = Message(
            id=uuid.uuid4(),
            chat_room_id=data["chat_room_id"],
            user_id=user_id,
            content=data["content"],
            message_type=data.get("message_type", 1),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        db.session.add(message)
        db.session.commit()

        response_data = MessageResponseSchema().dump(message)
        response_data['sender'] = ChatRoomUserSchema().dump(user)
        
        return jsonify(response_data), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"message": f"Unexpected error: {str(e)}"}), 500


@message_bp.route("/<uuid:id>", methods=["GET"])
@jwt_required()
def get_message_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if not message:
        return jsonify({"message": "Message not found"}), 404
    return jsonify(MessageResponseSchema().dump(message)), 200


@message_bp.route("/<uuid:id>", methods=["PUT"])
@jwt_required()
def update_message(id):
    try:
        message = Message.query.filter_by(id=id).first()
        if not message:
            return jsonify({"message": "Message not found"}), 404

        user_id = get_jwt_identity()
        if str(message.user_id) != user_id:
            return jsonify({"message": "Forbidden"}), 403

        data = UpdateMessageRequestSchema().load(request.json)
        message.content = data["content"]
        message.is_edited = True
        message.edited_at = datetime.now(UTC)
        message.updated_at = datetime.now(UTC)
        db.session.commit()

        return jsonify(MessageResponseSchema().dump(message)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500


@message_bp.route("/<uuid:id>", methods=["DELETE"])
@jwt_required()
def delete_message(id):
    try:
        message = Message.query.get(id)
        if not message:
            return jsonify({"message": "Message not found"}), 404

        user_id = get_jwt_identity()

        chat_room = ChatRoom.query.get(message.chat_room_id)
        is_owner = str(message.user_id) == user_id
        is_creator = chat_room and str(chat_room.created_by) == user_id

        if not is_owner and not is_creator:
            return jsonify({"message": "Forbidden"}), 403

        db.session.delete(message)
        db.session.commit()
        return "", 204
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500


@message_bp.route("/chatroom/<uuid:id>", methods=["GET"])
@jwt_required()
def get_chatroom_by_id(id):
    try:
        user_id = get_jwt_identity()
        cr = ChatRoom.query.filter_by(id=id).first()

        if not cr or user_id not in [str(u.id) for u in cr.users]:
            return jsonify({"message": "Cannot find or access chat room!"}), 404

        return jsonify(ChatRoomResponseSchema().dump(cr)), 200

    except Exception as e:
        return jsonify({"message": f"Cannot get chat room: {str(e)}"}), 500
