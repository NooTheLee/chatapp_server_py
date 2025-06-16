import uuid
from datetime import datetime, UTC
from sqlalchemy.dialects.postgresql import UUID
from ..data.db import db

# Association table for N-N: User <-> ChatRoom
user_chatroom = db.Table(
    "chat_room_users",
    db.Column("UsersId", UUID(as_uuid=True), db.ForeignKey("users.id"), primary_key=True),
    db.Column("ChatRoomsId", UUID(as_uuid=True), db.ForeignKey("chat_rooms.id"), primary_key=True)
)

class ChatRoom(db.Model):
    __tablename__ = "chat_rooms"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    is_group = db.Column(db.Boolean, default=False)

    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    # Relationships
    creator = db.relationship("User", backref="created_rooms", foreign_keys=[created_by])
    users = db.relationship("User", secondary="chat_room_users", backref="chatrooms")

    def __repr__(self):
        return f"<ChatRoom {self.name}>"
