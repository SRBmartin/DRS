from ...domains.user.models import User, Session
from ..contracts.schemas.user.schemas import SessionSchema
from ...core.extensions import db
from ...domains.user.repositories import UserRepository, SessionRepository
import uuid

class UserService:

    def register_user(self, command):
        existing_user = User.query.filter_by(email=command.email).first()
        if existing_user:
            return {"message": "Email already exists", "status": 409}
        
        try:
            user = User(
                name=command.name,
                lastname=command.lastname,
                address=command.address,
                city=command.city,
                country=command.country,
                phone_number=command.phone_number,
                email=command.email,
            )
            user.hash_password(command.password)

            session = Session(
                user=user,
                ip_address=command.ip_address
            )

            UserRepository.add(user)
            SessionRepository.add(session)

            session_schema = SessionSchema()

            serialized_session_schema = session_schema.dump(session)

            return {"session": serialized_session_schema, "status": 201}
        except Exception:
            return {"message":"There was an error while registering account.", "status":500}

    def login_user(self, email: str, password: str, ip_address: str):
        if not email or not password or not ip_address:
            raise ValueError({"message":"Data is missing.", "status":400})
        
        user = UserRepository.get_by_email(email)
        if not user:
            raise ValueError({"message":"User is not found.", "status":404})
        
        if not user.check_password(password):
            raise ValueError({"message": "Password is incorrect.", "status": 401})
        
        active_session = SessionRepository.get_active_by_user_id(user.id, ip_address)
        if not active_session:
            session = Session(
                user=user,
                ip_address=ip_address
            )
            SessionRepository.add(session)
            new_session = session
        else:
            new_session = active_session

        session_schema = SessionSchema()
        serialized_session = session_schema.dump(new_session)

        return { "session": serialized_session, "status": 200 }
    
    def verifySSID(self, ssid: str, ip_address: str):
        if not ssid:
            raise ValueError({"message":"Data is missing.", "status":400})
        
        ses_id = uuid.UUID(ssid)
        session = SessionRepository.get_active_by_id(ses_id, ip_address)
        if session:
            return True
        else:
            return False
