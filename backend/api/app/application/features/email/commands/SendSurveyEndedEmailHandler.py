from dataclasses import dataclass
from typing import List
import threading
import os
import uuid
from flask import current_app
from .....domains.email.models import EmailStatus
from .....domains.email.repositories import SurveySentEmailRepository
from ....contracts.IHandler import IHandler
from sqlalchemy.orm import Session   
from .....core.extensions import db
from ....services.email_service import EmailService


@dataclass
class SendSurveyEndedEmailCommand:
    recipients: List[str]
    survey_title: str
    survey_id: str

class SendSurveyEndedEmailHandler(IHandler):
    def __init__(self, email_service: EmailService, flask_app):
        self.email_service = email_service
        self.flask_app = flask_app
        self.template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../../resources/email_templates/survey_ended_template.html"
        )

    def handle(self, command: SendSurveyEndedEmailCommand):
        saved_emails = self.email_service.save_survey_email(command.survey_id, command.recipients)

        with open(self.template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        email_body = template_content.format(
            survey_title=command.survey_title
        )

        email_ids = [email.id for email in saved_emails]

        thread = threading.Thread(
            target=self._send_emails_in_thread,
            args=(self.flask_app, saved_emails, command, email_body)
        )
        thread.start()

    def _send_emails_in_thread(self, flask_app, email_ids: List[uuid.UUID], command, email_body):
        with flask_app.app_context():
            session = Session(db.engine)
            try:
                for email_id in email_ids:
                    email_entry = SurveySentEmailRepository.get_by_id(email_id, session)
                    try:
                        self.email_service.send_email(
                            to=email_entry.email,
                            subject=f'Survey "{command.survey_title}" has ended',
                            body=email_body
                        )
                        SurveySentEmailRepository.update_status(email_entry.id, EmailStatus.SENT, session)
                    except Exception:
                        SurveySentEmailRepository.update_status(email_entry.id, EmailStatus.FAILED, session)
            finally:
                session.close()