from dataclasses import dataclass
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler
from ....contracts.schemas.user.schemas import UpdateGeneralInformationSchema
from marshmallow import ValidationError

@dataclass
class UpdateGeneralInformationCommand:
    ssid: str
    ip_address: str
    data: dict
    
class UpdateGeneralInformationCommandHandler(IHandler):
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        
    def handle(self, command):
        schema = UpdateGeneralInformationSchema()
        try:
            validated_data = schema.load(command.data)
            return self.user_service.change_general_info(
                ssid=command.ssid,
                ip_address=command.ip_address,
                **validated_data
            )
        except ValidationError as err:
            required_fields = [
                field_name
                for field_name, field_obj in schema.fields.items()
                if field_obj.required
            ]

            missing_fields = [
                field for field in required_fields if field not in command.data or not command.data[field]
            ]

            if missing_fields:
                missing_fields_message = f"Missing required fields: {', '.join(missing_fields).capitalize() + '.'}"
                return {"message": missing_fields_message, "status": 400}

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
                message = error_info.get("message", "And unexpected error occurred.")
                status = error_info.get("status", 500)
            else:
                message = "An unexpected error occurred."
                status = 500
            return {"message": message, "status": status}