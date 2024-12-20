from dataclasses import dataclass
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler
from ....contracts.schemas.user.schemas import ChangePasswordSchema
from marshmallow import ValidationError

@dataclass
class ChangePasswordCommand:
    ssid: str
    ip_address: str
    data: dict
    
class ChangePasswordCommandHandler(IHandler):
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        
    def handle(self, command):
        schema =  ChangePasswordSchema()
        try:
            validated_data = schema.load(command.data)
            return self.user_service.change_password(
                ssid=command.ssid,
                ip_address=command.ip_address,
                old_password=validated_data["old_password"],
                new_password=validated_data["new_password"]
            )
        except ValidationError as err:
            return {
                "message": "Validation failed.",
                "status": 400
            }
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