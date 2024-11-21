from ...domains.user.models import User, Session
from ...domains.user.schemas import SessionSchema
from ...core.extensions import db
from ...domains.user.repositories import UserRepository, SessionRepository

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

            return serialized_session_schema
        except Exception:
            return {"message":"There was an error while registering account.", "status":500}