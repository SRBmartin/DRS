import uuid
import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from ...core.extensions import db

class EmailStatus(str, enum.Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"

class SurveySentEmail(db.Model):
    __tablename__ = 'survey_sent_emails'
    __table_args__ = {'schema': 'email'}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    survey_id = db.Column(UUID(as_uuid=True), ForeignKey('surveys.surveys.id'), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.Enum(EmailStatus), nullable=False, default=EmailStatus.PENDING)
    status_change_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    survey = relationship("Survey", backref=db.backref("survey_sent_emails", lazy=True))