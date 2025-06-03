import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from ...core.extensions import db

class Survey(db.Model):
    __tablename__ = 'surveys'
    __table_args__ = {'schema': 'surveys'}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('users.users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    question = db.Column(db.String(1000), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    ending_time = db.Column(db.DateTime, nullable=False)
    is_anonymous = db.Column(db.Boolean, nullable=False)
    user_ended = db.Column(db.Boolean, default=False, nullable=False)

    user = relationship("User", backref=db.backref("surveys", lazy=True))

class SurveyResponses(db.Model):
    __tablename__ = 'survey_responses'
    __table_args__ = {'schema': 'surveys'}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('users.users.id'), nullable=True)
    survey_id = db.Column(UUID(as_uuid=True), ForeignKey('surveys.surveys.id'), nullable=False)
    email = db.Column(db.String(200), nullable=True)
    response = db.Column(db.String(32), nullable=False, default="no response")
    responded_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", backref=db.backref("survey_responses", lazy=True))
    survey = relationship("Survey", backref=db.backref("survey_responses", lazy=True))
