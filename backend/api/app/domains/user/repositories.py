from .models import User, Session
from ...core.extensions import db
from sqlalchemy import and_
import uuid
from datetime import datetime
from ...infrastructure.utils.time import now


class UserRepository:
    @staticmethod
    def add(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_by_email(email: str) -> User:
        return User.query.filter_by(email=email, is_deleted=False).first()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def updateUser(user):
            db.session.add(user)  
            db.session.commit()  
        
    def update_password(user_id: uuid.UUID, hashed_password: str):
        user = User.query.get(user_id)
        if not user:
            raise ValueError({"message": "User not found.", "status": 404})
        user.password = hashed_password
        db.session.commit()
        
    @staticmethod
    def update_user(user: User):
        db.session.commit()
        
    @staticmethod
    def get_by_phone_number(phone_number: str):
        return User.query.filter_by(phone_number=phone_number, is_deleted=False).first()

class SessionRepository:
    @staticmethod
    def add(session):
        db.session.add(session)
        db.session.commit()

    @staticmethod
    def get_active_by_user_id(id: uuid.UUID, ip_address: str):
        current_time = now()
        
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
        current_time = now()
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
        
    @staticmethod
    def get_active_by_ssid(ssid: uuid.UUID, ip_address: str):
        try:
            pass
            #user_uuid = uuid.UUID(id)
        except ValueError:
            raise ValueError({"message":"Invalid ID", "status": 400})
        current_time = now()

        active_session = Session.query.filter(
            and_(
                Session.id == ssid,
                Session.logged_out == False,
                Session.ip_address == ip_address,
                Session.started_time <= current_time,
                Session.ending_time >= current_time
            )
        ).first()
        
        return active_session
