from dataclasses import dataclass
from datetime import datetime, timezone
from flask import current_app, g

from ....services.survey_service import SurveyResponsesService, SurveyService
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler
from .....application.features.email.commands.SurveyResponseConfirmationEmailCommand import SendSurveyResponseConfirmationEmailCommand

@dataclass
class AnswerSurveyWebsiteCommand:
    survey_id: str
    response: str  # Expected values: "yes", "no", or "maybe"
    ip_address: str
    ssid: str

class AnswerSurveyWebsiteCommandHandler(IHandler):
    def __init__(self, survey_service: SurveyService, survey_responses_service: SurveyResponsesService, user_service: UserService):
        self.survey_service = survey_service
        self.survey_responses_service = survey_responses_service
        self.user_service = user_service

    def handle(self, command: AnswerSurveyWebsiteCommand):
        try:
            allowed_options = ['yes', 'no', 'maybe']
            option = command.response.strip().lower()
            if option not in allowed_options:
                return {"message": "Invalid response value.", "status": 400}
            
            user = self.user_service.get_user_id_by_ssid(command.ssid, command.ip_address)
            if not user:
                return {"message": "User not authenticated.", "status": 403}
            
            survey = self.survey_service.getSurvey(command.survey_id)
            if not survey:
                return {"message": "Survey not found.", "status": 404}

            now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)  
            survey_end_time = survey.ending_time.replace(tzinfo=timezone.utc)

            if survey_end_time < now_utc:
                return {"message": "Survey has expired.", "status": 400}

            survey_response = self.survey_responses_service.get_by_survey_id_and_email(command.survey_id, user.email)

            if survey_response:
                if survey_response.response.lower() != "no response":
                    return {"message": "Survey already answered.", "status": 400}
                
                survey_response.response = option
                survey_response.responded_time = now_utc
                self.survey_responses_service.update(survey_response)
            else:
                return {"message": "Survey answer doesn't exist.", "status": 500}

            confirm_command = SendSurveyResponseConfirmationEmailCommand(
                recipient=user.email,
                survey_title=survey.title,
                response=option,
                survey_id=command.survey_id,
                subject="Survey Response Confirmation"
            )
            mediator = current_app.config.get("mediator")
            mediator.send(confirm_command)
            
            return {"message": "Survey response recorded successfully.", "status": 200}
        except ValueError as err:
            if err.args and isinstance(err.args[0], dict):
                error_info = err.args[0]
                message = error_info.get("message", "An unexpected error occurred.")
                status = error_info.get("status", 500)
                return {"message": message, "status": status}
        except Exception as ex:
            if ex.args and isinstance(ex.args[0], dict):
                error_info = ex.args[0]
                message = error_info.get("message", "An unexpected error occurred.")
                status = error_info.get("status", 500)
            else:
                message = "An unexpected error occurred."
                status = 500
            return {"message": message, "status": status}