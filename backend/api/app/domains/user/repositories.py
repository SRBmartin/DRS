from .models import User
from ...core.extensions import db

class UserRepository:
    @staticmethod
    def add(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_all():
        return User.query.all()
    
class SessionRepository:
    @staticmethod
    def add(session):
        db.session.add(session)
        db.session.commit()