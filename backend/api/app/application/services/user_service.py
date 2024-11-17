from ...domains.user.services import UserService

class UserApplicationService:
    @staticmethod
    def register_user(data):
        return UserService.create_user(**data)