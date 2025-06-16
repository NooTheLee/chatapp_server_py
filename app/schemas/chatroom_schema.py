from marshmallow import fields
from .convert_camel_schema import CamelCaseSchema


class CreateChatRoomRequestSchema(CamelCaseSchema):
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    isGroup = fields.Bool(required=False)
    userIds = fields.List(fields.UUID(), required=True)


class ChatRoomUserSchema(CamelCaseSchema):
    id = fields.UUID()
    username = fields.Str()
    email = fields.Email()
    display_name = fields.Str(allow_none=True)
    avatar_url = fields.Str(allow_none=True)
    is_online = fields.Bool()
    last_seen = fields.DateTime(allow_none=True)


class ChatRoomMessageSchema(CamelCaseSchema):
    id = fields.UUID()
    content = fields.Str()
    message_type = fields.Int()
    is_edited = fields.Bool()
    edited_at = fields.DateTime(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    sender = fields.Nested(ChatRoomUserSchema, attribute="user", data_key="sender")


class ChatRoomResponseSchema(CamelCaseSchema):
    id = fields.UUID()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    is_group = fields.Bool()
    created_by = fields.UUID()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    members = fields.Nested(ChatRoomUserSchema, many=True, attribute="users", data_key="members")
    messages = fields.Nested(ChatRoomMessageSchema, many=True, attribute="messages", data_key="messages")

