from .models import User, Session
from ...core.extensions import db
from sqlalchemy import and_
import uuid
from datetime import datetime


class UserRepository:
    @staticmethod
    def add(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_by_email(email: str) -> User:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def updateUser(user):
        try:
            db.session.add(user)  # Dodaj korisnika u sesiju
            db.session.commit()  # Ove promene će biti sačuvane u bazi
        except Exception as e:
            db.session.rollback()  # U slučaju greške, poništi promene
            raise e
    
class SessionRepository:
    @staticmethod
    def add(session):
        db.session.add(session)
        db.session.commit()

    @staticmethod
    def get_active_by_user_id(id: uuid.UUID, ip_address: str):
        try:
            pass
            #user_uuid = uuid.UUID(id)
        except ValueError:
            raise ValueError({"message":"Invalid ID", "status": 400})
        current_time = datetime.utcnow()

        active_session = Session.query.filter(
            and_(
                Session.user_id == id,
                Session.logged_out == False,
                Session.ip_address == ip_address,
                Session.started_time <= current_time,
                Session.ending_time >= current_time
            )
        ).first()
        
        return active_session
    
    @staticmethod
    def get_by_id(id: uuid):
        ssid = uuid.UUID(id)
        return Session.query.filter_by(id=ssid).first()
    
    @staticmethod
    def get_active_by_id(id: uuid.UUID, ip_address) -> Session:
        current_time = datetime.utcnow()
        return Session.query.filter(
            and_(
                Session.id == id,
                Session.logged_out == False,
                Session.ip_address == ip_address,
                Session.started_time <= current_time,
                Session.ending_time >= current_time
            )
        ).first()
        
    @staticmethod
    def update(session):
        try:
            db.session.commit()  
        except Exception as e:
            db.session.rollback()  
            raise e