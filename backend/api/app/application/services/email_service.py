import requests

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
