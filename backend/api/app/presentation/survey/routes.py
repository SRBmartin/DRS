from flask import Blueprint, request, jsonify, current_app, g
from marshmallow.exceptions import ValidationError

from ...application.features.survey.commands.UserEndingSurveyCommand import UserEndingSurveyCommand
from ...application.contracts.schemas.surveys.schemas import SurveySchema
from ...core.services.middleware import require_auth
from ...application.features.survey.commands.CreateSurveyCommand import CreateSurveyCommand

survey_bp = Blueprint('survey', __name__, url_prefix='/survey')
survey_schema = SurveySchema()
surveys_schema = SurveySchema(many=True)

@survey_bp.route('', methods=['POST', 'OPTIONS'])
@require_auth
def create_survey():
    if request.method == 'OPTIONS':
        return '', 204
    
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message":"No data provided."}), 400
    
    try:
        survey_schema.load(json_data)
    except ValidationError:
        return jsonify({"message": "Check the fields and try again"}), 422
    
    command = CreateSurveyCommand(
        ssid=g.get('auth_token'),
        ip_address=request.remote_addr,
        title=json_data.get('title'),
        question=json_data.get('question'),
        ending_time=json_data.get('ending_time'),
        is_anonymous=json_data.get('is_anonymous'),
        emails=json_data.get('emails')
    )
    mediator = current_app.config.get('mediator')

    result = mediator.send(command)

    return jsonify(result), result["status"]

@survey_bp.route('/end_survey', methods=['PATCH', 'OPTIONS'])
@require_auth
def end_survey():
    if request.method == 'OPTIONS':
        return '', 204

    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No data provided."}), 400

    survey_id = json_data.get('survey_id')
    if not survey_id:
        return jsonify({"message": "Valid survey is required."}), 400

    command = UserEndingSurveyCommand(survey_id=str(survey_id))
    mediator = current_app.config.get("mediator")

    try:
        result = mediator.send(command)
        return jsonify(result), result["status"]
    except Exception:
        return jsonify({"message": "Stopping survey failed."}), 500

