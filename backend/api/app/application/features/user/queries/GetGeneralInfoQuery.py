from dataclasses import dataclass
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler
#import uuid

@dataclass
class GetGeneralInfoQuery:
    ssid: str
    ip_address: str
    
class GetGeneralInfoQueryHandler(IHandler):
    def __init__(self, user_service: UserService):
        self.user_service = user_service 
        
    def handle(self, query: GetGeneralInfoQuery):

        try:
            session_response = self.user_service.get_user_info(query.ssid, query.ip_address)
            return session_response
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
    