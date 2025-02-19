from .models import SurveySentEmail, EmailStatus
from ...core.extensions import db
from typing import List
from datetime import datetime

class SurveySentEmailRepository:

    @staticmethod
    def add_list(survey_email: List[SurveySentEmail]):
        db.session.add_all(survey_email)
        db.session.commit()

    @staticmethod
    def get_by_id(email_id, session):
        return session.query(SurveySentEmail).get(email_id.id)

    @staticmethod
    def update_status(email_id, new_status: EmailStatus, session):
        survey_email = session.query(SurveySentEmail).filter(SurveySentEmail.id == email_id).one_or_none()
        if survey_email is not None:
            survey_email.status = new_status
            survey_email.status_change_time = datetime.utcnow()
            session.commit()