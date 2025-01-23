from .models import Survey
from ...core.extensions import db

class SurveyRepository:

    @staticmethod
    def add(survey: Survey):
        db.session.add(survey)
        db.session.commit()