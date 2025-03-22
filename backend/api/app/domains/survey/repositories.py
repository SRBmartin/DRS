from .models import Survey, SurveyResponses
from ...core.extensions import db

class SurveyRepository:

    @staticmethod
    def add(survey: Survey):
        db.session.add(survey)
        db.session.commit()
        
    @staticmethod
    def get_by_id(survey_id):
        return Survey.query.get(survey_id)
    
    @staticmethod
    def update_survey(survey):
        db.session.commit()

class SurveyResponsesRepository:

    @staticmethod
    def add(survey_response):
        db.session.add(survey_response)
        db.session.commit()
        
    @staticmethod
    def mark_deleted_by_survey_id(survey_id):
        updated_count = db.session.query(SurveyResponses).filter_by(survey_id=survey_id).update(
            {"is_deleted": True}
        )
        db.session.commit()
        return updated_count