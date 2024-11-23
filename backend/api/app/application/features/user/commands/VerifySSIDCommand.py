from dataclasses import dataclass
from ....services.user_service import UserService
from ....contracts.IHandler import IHandler

@dataclass
class VerifySSIDCommand:
    ssid: str
    ip_address: str

class VerifySSIDCommandHandler(IHandler):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def handle(self, command: VerifySSIDCommand):
        try:
            return self.user_service.verifySSID(command.ssid, command.ip_address)
        except ValueError:
            return False
        except Exception:
            return False