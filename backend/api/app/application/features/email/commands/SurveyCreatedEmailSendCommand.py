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

@dataclass
class SendSurveyCreatedEmailCommand:
    recipients: List[str]
    survey_title: str
    survey_id: str
    subject: str = "Invitation to participate in a survey"

class SendSurveyCreatedEmailHandler(IHandler):
    def __init__(self, email_service, survey_responses_service, flask_app):
        self.email_service = email_service
        self.survey_responses_service = survey_responses_service
        self.flask_app = flask_app
        self.template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "../../../resources/email_templates/new_survey_template.html"
        )
        
    def handle(self, command):
        #firstly, we're gonna save the emails to the database
        #In case of failure, we're gonna resend these emails in some point in time
        saved_emails = self.email_service.save_survey_email(command.survey_id, command.recipients)

        with open(self.template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        email_body = template_content.format(
            survey_title=command.survey_title,
            survey_id=str(command.survey_id)
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
                    survey_email = SurveySentEmailRepository.get_by_id(email_id, session)
                    try:
                        self.email_service.send_email(
                            to=survey_email.email,
                            subject=command.subject,
                            body=email_body
                        )

                        SurveySentEmailRepository.update_status(survey_email.id, EmailStatus.SENT, session)
                        self.survey_responses_service.create(command.survey_id, survey_email.email)
                        
                    except Exception as e:
                        SurveySentEmailRepository.update_status(survey_email.id, EmailStatus.FAILED, session)
                    
            finally:
                session.close()