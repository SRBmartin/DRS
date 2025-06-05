from dataclasses import dataclass
import threading
import os
from flask import current_app

from .....domains.email.models import EmailStatus
from .....domains.email.repositories import SurveySentEmailRepository
from ....contracts.IHandler import IHandler
from .....core.extensions import db
from sqlalchemy.orm import Session

@dataclass
class SendSurveyResponseConfirmationEmailCommand:
    recipient: str
    survey_title: str
    response: str
    survey_id: str
    subject: str = "Survey Response Confirmation"

class SendSurveyResponseConfirmationEmailHandler(IHandler):
    def __init__(self, email_service, flask_app):
        self.email_service = email_service
        self.flask_app = flask_app
        self.template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../../resources/email_templates/survey_response_confirmation.html"
        )

    def handle(self, command: SendSurveyResponseConfirmationEmailCommand):
        saved_email = self.email_service.save_single_survey_email(command.survey_id, command.recipient)
        with open(self.template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        email_body = template_content.format(
            survey_title=command.survey_title,
            response=command.response
        )

        self._send_email(command, email_body, self.flask_app, saved_email)


    def _send_email(self, command, email_body, flask_app, saved_email):
        with flask_app.app_context():
            session = Session(db.engine)
            try:
                self.email_service.send_email(
                    to=command.recipient,
                    subject=command.subject,
                    body=email_body
                )
                SurveySentEmailRepository.update_status(saved_email.id, EmailStatus.SENT, session)
            except Exception as e:
                SurveySentEmailRepository.update_status(saved_email.id, EmailStatus.FAILED, session)
            finally:
                session.close()