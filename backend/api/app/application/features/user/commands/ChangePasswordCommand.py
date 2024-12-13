from dataclasses import dataclass
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler

@dataclass
class ChangePasswordCommand:
    ssid: str
    ip_address: str
    old_password: str
    new_password: str
    
class ChangePasswordCommandHandler(IHandler):
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        
    def handle(self, command):
        try:
            return self.user_service.change_password(
                ssid=command.ssid,
                ip_address=command.ip_address,
                old_password=command.old_password,
                new_password=command.new_password 
            )
        except ValueError as err:
            if err.args and isinstance(err.args[0], dict):
                error_info = err.args[0]
                message = error_info.get("message", "An unexpected error occurred.")
                status = error_info.get("status", 500)
                return {"message": message, "status": status}
        except Exception as ex:
            if ex.args and isinstance(ex.args[0], dict):
                error_info = ex.args[0]
                message = error_info.get("message", "An unexpected error occurred.")
                status = error_info.get("status", 500)
            else:
                message = "An unexpected error occurred."
                status = 500
            return {"message": message, "status": status}        