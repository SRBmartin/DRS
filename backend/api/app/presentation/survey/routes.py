from flask import Blueprint, request, jsonify, current_app, g
from marshmallow.exceptions import ValidationError

from ...application.features.survey.queries.GetSurveyAnswerDetailsQuery import GetSurveyAnswerDetailsQuery
from ...application.features.survey.commands.AnswerSurveyWebsiteCommand import AnswerSurveyWebsiteCommand
from ...application.features.survey.commands.AnswerSurveyEmailCommand import AnswerSurveyEmailLinkCommand

from ...application.features.survey.commands.DeleteEndedSurveyCommand import DeleteEndedSurveyCommand
from ...application.contracts.schemas.surveys.schemas import SurveySchema
from ...core.services.middleware import require_auth
from ...application.features.survey.commands.CreateSurveyCommand import CreateSurveyCommand
from ...application.features.survey.queries.GetSurveyDetailsQuery import GetSurveyDetailsQuery
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

@survey_bp.route('/details/<uuid:survey_id>', methods=['GET'])
@require_auth
def get_survey_details_get(survey_id):
    query = GetSurveyDetailsQuery(survey_id=str(survey_id), ssid=g.get('auth_token'), ip_address=str(request.remote_addr))
    mediator = current_app.config.get('mediator')
    
    try:
        result = mediator.send(query)
        return jsonify(result), result["status"]
    except Exception:
        return jsonify({"message": "Fetching survey details failed."}), 500

@survey_bp.route('/answer/mail/<uuid:email_id>/<uuid:survey_id>/<uuid:response_id>/<option>', methods=['POST', 'OPTIONS'])
def answer_survey_email_link(email_id, survey_id, response_id, option):
    if request.method == 'OPTIONS':
        return '', 204
    
    command = AnswerSurveyEmailLinkCommand(
        survey_id=str(survey_id),
        email_id=str(email_id),
        response_id=str(response_id),
        option=str(option)
    )
    mediator = current_app.config.get('mediator')
    result = mediator.send(command)
    return jsonify(result), result.get("status", 200)

@survey_bp.route('/answer/website', methods=['POST', 'OPTIONS'])
@require_auth
def answer_surevy_webiste():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No data provided."}), 400
    
    survey_id = json_data.get('survey_id')
    response = json_data.get('response')
    if not survey_id:
        return jsonify({"message": "Valid survey is required."}), 400
    
    if not response:
        return jsonify({"message": "Response is required."}), 400
    
    command = AnswerSurveyWebsiteCommand(
        survey_id=str(survey_id),
        response=str(response),
        ip_address=str(request.remote_addr),
        ssid=str(g.get('auth_token'))
    )
    mediator = current_app.config.get('mediator')
    result = mediator.send(command)
    return jsonify(result), result["status"]

@survey_bp.route('/details', methods=['POST', 'OPTIONS'])
def get_survey_details():
    if request.method == 'OPTIONS':
        return '', 204
    
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No data provided."}), 400
    
    survey_id = json_data.get('survey_id')
    query = GetSurveyAnswerDetailsQuery(survey_id=survey_id)
    mediator = current_app.config.get('mediator')
    
    try:
        result = mediator.send(query)
        if "data" in result:
            return jsonify({
                "message": "Survey information retrieved successfully",
                "data": result["data"],
                "status": 200
            }), 200
        else:
            return jsonify({
                "message": "Survey not found",
                "status": 404
            }), 404
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred."}), 500

@survey_bp.route('/delete', methods=['PATCH', 'OPTIONS'])
@require_auth
def delete_ended_survey():
    if request.method == 'OPTIONS':
        return '', 204
    
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No data provided."}), 400
    
    survey_id = json_data.get('survey_id')
    
    if not survey_id:
        return jsonify({"message": "Valid survey is required."}), 400
    
    command = DeleteEndedSurveyCommand(
        survey_id=str(json_data.get('survey_id'))
    )
    
    mediator = current_app.config.get("mediator")
    try:
        result = mediator.send(command)
        return jsonify(result), result["status"]
    except Exception as e:
        return jsonify({"message": "Deleting survey failed."}), 500

    
    