from ...domains.user.models import User, Session
from ..contracts.schemas.user.schemas import SessionSchema, UserSchema
from ...core.extensions import db
from ...domains.user.repositories import UserRepository, SessionRepository
import uuid

class UserService:

    def register_user(self, command):
        existing_user = User.query.filter_by(email=command.email).first()

        if existing_user and not existing_user.is_deleted:
            return {"message": "An user with this email already exists.", "status": 409}

        existing_user_by_phone = User.query.filter_by(phone_number=command.phone_number).first()
        if existing_user_by_phone and not existing_user_by_phone.is_deleted:
            raise ValueError({"message": "This phone number is already in use.", "status": 400})
        
        try:
            if existing_user and existing_user.is_deleted:
                existing_user.name = command.name
                existing_user.lastname = command.lastname
                existing_user.address = command.address
                existing_user.city = command.city
                existing_user.country = command.country
                existing_user.phone_number = command.phone_number
                existing_user.hash_password(command.password)
                existing_user.is_deleted = False  
                
                session = Session(
                    user=existing_user,
                    ip_address=command.ip_address
                )

                SessionRepository.add(session)

                session_schema = SessionSchema()
                serialized_session_schema = session_schema.dump(session)

                return {"session": serialized_session_schema, "status": 201}

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

        except Exception as ex:
            return {"message": "An error occurred while registering the account.", "status": 500}

    def login_user(self, email: str, password: str, ip_address: str):
        if not email or not password or not ip_address:
            raise ValueError({"message":"Data is missing.", "status":400})
        
        user = UserRepository.get_by_email(email)
        if not user:
            raise ValueError({"message":"User is not found.", "status":404})
        
        if not user.check_password(password):
            raise ValueError({"message": "Password is incorrect.", "status": 401})
        
        if user.is_deleted == True:
            raise ValueError({"message":"User is not found.", "status":404})
        
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
                
                ses_id = uuid.UUID(ssid)
                session = SessionRepository.get_active_by_id(ses_id, ip_address)
                
                session.logged_out = True
                SessionRepository.update(session)

                return {"message": "User logged out successfully", "status": 200}
            except Exception as ex:
                return {"message": "An unexpected error occurred", "details": str(ex), "status": 500}
   
    def get_user_id_from_ssid(self, ssid: str, ip_address: str):
        try:
            session = SessionRepository.get_active_by_ssid(uuid.UUID(ssid), ip_address)

            if not session:
                return None
            return session.user_id
        except ValueError as ve:
            return None


    def delete_user(self, user_id: uuid.UUID, password: str):
        try:
            user = User.query.get(user_id)

            if not user:
                return {"message": "User not found", "status": 404}

            if not user.check_password(password):
                return {"message": "Incorrect password", "status": 401}

            user.is_deleted = True  
            UserRepository.updateUser(user)

            return {"message": "User account deleted successfully", "status": 200}

        except Exception as ex:
            return {"message": "An unexpected error occurred", "status": 500}
        
    def get_user_info(self, ssid: str, ip_address: str):
        try:
            ses_id = uuid.UUID(ssid)
        except ValueError:
            raise ValueError({"message": "You are not logged in.", "status": 401})
        
        session = SessionRepository.get_active_by_ssid(ses_id, ip_address)
        if not session:
            return {"message": "You are not logged in.", "status": 401}
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
            raise ValueError({"message": "You are not logged in.", "status": 400})
        
        session = SessionRepository.get_active_by_ssid(ses_id, ip_address)
        if not session:
            raise ({"message": "You are not logged in.", "status": 401})
        user: User
        user = UserRepository.get_by_id(session.user_id)

        if not user:
            raise ({"message": "User not found.", "status": 404})

        if not user.check_password(old_password):    
            raise ValueError({"message": "Old password is incorrect.", "status": 403})

        if user.check_password(new_password):
            raise ValueError({"message": "New password cannot be the same as the old password.", "status": 409})

        if len(str(new_password))<6:
            raise ValueError({"message": "Password must be at least 6 characters long.", "status": 422})

        user.hash_password(new_password)
        UserRepository.update_password(user.id, user.password)
        
        return {"message": "Password updated successfully.", "status": 200}
    
    def change_general_info(self, ssid, ip_address, name, lastname, email, phone_number, address, city, country):
        try:
            ses_id = uuid.UUID(ssid)
        except ValueError:
            raise ValueError({"message": "You are not logged in.", "status": 400})
        
        session = SessionRepository.get_active_by_ssid(ses_id, ip_address)
        if not session:
            raise ValueError({"message": "You are not logged in.", "status": 401})
        
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

        general_info = [name, lastname, email, phone_number, address, city, country]
        field_names = ["Name", "Lastname", "Email", "Phone Number", "Address", "City", "Country"]

        if not all(general_info):
            ret_string = "Following fields cannot be empty: "
            missing_fields = [
                field_name for field_name, value in zip(field_names, general_info) if not value
            ]
            ret_string += ", ".join(missing_fields) + "."
            raise ValueError({"message": ret_string, "status": 400})

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
        if not has_changes:
            return {"message": "No changes detected in user information.", "status": 204}

        for key, value in changes.items():
            setattr(user, key, value)

        UserRepository.update_user(user)
        
        return {"message": "User information updated successfully.", "status": 200}
    
    def get_user_id_by_ssid(self, ssid: str, ip_address: str) -> User:
        session = SessionRepository.get_active_by_id(ssid, ip_address)
        user = session.user
        
        return user
    
    def get_user_by_id(self, user_id: str):
        try:
            uid = uuid.UUID(user_id)
        except Exception:
            raise ValueError({"message": "You are not logged in.", "status": 400})
        
        user = UserRepository.get_by_id(uid)
        if not user:
            raise ValueError({"message": "User not found", "status": 404})

        return user
