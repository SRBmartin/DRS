from marshmallow import Schema, fields, validate, post_load
from datetime import datetime
from .....domains.user.models import Session

class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    lastname = fields.Str(required=True, validate=validate.Length(max=100))
    address = fields.Str(required=True, validate=validate.Length(max=200))
    city = fields.Str(required=True, validate=validate.Length(max=100))
    country = fields.Str(required=True, validate=validate.Length(max=100))
    phone_number = fields.Str(required=True, validate=validate.Length(max=32))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(max=128))

class SessionSchema(Schema):
    id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)
    started_time = fields.DateTime(dump_only=True)
    ending_time = fields.DateTime(allow_none=True)
    ip_address = fields.Str(required=True, validate=validate.Length(max=45))
    logged_out = fields.Boolean(required=True)

    @post_load
    def make_session(self, data, **kwargs):
        return Session(**data)
    
class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)