from .models import Survey
from ...core.extensions import db

class SurveyRepository:

    @staticmethod
    def add(survey: Survey):
        db.session.add(survey)
        db.session.commit()

class SurveyResponsesRepository:

    @staticmethod
    def add(survey_response):
        db.session.add(survey_response)
        db.session.commit()