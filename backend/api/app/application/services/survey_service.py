from ...domains.survey.models import Survey
from ...domains.survey.repositories import SurveyRepository
from ...application.contracts.schemas.surveys.schemas import SurveySchema

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