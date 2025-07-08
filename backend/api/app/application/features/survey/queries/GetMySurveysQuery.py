from dataclasses import dataclass
from ....services.survey_service import SurveyService
from ....services.user_service import UserService

@dataclass
class GetMySurveysQuery:
    ssid: str
    ip_address: str

class GetMySurveysQueryHandler:
    def __init__(self, survey_service: SurveyService, user_service: UserService):
        self.survey_service = survey_service
        self.user_service = user_service

    def handle(self, query: GetMySurveysQuery):
        try:
            user_id = self.user_service.get_user_id_by_ssid(query.ssid, query.ip_address)
            if not user_id:
                return {"message": "User not authenticated.", "status": 403}
            
            surveys = self.survey_service.get_surveys_by_user_id(user_id.id)
            if not surveys:
                return {"message": "You currently have no surveys.", "status": 200}
            
            surveys_data = []
            for survey in surveys:
                if not survey.is_deleted:
                    surveys_data.append({
                        "id": str(survey.id),
                        "title": survey.title,
                        "question": survey.question,
                        "ending_time": survey.ending_time,
                        "user_ended": survey.user_ended,
                        "is_anonymous": survey.is_anonymous
                    })

            return {"surveys": surveys_data, "status": 200}
        
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
