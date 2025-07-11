from .Mediator import Mediator
from ...core.config import Config
from ..services.user_service import UserService
from ..services.survey_service import SurveyService, SurveyResponsesService
from ..services.email_service import EmailService
from ..features.user.commands.CreateUserCommand import CreateUserCommand, CreateUserCommandHandler
from ..features.user.commands.LoginUserCommand import LoginUserCommand, LoginUserCommandHandler
from ..features.user.commands.VerifySSIDCommand import VerifySSIDCommand, VerifySSIDCommandHandler
from ..features.user.commands.LogoutUserCommand import LogoutUserCommand,LogoutUserCommandHandler
from ..features.user.commands.DeleteUserAccountCommand import DeleteUserCommand, DeleteUserCommandHandler
from ..features.user.queries.GetGeneralInfoQuery import GetGeneralInfoQuery, GetGeneralInfoQueryHandler
from ..features.user.commands.ChangePasswordCommand import ChangePasswordCommand, ChangePasswordCommandHandler
from ..features.user.commands.UpdateGeneralInfoCommand import UpdateGeneralInformationCommand, UpdateGeneralInformationCommandHandler
from ..features.survey.commands.CreateSurveyCommand import CreateSurveyCommand, CreateSurveyCommandHandler
from ..features.email.commands.SurveyCreatedEmailSendCommand import SendSurveyCreatedEmailCommand, SendSurveyCreatedEmailHandler
from ..features.survey.queries.GetSurveyDetailsQuery import GetSurveyDetailsQuery, GetSurveyDetailsQueryHandler
from ..features.email.commands.SurveyResponseConfirmationEmailCommand import SendSurveyResponseConfirmationEmailCommand, SendSurveyResponseConfirmationEmailHandler
from ..features.survey.commands.AnswerSurveyEmailCommand import AnswerSurveyEmailLinkCommand, AnswerSurveyEmailLinkCommandHandler
from ..features.survey.commands.AnswerSurveyWebsiteCommand import AnswerSurveyWebsiteCommandHandler, AnswerSurveyWebsiteCommand
from ..features.survey.queries.GetSurveyAnswerDetailsQuery import GetSurveyAnswerDetailsQuery, GetSurveyAnswerDetailsQueryHandler
from ..features.survey.queries.GetMySurveysQuery import GetMySurveysQuery, GetMySurveysQueryHandler
from ..features.survey.queries.GetSurveysForMeQuery import GetSurveysForMeQuery, GetSurveysForMeQueryHandler

from ..features.survey.commands.DeleteEndedSurveyCommand import DeleteEndedSurveyCommand, DeleteEndedSurveyCommandHandler
from ..features.survey.commands.UserEndingSurveyCommand  import UserEndingSurveyCommand, UserEndingSurveyCommandHandler
from ..features.email.commands.SendSurveyEndedEmailHandler import SendSurveyEndedEmailHandler, SendSurveyEndedEmailCommand

def initialize_mediator(flask_app):
    mediator = Mediator()
    user_service = UserService()
    survey_service = SurveyService()
    survey_responses_service = SurveyResponsesService()
    email_serice = EmailService(Config.EMAIL_SERVICE_URL, Config.EMAIL_SERVICE_API)

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

    general_info_handler = GetGeneralInfoQueryHandler(user_service)
    mediator.register(GetGeneralInfoQuery, general_info_handler)
    
    change_password_handler = ChangePasswordCommandHandler(user_service)
    mediator.register(ChangePasswordCommand, change_password_handler)
    
    update_general_info_handler = UpdateGeneralInformationCommandHandler(user_service)
    mediator.register(UpdateGeneralInformationCommand, update_general_info_handler)

    create_survey_handler = CreateSurveyCommandHandler(survey_service, user_service)
    mediator.register(CreateSurveyCommand, create_survey_handler)

    send_created_survey_email_handler = SendSurveyCreatedEmailHandler(email_serice, survey_responses_service, flask_app)
    mediator.register(SendSurveyCreatedEmailCommand, send_created_survey_email_handler)
    
    get_survey_details_handler = GetSurveyDetailsQueryHandler(survey_responses_service, survey_service, user_service)
    mediator.register(GetSurveyDetailsQuery, get_survey_details_handler)
    
    send_survey_response_confirmation_handler = SendSurveyResponseConfirmationEmailHandler(email_serice, flask_app)
    mediator.register(SendSurveyResponseConfirmationEmailCommand, send_survey_response_confirmation_handler)
    
    answer_survey_email_handler = AnswerSurveyEmailLinkCommandHandler(survey_service, survey_responses_service)
    mediator.register(AnswerSurveyEmailLinkCommand, answer_survey_email_handler)
    
    answer_survey_website_handler = AnswerSurveyWebsiteCommandHandler(survey_service, survey_responses_service, user_service)
    mediator.register(AnswerSurveyWebsiteCommand, answer_survey_website_handler)
    
    get_survey_answer_details_handler = GetSurveyAnswerDetailsQueryHandler(survey_service)
    mediator.register(GetSurveyAnswerDetailsQuery, get_survey_answer_details_handler)
    
    get_my_surveys_handler = GetMySurveysQueryHandler(survey_service, user_service)
    mediator.register(GetMySurveysQuery, get_my_surveys_handler)
    
    get_surveys_for_me_handler = GetSurveysForMeQueryHandler(survey_service, survey_responses_service, user_service)
    mediator.register(GetSurveysForMeQuery, get_surveys_for_me_handler)
    delete_ended_survey_handler = DeleteEndedSurveyCommandHandler(survey_service, survey_responses_service)
    mediator.register(DeleteEndedSurveyCommand, delete_ended_survey_handler)
    
    user_ending_survey_handler = UserEndingSurveyCommandHandler(survey_service, survey_responses_service)
    mediator.register(UserEndingSurveyCommand, user_ending_survey_handler)

    send_survey_ended_email_handler = SendSurveyEndedEmailHandler(email_serice, flask_app)
    mediator.register(SendSurveyEndedEmailCommand, send_survey_ended_email_handler)
    
    return mediator
