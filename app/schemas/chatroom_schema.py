from marshmallow import Schema, fields


class CreateChatRoomRequestSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    is_group = fields.Bool(required=False)
    user_ids = fields.List(fields.UUID(), required=True)


class ChatRoomUserSchema(Schema):
    id = fields.UUID()
    username = fields.Str()
    email = fields.Email()
    display_name = fields.Str(allow_none=True)
    avatar_url = fields.Str(allow_none=True)
    is_online = fields.Bool()
    last_seen = fields.DateTime(allow_none=True)


class ChatRoomMessageSchema(Schema):
    id = fields.UUID()
    content = fields.Str()
    message_type = fields.Int()
    is_edited = fields.Bool()
    edited_at = fields.DateTime(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    sender = fields.Nested(ChatRoomUserSchema, attribute="user")


class ChatRoomResponseSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    is_group = fields.Bool()
    created_by = fields.UUID()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    members = fields.Nested(ChatRoomUserSchema, many=True, attribute="user")
    messages = fields.Nested(ChatRoomMessageSchema, many=True, attribute="user")
