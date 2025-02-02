from marshmallow import Schema, fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from uuid import UUID
from datetime import datetime
from .....domains.survey.models import Survey, SurveyResponses  # Adjust the import path as necessary

class SurveySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Survey
        include_fk = True
        include_relationships = True
        sqla_session = None

    id = auto_field(dump_only=True)
    user_id = fields.UUID(required=False) #it's not mandatary in the request
    title = fields.String(required=True, validate=validate.Length(max=200))
    question = fields.String(required=True, validate=validate.Length(max=1000))
    created_time = fields.DateTime(dump_only=True)
    ending_time = fields.DateTime(required=True)
    is_anonymous = fields.Boolean(required=True)
    user_ended = fields.Boolean(dump_only=True)
    emails = fields.List(
        fields.Email(error_messages={"invalid": "Not a valid email address."}),
        required=False,
        allow_none=True,
        validate=validate.Length(min=0)
    )

class SurveyResponsesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SurveyResponses
        include_fk = True
        include_relationships = True
        sqla_session = None

    id = auto_field(dump_only=True)
    user_id = fields.UUID(allow_none=True)
    email = fields.Email(required=False, allow_none=True, validate=validate.Length(max=200))
    response = fields.String(required=True, validate=validate.Length(max=32))
    responded_time = fields.DateTime(dump_only=True)