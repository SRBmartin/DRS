from dataclasses import dataclass
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler

@dataclass
class GetGeneralInfoQuery:
    user_id: str
    
class GetGeneralInfoQueryHandler(IHandler):
    def __init__(self, user_service: UserService):
        self.user_service = user_service 
        
    def handle(self, query: GetGeneralInfoQuery):
        try:
            user_info = self.user_service.get_user_info(query.user_id)
            return user_info
        except ValueError as err:
            if err.args and isinstance(err.args[0], dict):
                error_info = err.args[0]
                return {"message": error_info.get("message", "An unexpected error occurred."), "status": error_info.get("status", 500)}
        except Exception:
            return {"message": "An unexpected error occurred.", "status": 500}