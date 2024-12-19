from dataclasses import dataclass
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler


@dataclass
class LogoutUserCommand:
    ssid: str  
    ip_address: str  

class LogoutUserCommandHandler(IHandler):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def handle(self, command: LogoutUserCommand):
        try:
            result = self.user_service.logout_user(command.ssid, command.ip_address)
            return result
        except Exception as ex:
            if ex.args and isinstance(ex.args[0], dict):
                error_info = ex.args[0]
                message = error_info.get("message", "An unexpected error occurred.")
                status = error_info.get("status", 500)
            else:
                message = "An unexpected error occurred."
                status = 500
            return {"message": message, "status": status}
