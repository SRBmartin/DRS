from dataclasses import dataclass

from ....contracts.schemas.surveys.schemas import SurveySchema
from ....services.survey_service import SurveyService
from ....contracts.IHandler import IHandler

@dataclass
class GetSurveyAnswerDetailsQuery:
    survey_id: str
    
class GetSurveyAnswerDetailsQueryHandler(IHandler):
    def __init__(self, survey_service: SurveyService):
        self.survey_service = survey_service
        
    def handle(self, query: GetSurveyAnswerDetailsQuery):
        try:
            survey = self.survey_service.getSurvey(query.survey_id)
            
            if survey.is_deleted:
                return {"message": "Survey not fount.", "status": 404}
            
            survey_schema = SurveySchema()
            survey_data = survey_schema.dump(survey)
            
            if not survey_data:
                return {"message": "Survey not found.", "status": 404}
            
            return {
                "message": "Survey details retrieved successfully",
                "data": survey_data,
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