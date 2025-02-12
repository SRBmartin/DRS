from dataclasses import dataclass
from datetime import datetime
from flask import current_app, g
from ....contracts.IHandler import IHandler
from .....domains.survey.repositories import SurveyRepository, SurveyResponsesRepository
from .....domains.survey.models import SurveyResponses

@dataclass
class AnswerSurveyWebsiteCommand:
    survey_id: str
    response: str

class AnswerSurveyWebsiteCommandHandler(IHandler):
    def handle(self, command: AnswerSurveyWebsiteCommand):
        allowed_responses = ["yes", "no", "maybe"]
        if command.response.lower() not in allowed_responses:
            return {"message": "Invalid response value.", "status": 400}

        survey = SurveyRepository.get_by_id(command.survey_id)
        if not survey:
            return {"message": "Survey not found.", "status": 404}
        if survey.ending_time < datetime.utcnow():
            return {"message": "Survey has expired.", "status": 400}

        # Get the authenticated user (set by your middleware)
        user = getattr(g, "user", None)
        if not user:
            return {"message": "User not authenticated.", "status": 403}

        # Check if the user has already responded to this survey
        existing_response = SurveyResponsesRepository.get_by_survey_and_user(command.survey_id, user.id)
        if existing_response and existing_response.response.lower() != "no response":
            return {"message": "Survey already answered.", "status": 400}

        now = datetime.utcnow()
        if existing_response:
            existing_response.response = command.response.lower()
            existing_response.responded_time = now
            SurveyResponsesRepository.update(existing_response)
        else:
            new_response = SurveyResponses(
                user_id=user.id,
                survey_id=command.survey_id,
                email=user.email,  # use the authenticated user's email
                response=command.response.lower(),
                responded_time=now
            )
            SurveyResponsesRepository.add(new_response)

        # Trigger a confirmation email (the email content is defined in a dedicated template)
        #from ....application.features.survey.commands.SendSurveyResponseConfirmationEmailCommand import SendSurveyResponseConfirmationEmailCommand
        # confirm_command = SendSurveyResponseConfirmationEmailCommand(
        #     recipient=user.email,
        #     survey_title=survey.title,
        #     response=command.response.lower(),
        #     survey_id=command.survey_id,
        #     subject="Survey Response Confirmation"
        # )
        # mediator = current_app.config.get("mediator")
        # mediator.send(confirm_command)

        return {"message": "Survey response recorded successfully.", "status": 200}
