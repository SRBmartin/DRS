from ...domains.survey.models import Survey, SurveyResponses
from ...domains.survey.repositories import SurveyRepository, SurveyResponsesRepository
from ...application.contracts.schemas.surveys.schemas import SurveySchema
from ...domains.user.repositories import UserRepository

class SurveyService:
    
    def createSurvey(self, user_id, title, question, ending_time, is_anonymous) -> SurveySchema:
        if not user_id or not title or not question or not ending_time:
            raise ValueError({"message":"Not all required fields are populated.", "status": 400})
        
        survey = Survey(
            user_id=user_id,
            title=title,
            question=question,
            ending_time=ending_time,
            is_anonymous=is_anonymous
        )

        SurveyRepository.add(survey)

        survey_schema = SurveySchema()
        serialized_survey_schema = survey_schema.dump(survey)

        return serialized_survey_schema
    
    def getSurveyById(self, survey_id):
        return SurveyRepository.get_by_id(survey_id)
    
    def deleteSurvey(self, survey_id):
        survey: Survey = SurveyRepository.get_by_id(survey_id)
        if not survey or survey.is_deleted:
            return {"message": "Survey not found", "status": 404}
        
        survey.is_deleted = True
        try:
            SurveyRepository.update_survey(survey)
            return {"message": "Survey deleted successfully.", "status": 200}
        except Exception as e:
            return {"message": f"Failed to delete survey: {str(e)}", "status": 500}

class SurveyResponsesService:
    
    def create(self, survey_id, email):
        user = UserRepository.get_by_email(email)
        user_id = None

        if user:
            user_id = user.id

        survey_response = SurveyResponses(
            user_id=user_id,
            survey_id=survey_id,
            email=email
        )

        SurveyResponsesRepository.add(survey_response)

        return survey_response
    
    def delete_survey_responses(self, survey_id):
        try:
            count = SurveyResponsesRepository.mark_deleted_by_survey_id(survey_id)
            print(f"Updated responses: {count}")
            print("Survey responses deleted successfully.")
            return {"message": "Survey responses deleted successfully.", "status": 200}
        except Exception as e:
            print("Survey responses not deleted successfully.")
            return {"message": f"Failed to delete survey responses: {str(e)}", "status": 500}
