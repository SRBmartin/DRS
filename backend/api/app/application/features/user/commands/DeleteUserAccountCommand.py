from dataclasses import dataclass
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler
import uuid  


@dataclass
class DeleteUserCommand:
    user_id: uuid.UUID  
    password: str  

class DeleteUserCommandHandler(IHandler):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def handle(self, command: DeleteUserCommand):
        try:
            result = self.user_service.delete_user(
                user_id=command.user_id,  
                password=command.password
            )
            return result
        except Exception as ex:
            print(f"Error during delete operation: {str(ex)}")
            if ex.args and isinstance(ex.args[0], dict):
                error_info = ex.args[0]
                message = error_info.get("message", "An unexpected error occurred.")
                status = error_info.get("status", 500)
            else:
                message = "An unexpected error occurred."
                status = 500
            return {"message": message, "status": status}
