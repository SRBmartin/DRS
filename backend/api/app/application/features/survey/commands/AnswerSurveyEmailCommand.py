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
        allowed_options = ['yes', 'no', 'maybe']
        
        if command.option.lower() not in allowed_options:
            return {"message": "Invalid option.", "status": 400}
        
        survey = self.survey_service.getSurvey(command.survey_id)
        if not survey:
            return {"message": "Survey not found.", "status": 404}
        
        now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)  
        survey_end_time = survey.ending_time.replace(tzinfo=timezone.utc)
        
        if survey_end_time < now_utc:
            return {"message": "Survey has expired.", "status": 400}
        
        try:
            email_uuid = UUID(command.email_id)
        except Exception:
            return {"message": "Invalid email_id.", "status": 400}
        session = Session(db.engine)
        survey_email = SurveySentEmailRepository.get_by_uuid(email_uuid, session)
        if not survey_email:
            return {"message": "Email invitation not found.", "status": 404}
        
        try:
            response_uuid = UUID(command.response_id)
        except Exception:
            return {"message": "Invalid response_id.", "status": 400}
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