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
    
    def get_survey_by_id(self, survey_id) -> Survey:
        survey = SurveyRepository.get_survey_by_id(survey_id)
        if not survey:
            raise ({"message": "Survey not found.", "status": 404})
        return survey
    
    def updateSurvey(self, updated_survey: Survey):
            print("helo")

            SurveyRepository.update(updated_survey)
            print("helo")
            return {"message": "Survey updated successfully.", "status": 200}

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
    
    def count_responses_by_survey_id(self, survey_id: str) -> dict:
        yes: int = SurveyResponsesRepository.get_yes_count(survey_id)
        no: int = SurveyResponsesRepository.get_no_count(survey_id)
        maybe: int = SurveyResponsesRepository.get_maybe_count(survey_id)
        
        return {
            "yes": yes or 0,
            "no": no or 0,
            "no_response": maybe or 0
        }
    
    def get_responses_with_users(self, survey_id: str):
        responses = SurveyResponsesRepository.get_all_responses_with_users(survey_id)
        response_list = []
        
        for response in responses:
            response_list.append({
                "email": response.email,
                "response": response.response
            })
            
        return response_list
    def get_pending_users(self, survey_id: str):
        
        responses: SurveyResponses = SurveyResponsesRepository.get_responses_by_survey_id_and_response(survey_id=survey_id, response="no response")
        if not responses:
            raise ({"message": "Survey responses not found.", "status": 404})
        
        no_response_emails = []
        for response in responses:
            no_response_emails.append(response.email)
            
        if len(no_response_emails) == 0:
            raise ({"message": "No emails found.", "status": 404})
        
        return no_response_emails
