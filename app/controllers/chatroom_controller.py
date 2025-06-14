from flask import Blueprint, request, jsonify
import uuid
from ..schemas.chatroom_schema import *

chatroom_bp = Blueprint("chatroom", __name__)


@chatroom_bp.route("/")
def index():
    return "Hello world from ChatRoom API", 200
