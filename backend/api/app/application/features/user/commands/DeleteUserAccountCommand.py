from dataclasses import dataclass
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler
from flask import request


@dataclass
class DeleteUserCommand:
    ssid: str  
    password: str  

class DeleteUserCommandHandler(IHandler):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def handle(self, command: DeleteUserCommand):
        try:
            ip_address = request.remote_addr 
            user_id = self.user_service.get_user_id_from_ssid(command.ssid, ip_address)

            if not user_id:
                return {"message": "Unauthorized", "status": 401}

            result = self.user_service.delete_user(
                user_id=user_id,
                password=command.password
            )

            return result

        except Exception as ex:
            return {"message": "An unexpected error occurred", "status": 500}
