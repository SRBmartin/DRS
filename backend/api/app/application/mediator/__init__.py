from .Mediator import Mediator
from ..services.user_service import UserService
from ..features.user.commands.CreateUserCommand import CreateUserCommand, CreateUserCommandHandler
from ..features.user.commands.LoginUserCommand import LoginUserCommand, LoginUserCommandHandler
from ..features.user.commands.VerifySSIDCommand import VerifySSIDCommand, VerifySSIDCommandHandler
from ..features.user.commands.LogoutUserCommand import LogoutUserCommand,LogoutUserCommandHandler
from ..features.user.commands.DeleteUserAccountCommand import DeleteUserCommand, DeleteUserCommandHandler

def initialize_mediator():
    mediator = Mediator()
    user_service = UserService()

    create_user_handler = CreateUserCommandHandler(user_service)
    mediator.register(CreateUserCommand, create_user_handler)

    login_user_handler = LoginUserCommandHandler(user_service)
    mediator.register(LoginUserCommand, login_user_handler)

    verify_ssid_handler = VerifySSIDCommandHandler(user_service)
    mediator.register(VerifySSIDCommand, verify_ssid_handler)
    
    logout_user_handler = LogoutUserCommandHandler(user_service)  
    mediator.register(LogoutUserCommand, logout_user_handler)
    
    delete_user_account_handler = DeleteUserCommandHandler(user_service)
    mediator.register(DeleteUserCommand, delete_user_account_handler)

    return mediator
