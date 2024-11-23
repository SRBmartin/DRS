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
            return session
        except ValueError as err:
            if err.args and isinstance(err.args[0], dict):
                error_info = err.args[0]
                message = error_info.get("message", "An unexpected error occurred.")
                status = error_info.get("status", 500)
                return {"message": message, "status": status}
            else:
                message = "An unexpected error occurred."
                status = 500
        except Exception as ex:
            if ex.args and isinstance(ex.args[0], dict):
                error_info = ex.args[0]
                message = error_info.get("message", "An unexpected error occurred.")
                status = error_info.get("status", 500)
            else:
                message = "An unexpected error occurred."
                status = 500
            return {"message": message, "status": status}