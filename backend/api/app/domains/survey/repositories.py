from .models import Survey, SurveyResponses
from ...core.extensions import db

class SurveyRepository:

    @staticmethod
    def add(survey: Survey):
        db.session.add(survey)
        db.session.commit()
        
    @staticmethod
    def get_survey_by_id(survey_id):
        return Survey.query.get(survey_id)
    
    @staticmethod
    def update(survey: Survey):
        db.session.merge(survey)
        db.session.commit()

class SurveyResponsesRepository:

    @staticmethod
    def add(survey_response):
        db.session.add(survey_response)
        db.session.commit()
        
    @staticmethod
    def get_yes_count(survey_id: str) -> int:
        return SurveyResponses.query.filter_by(
            survey_id=survey_id,
            response='yes'
        ).count()
        
    @staticmethod
    def get_no_count(survey_id: str) -> int:
        return SurveyResponses.query.filter_by(
            survey_id=survey_id,
            response='no'
        ).count()

    @staticmethod
    def get_maybe_count(survey_id: str) -> int:
        return SurveyResponses.query.filter_by(
            survey_id=survey_id,
            response='no response'
        ).count()
        
    @staticmethod
    def get_all_responses_with_users(survey_id: str):
        return SurveyResponses.query.filter_by(survey_id=survey_id).all()
    
    @staticmethod
    def get_responses_by_survey_id_and_response(survey_id: str, response: str):
        return SurveyResponses.query.filter_by(survey_id=survey_id, response=response).all()
