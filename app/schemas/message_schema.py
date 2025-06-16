from marshmallow import fields
from .convert_camel_schema import CamelCaseSchema
from .chatroom_schema import ChatRoomUserSchema


class CreateMessageRequestSchema(CamelCaseSchema):
    chat_room_id = fields.UUID(required=True, data_key="chatRoomId")
    content = fields.Str(required=True)
    message_type = fields.Int()  # 1: text by default


class UpdateMessageRequestSchema(CamelCaseSchema):
    content = fields.Str(required=True)


class MessageResponseSchema(CamelCaseSchema):
    id = fields.UUID()
    chat_room_id = fields.UUID()
    content = fields.Str()
    message_type = fields.Int()
    is_edited = fields.Bool()
    edited_at = fields.DateTime(allow_none=True, )
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    sendor = fields.Nested(ChatRoomUserSchema, attribute="user", data_key="sender")
