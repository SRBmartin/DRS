from dataclasses import dataclass
from typing import List
import threading
import os

from .....core.config import Config
from ....contracts.IHandler import IHandler

@dataclass
class SendSurveyCreatedEmailCommand:
    recipients: List[str]
    survey_title: str
    survey_id: str
    subject: str = "Invitation to participate in a survey"

class SendSurveyCreatedEmailHandler(IHandler):
    def __init__(self, email_service):
        self.email_service = email_service
        self.template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "../../../resources/email_templates/new_survey_template.html"
        )
        
    def handle(self, command):
        with open(self.template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        email_body = template_content.format(
            survey_title=command.survey_title,
            survey_id=str(command.survey_id)
        )

        thread = threading.Thread(
            target=self._send_emails_in_thread,
            args=(command, email_body)
        )
        thread.start()

    def _send_emails_in_thread(self, command, email_body):
        for recipient in command.recipients:
            try:
                self.email_service.send_email(
                    to=recipient,
                    subject=command.subject,
                    body=email_body
                )
            except Exception as e:
                print(f"Failed to send email to {recipient}: {e}")