from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID
from flask import current_app
from sqlalchemy.orm import Session

from .....application.features.email.commands.SurveyResponseConfirmationEmailCommand import SendSurveyResponseConfirmationEmailCommand
from .....domains.email.repositories import SurveySentEmailRepository
from ....contracts.IHandler import IHandler
from .....domains.email.repositories import SurveySentEmailRepository
from .....core.extensions import db

@dataclass
class AnswerSurveyEmailLinkCommand:
    survey_id: str
    email_id: str
    response_id: str
    option: str 

class AnswerSurveyEmailLinkCommandHandler(IHandler):
    def __init__(self, survey_service, survey_responses_service):
        self.survey_service = survey_service
        self.survey_responses_service = survey_responses_service

    def handle(self, command: AnswerSurveyEmailLinkCommand):
        try:
            allowed_options = ['yes', 'no', 'maybe']
            
            if command.option.lower() not in allowed_options:
                return {"message": "Invalid option.", "status": 400}
            
            survey = self.survey_service.getSurvey(command.survey_id)
            if not survey:
                return {"message": "Survey not found.", "status": 404}
            
            if survey.user_ended:
                return {"message": "Survey has ended.", "status": 403}
            
            now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)  
            survey_end_time = survey.ending_time.replace(tzinfo=timezone.utc)
            
            if survey_end_time < now_utc:
                return {"message": "Survey has expired.", "status": 403}
            
            email_uuid = UUID(command.email_id)
            session = Session(db.engine)
            survey_email = SurveySentEmailRepository.get_by_uuid(email_uuid, session)
           
            if not survey_email:
                return {"message": "Email invitation not found.", "status": 404}
            
            response_uuid = UUID(command.response_id)
            survey_response = self.survey_responses_service.get_by_id(str(response_uuid))
            
            if not survey_response:
                return {"message": "Survey response not found.", "status": 404}
            
            if str(survey_response.survey_id) != command.survey_id or survey_response.email != survey_email.email:
                return {"message": "Mismatch in survey or email.", "status": 400}
            
            if survey_response.response.lower() != "no response":
                return {"message": "Survey already answered.", "status": 400}
            
            survey_response.response = command.option.lower()
            survey_response.responded_time = datetime.utcnow()
            self.survey_responses_service.update(survey_response)
            
            confirm_command = SendSurveyResponseConfirmationEmailCommand(
                recipient=survey_email.email,
                survey_title=survey.title,
                response=command.option.lower(),
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