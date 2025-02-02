from dataclasses import dataclass
from ....services.survey_service import SurveyService
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler
from typing import List
from ...email.commands.SurveyCreatedEmailSendCommand import SendSurveyCreatedEmailCommand
from flask import current_app

@dataclass
class CreateSurveyCommand:
    ssid: str
    ip_address: str
    title: str
    question: str
    ending_time: str
    is_anonymous: bool
    emails: List[str]

class CreateSurveyCommandHandler(IHandler):
    def __init__(self, survey_service: SurveyService, user_service: UserService):
        self.survey_service = survey_service
        self.user_service = user_service

    def handle(self, command: CreateSurveyCommand):
        try:
            user = self.user_service.get_user_id_by_ssid(command.ssid, command.ip_address)
            if not user:
                return {"message": "Not logged in.", "status": 403}
            
            user_id = user.id

            survey = self.survey_service.createSurvey(
                user_id,
                command.title,
                command.question,
                command.ending_time,
                command.is_anonymous)
            
            self._init_send_mails(command.emails, survey)

            return {
                "survey": survey,
                "status": 201
            }
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
                #message = "An unexpected error occurred."
                message = str(ex)
                status = 500
            return {"message": message, "status": status}
    
    def _init_send_mails(self, emails: List[str], survey):
        command = SendSurveyCreatedEmailCommand(
            recipients=emails,
            survey_title=survey["title"],
            survey_id=str(survey["id"]),
            is_anonymous=survey["is_anonymous"],
            question=survey["question"],
            subject="Invitation to participate in a survey"
        )
        
        mediator = current_app.config.get('mediator')
        mediator.send(command)