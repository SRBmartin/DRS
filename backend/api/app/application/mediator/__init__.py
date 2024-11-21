from .Mediator import Mediator
from ..services.user_service import UserService
from ..features.user.commands.CreateUserCommand import CreateUserCommand, CreateUserCommandHandler

def initialize_mediator():
    mediator = Mediator()
    user_service = UserService()

    create_user_handler = CreateUserCommandHandler(user_service)
    mediator.register(CreateUserCommand, create_user_handler)

    return mediator
