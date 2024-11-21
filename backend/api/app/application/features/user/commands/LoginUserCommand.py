from dataclasses import dataclass
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler

@dataclass
class LoginUserCommand:
    email: str
    password: str
    ip_address: str

class LoginUserCommandHandler(IHandler):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def handle(self, command: LoginUserCommand):
        try:
            session = self.user_service.login_user(command.email, command.password, command.ip_address)
            return {
                "session": session
            }
        except ValueError as err:
            return err.args
        except Exception as ex:
            return ex.args