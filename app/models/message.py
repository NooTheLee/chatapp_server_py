import uuid
from datetime import datetime, UTC
from sqlalchemy.dialects.postgresql import UUID
from ..data.db import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    chat_room_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("chat_rooms.id"), nullable=False
    )

    message_type = db.Column(db.Integer, default=1)  # 1: text, 2: image, 3: file...
    is_edited = db.Column(db.Boolean, default=False)
    edited_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(
        db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )

    # Relationships
    # user = db.relationship("User", backref="messages", lazy=True)
    chatroom = db.relationship("ChatRoom", backref="messages", lazy=True)

    def __repr__(self):
        return f"<Message {self.id} in room {self.chat_room_id}>"
