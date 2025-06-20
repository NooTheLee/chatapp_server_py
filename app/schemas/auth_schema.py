from marshmallow import fields
from .convert_camel_schema import CamelCaseSchema


class RegisterRequestSchema(CamelCaseSchema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    display_name = fields.String(allow_none=True)
    avatar_url = fields.Str(allow_none=True)


class LoginRequestSchema(CamelCaseSchema):
    username = fields.Str(allow_none=True)
    email = fields.Str(allow_none=True)
    password = fields.Str(required=True)


class AuthResponseSchema(CamelCaseSchema):
    id = fields.UUID()
    username = fields.Str()
    email = fields.Str()
    display_name = fields.Str(allow_none=True)
    avatar_url = fields.Str(allow_none=True)
    is_online = fields.Bool()


class ProfileResponseSchema(AuthResponseSchema):
    last_seen = fields.DateTime(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
