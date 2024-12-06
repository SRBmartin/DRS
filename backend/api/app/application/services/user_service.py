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
        
        if user.is_deleted == True:
            raise ValueError({"message":"User does not exist.", "status":404})
        
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
        
    def logout_user(self, ssid: str, ip_address: str):
            try:
                if not ssid:
                    return {"message": "SSID is required", "status": 400}

                try:
                    ses_id = uuid.UUID(ssid)
                except ValueError:
                    return {"message": "Invalid SSID format", "status": 400}

                session = SessionRepository.get_active_by_id(ses_id, ip_address)
                if not session:
                    return {"message": "Session not found", "status": 404}

                session.logged_out = True
                SessionRepository.update(session)

                return {"message": "User logged out successfully", "status": 200}

            except ValueError as ve:
                return {"message": str(ve), "status": 400}

            except Exception as ex:
                return {"message": "An unexpected error occurred", "details": str(ex), "status": 500}
            
    def delete_user(self, user_id: uuid.UUID, password: str):
        try:
            print(f"Received password: {password}")
            print(f"Received user_id (SSID): {user_id}")

            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found", "status": 404}

            if not user.check_password(password):
                print("Incorrect password provided.")
                return {"message": "Incorrect password", "status": 401}

            print(f"Before updating user, is_deleted: {user.is_deleted}")

            user.is_deleted = True  
            UserRepository.updateUser(user)
            print(f"after updating user, is_deleted: {user.is_deleted}")

            return {"message": "User account deleted successfully", "status": 200}

        except Exception as ex:
            print(f"Error during delete operation: {str(ex)}")
            return {"message": "An unexpected error occurred", "status": 500}
