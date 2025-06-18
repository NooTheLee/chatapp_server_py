import uuid
from datetime import datetime, UTC
from sqlalchemy.dialects.postgresql import UUID

#
from ..data.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    display_name = db.Column(db.String(255), nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    is_online = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(
        db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )

    # Relationships (nếu đã định nghĩa Message và ChatRoom models)
    # messages = db.relationship("Message", backref="user", lazy=True)
    # chatrooms = db.relationship("ChatRoom", secondary="chat_room_users", backref="users")

    def __repr__(self):
        return f"<User {self.username}>"
