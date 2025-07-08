from .models import Survey, SurveyResponses, SurveyResponses
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

    @staticmethod
    def get_by_id(survey_id):
        return db.session.query(Survey).filter(Survey.id == survey_id).one_or_none()
        
    @staticmethod
    def get_by_id(survey_id):
        return Survey.query.get(survey_id)
    
    @staticmethod
    def update_survey(survey):
        db.session.commit()

    @staticmethod
    def get_by_user_id(user_id):
        return Survey.query.filter_by(user_id=user_id).all()


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
            response='maybe'
        ).count()
        
    @staticmethod
    def get_all_responses_with_users(survey_id: str):
        return SurveyResponses.query.filter_by(survey_id=survey_id).all()
    
    @staticmethod
    def get_responses_by_survey_id_and_response(survey_id: str, response: str):
        return SurveyResponses.query.filter_by(survey_id=survey_id, response=response).all()

        
    @staticmethod
    def delete(survey_response):
        db.session.delete(survey_response)
        db.session.commit()
        
    @staticmethod
    def update(survey_response):
        db.session.merge(survey_response)
        db.session.commit()
        
    @staticmethod
    def get_by_id(response_id):
        return db.session.query(SurveyResponses).filter(SurveyResponses.id == response_id).one_or_none()
    
    @staticmethod
    def get_by_survey_and_email(survey_id, email):
        return db.session.query(SurveyResponses).filter(
            SurveyResponses.survey_id == survey_id,
            SurveyResponses.email == email
        ).first()
        
    @staticmethod
    def get_survey_ids_by_user_id(user_id):
        responses = SurveyResponses.query.filter_by(user_id=user_id).all()
        return list(set([response.survey_id for response in responses]))
    def mark_deleted_by_survey_id(survey_id):
        updated_count = db.session.query(SurveyResponses).filter_by(survey_id=survey_id).update(
            {"is_deleted": True}
        )
        db.session.commit()
        return updated_count
