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