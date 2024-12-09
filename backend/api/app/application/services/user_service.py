from ...domains.user.models import User, Session
from ..contracts.schemas.user.schemas import SessionSchema, UserSchema
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
        
    def get_user_info(self, ssid: str, ip_address: str):
        try:
            ses_id = uuid.UUID(ssid)
        except ValueError:
            raise ValueError({"message": "Invalid session ID format.", "status": 400})
        
        session = SessionRepository.get_active_by_ssid(ses_id, ip_address)
        if not session:
            return {"message": "Session is not active or IP address mismatch.", "status": 401}
        user = UserRepository.get_by_id(session.user_id)
        if not user:
            raise ({"message": "User not found.", "status": 404})
        
        user_schema = UserSchema()
        serialized_user = user_schema.dump(user)
        
        return {"user": serialized_user, "status": 200}
    
    def change_password(self, ssid, ip_address, old_password, new_password):
        try:
            ses_id = uuid.UUID(ssid)
        except ValueError:
            raise ValueError({"message": "Invalid session ID format.", "status": 400})
        
        session = SessionRepository.get_active_by_ssid(ses_id, ip_address)
        if not session:
            raise ({"message": "Session is not active or expired.", "status": 401})
        user: User
        user = UserRepository.get_by_id(session.user_id)

        if not user:
            raise ({"message": "User not found.", "status": 404})
        
        if not user.check_password(old_password):
            
            raise ValueError({"message": "Old password is incorrect.", "status": 403})

        user.hash_password(new_password)
        UserRepository.update_password(user.id, user.password)
        
        return {"message": "Password updated successfully.", "status": 200}
    
    def change_general_info(self, ssid, ip_address, name, lastname, email, phone_number, address, city, country):
        try:
            ses_id = uuid.UUID(ssid)
        except ValueError:
            raise ValueError({"message": "Invalid session ID format.", "status": 400})
        
        session = SessionRepository.get_active_by_ssid(ses_id, ip_address)
        if not session:
            raise ValueError({"message": "Session is not active or expired", "status": 401})
        
        user: User
        user = UserRepository.get_by_id(session.user_id)
        if not user:
            raise ValueError({"message": "User not found.", "status": 404})
        
        existing_user_by_email = UserRepository.get_by_email(email)
        if existing_user_by_email and existing_user_by_email.id != user.id:
            raise ValueError({"message": "This email address is already in use.", "status": 400})
        
        existing_user_by_phone = UserRepository.get_by_phone_number(phone_number)
        if existing_user_by_phone and existing_user_by_phone.id != user.id:
            raise ValueError({"message": "This phone number is already in use.", "status": 400})

        
        changes = {
            "name": name,
            "lastname": lastname,
            "email": email,
            "phone_number": phone_number,
            "address": address,
            "city": city,
            "country": country
        }        
        
        has_changes = any(getattr(user, key) != value for key, value in changes.items())
        print(f"Has changes: {has_changes}")
        if not has_changes:
            return {"message": "No changes detected in user information.", "status": 400}

        for key, value in changes.items():
            setattr(user, key, value)
        
        print(f"User: {user.address}")

        UserRepository.update_user(user)
        
        return {"message": "User information updated successfully.", "status": 200}
    
    


