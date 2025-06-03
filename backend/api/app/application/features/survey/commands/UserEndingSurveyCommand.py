import datetime
from typing import List
from dataclasses import dataclass

from app.domains.survey.models import Survey
from ....services.survey_service import SurveyResponsesService, SurveyService
from ....contracts.IHandler import IHandler

@dataclass
class UserEndingSurveyCommand:
    survey_id:str
    #emails: List[str]
class UserEndingSurveyCommandHandler(IHandler):
    def __init__(self, survey_service: SurveyService, survey_response_service: SurveyResponsesService):
        self.survey_service = survey_service
        self.survey_response_service = survey_response_service

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
            survey.ending_time = now_utc
            update_status = self.survey_service.updateSurvey(survey)

            if update_status["status"] != 200:
                return {"message": "Failed to update survey.", "status": 500}
            
           # pending_users = self.survey_responses_service.get_pending_users(command.survey_id)
            #self.email_service.notify_users_survey_ended(command.survey_id, pending_users)
            
            return {"message": "Survey ended successfully.", "status": 200}
        

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

