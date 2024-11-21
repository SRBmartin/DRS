from dataclasses import dataclass
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler

@dataclass
class CreateUserCommand:
    name: str
    lastname: str
    address: str
    city: str
    country: str
    phone_number: str
    email: str
    password: str
    ip_address: str

class CreateUserCommandHandler(IHandler):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def handle(self, command: CreateUserCommand):
        try:
            session = self.user_service.register_user(command)
            return {
                "session": session
            }
        except ValueError as err:
            return {err.args}
        except Exception as ex:
            return {ex.args}