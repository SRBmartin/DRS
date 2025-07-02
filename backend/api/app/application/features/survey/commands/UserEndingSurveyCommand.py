from dataclasses import dataclass
from typing import List
import datetime
from flask import current_app

from app.domains.survey.models import Survey
from ....services.survey_service import SurveyResponsesService, SurveyService
from ....contracts.IHandler import IHandler
from ...email.commands.SendSurveyEndedEmailHandler import SendSurveyEndedEmailCommand
@dataclass
class UserEndingSurveyCommand:
    survey_id: str

class UserEndingSurveyCommandHandler(IHandler):
    def __init__(self, survey_service: SurveyService, survey_responses_service: SurveyResponsesService):
        self.survey_service = survey_service
        self.survey_responses_service = survey_responses_service

    def handle(self, command: UserEndingSurveyCommand):
        try:
            survey: Survey = self.survey_service.get_survey_by_id(command.survey_id)
            if not survey:
                raise ValueError({"message": "Survey not found.", "status": 404})
            
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            if survey.ending_time.tzinfo is None:
                survey.ending_time = survey.ending_time.replace(tzinfo=datetime.timezone.utc)

            if (survey.ending_time.tzinfo and survey.ending_time <= now_utc) or survey.user_ended:
                return {"message": "Survey is already ended.", "status": 400}

            survey.user_ended = True
            update_status = self.survey_service.updateSurvey(survey)

            if update_status["status"] != 200:
                return {"message": "Failed to update survey.", "status": 500}

            pending_users = self.survey_responses_service.get_pending_users(command.survey_id)
            print(pending_users)
            if pending_users:
                self._init_send_mails(pending_users, survey)

            return {"message": "Survey ended successfully.", "status": 200}
        
        except ValueError as err:
            if err.args and isinstance(err.args[0], dict):
                return err.args[0]
        except Exception as ex:
            return {"message": "An unexpected error occurred.", "status": 500}
        
    def _init_send_mails(self, emails: List[str], survey: Survey):
        command = SendSurveyEndedEmailCommand(
                recipients=emails,
                survey_title=survey.title,
                survey_id = survey.id
            )
        
        mediator = current_app.config.get('mediator')
        mediator.send(command)
        