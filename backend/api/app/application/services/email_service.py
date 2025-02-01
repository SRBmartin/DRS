import requests
from typing import List
from ...domains.email.models import SurveySentEmail
from ...domains.email.repositories import SurveySentEmailRepository

class EmailService:
    def __init__(self, email_service_url: str, email_service_api: str):
        self.email_service_url = email_service_url
        self.email_service_api = email_service_api

    def send_email(self, to: str, subject: str, body: str) -> None:
        payload = {
            "to": to,
            "subject": subject,
            "body": body
        }

        headers = {
            "Authorization": f"Bearer {self.email_service_api}",
            "Content-Type": "application/json"
        }

        response = requests.post(self.email_service_url, json=payload, headers=headers)
        response.raise_for_status()  # raise exception, we catch it in the handler

    def save_survey_email(self, survey_id: str, emails: List[str]) -> List[SurveySentEmail]:
        survey_emails = []
        for email in emails:
            survey_emails.append(
                SurveySentEmail(
                    survey_id=survey_id,
                    email=email
                )
            )

        SurveySentEmailRepository.add_list(survey_emails)
        return survey_emails