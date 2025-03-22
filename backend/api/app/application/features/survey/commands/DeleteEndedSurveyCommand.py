from dataclasses import dataclass
import datetime

from .....domains.survey.models import Survey
from .....application.services.survey_service import SurveyResponsesService, SurveyService

@dataclass
class DeleteEndedSurveyCommand:
    survey_id: str
    
class DeleteEndedSurveyCommandHandler:
    def __init__(self, survey_service: SurveyService, survey_responses_service: SurveyResponsesService):
        self.survey_service = survey_service
        self.survey_responses_service = survey_responses_service

    def handle(self, command: DeleteEndedSurveyCommand):
        try:
            survey: Survey = self.survey_service.getSurveyById(command.survey_id)
            now_utc = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)  
            survey_end_time = survey.ending_time.replace(tzinfo=datetime.timezone.utc)
            print(survey.is_deleted)
            print(f"now_utc: {now_utc}\nsurvey end time: {survey_end_time}")
            if survey.is_deleted:
                return {"message": "Survey does not exist.", "status": 404}                

            if survey_end_time > now_utc and not(survey.user_ended):
                return {"message": "Survey is still in progress.", "status": 400}
            
            retValSurvey = self.survey_service.deleteSurvey(command.survey_id)
            if retValSurvey["status"] == 500:
                return {"message": "An error occurred.", "status": 500}
            elif retValSurvey["status"] != 200:
                return {"message": "An error occurred.", "status": 400}
            
            retValSurveyResponses = self.survey_responses_service.delete_survey_responses(command.survey_id)
            if retValSurveyResponses["status"] == 500:
                return {"message": "An error occurred.", "status": 500}
            elif retValSurveyResponses["status"] != 200:
                return {"message": "An error occurred.", "status": 400}
        
            return {"message": "Survey deleted successfully.", "status": 200}
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