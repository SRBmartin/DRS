from dataclasses import dataclass
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler

@dataclass
class UpdateGeneralInformationCommand:
    ssid: str
    ip_address: str
    name: str
    lastname: str
    email: str
    phone_number: str
    address: str
    city: str
    country: str
    
class UpdateGeneralInformationCommandHandler(IHandler):
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        
    def handle(self, command):
        try:
            return self.user_service.change_general_info(
                ssid=command.ssid,
                ip_address=command.ip_address,
                name=command.name,
                lastname=command.lastname,
                email=command.email,
                phone_number=command.phone_number,
                address=command.address,
                city=command.city,
                country=command.country
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