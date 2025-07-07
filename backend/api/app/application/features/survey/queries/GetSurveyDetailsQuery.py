from dataclasses import dataclass
from datetime import datetime

from ....services.survey_service import SurveyResponsesService,SurveyService
from ....services.user_service import UserService

@dataclass
class GetSurveyDetailsQuery:
    survey_id: str
    ssid: str
    ip_address: str

class GetSurveyDetailsQueryHandler:
    def __init__(self, survey_responses_service: SurveyResponsesService, survey_service: SurveyService, user_service: UserService):
        self.survey_responses_service = survey_responses_service
        self.survey_service = survey_service
        self.user_service = user_service
        
    def handle(self, query: GetSurveyDetailsQuery):
        try:
            
            user_id = self.user_service.get_user_id_by_ssid(query.ssid, query.ip_address)
            if not user_id:
                return {"message": "User not authenticated.", "status": 403}
            
            survey = self.survey_service.get_survey_by_id(query.survey_id)

            if not survey:
                return {"message": "Survey not found", "status": 404}
                        
            if survey.is_deleted:
                return {"message": "Survey not found", "status": 404}
            
            if user_id.id != survey.user_id:
                return {"message": "Unauthorized", "status": 401}
            
            response_counts = self.survey_responses_service.count_responses_by_survey_id(query.survey_id)
            
            responses_with_users = None
            if not survey.is_anonymous:
                responses_with_users = self.survey_responses_service.get_responses_with_users(query.survey_id)
    
            return {
                "title": survey.title,
                "question": survey.question,
                "ending_time": survey.ending_time,
                "user_ended": survey.user_ended,
                "is_anonymous": survey.is_anonymous,
                "responses": response_counts,
                "user_responses": responses_with_users if responses_with_users is not None else [],
                "status": 200
            }          
            
        except ValueError as err:
            if err.args and isinstance(err.args[0], dict):
                error_info = err.args[0]
                message = error_info.get("message", "An unexpected error occurred.")
                status = error_info.get("status", 500)
                return {"message": message, "status": status}
            else:
                message = "An unexpected error occurred."
                status = 500
        except Exception as ex:
            if ex.args and isinstance(ex.args[0], dict):
                error_info = ex.args[0]
                message = error_info.get("message", "An unexpected error occurred.")
                status = error_info.get("status", 500)
            else:
                message = "An unexpected error occurred."
                status = 500
            return {"message": message, "status": status}