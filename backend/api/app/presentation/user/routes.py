from flask import Blueprint, request, jsonify, current_app
from ...application.contracts.schemas.user.schemas import UserSchema, LoginSchema
from marshmallow import ValidationError
from ...application.features.user.commands.CreateUserCommand import CreateUserCommand
from ...application.features.user.commands.LoginUserCommand import LoginUserCommand
from ...application.features.user.commands.VerifySSIDCommand import VerifySSIDCommand
from ...application.features.user.queries.GetGeneralInfoQuery import GetGeneralInfoQuery

user_bp = Blueprint('user', __name__, url_prefix='/users')
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('', methods=['POST', 'OPTIONS'])
def create_user():
    if request.method == 'OPTIONS':
        return '', 204

    json_data = request.get_json()
    if not json_data:
        return jsonify({"message":"No data provided."}), 400
    
    from app.application.contracts.schemas.user.schemas import UserSchema
    user_schema = UserSchema()
    try:
        user_data = user_schema.load(json_data)
    except ValidationError:
        return jsonify({"message": "Check the fields and try again"}), 422
    
    command = CreateUserCommand(
        name=json_data.get('name'),
        lastname=json_data.get('lastname'),
        address=json_data.get('address'),
        city=json_data.get('city'),
        country=json_data.get('country'),
        phone_number=json_data.get('phone_number'),
        email=json_data.get('email'),
        password=json_data.get('password'),
        ip_address=request.remote_addr
    )
    mediator = current_app.config.get('mediator')

    result = mediator.send(command)

    return jsonify(result), result["status"]

@user_bp.route('/login', methods=['POST'])
def login_user():
    json_data = request.get_json()
    login_schema = LoginSchema()
    try:
        req = login_schema.load(json_data)
        if not json_data:
            return jsonify({"message":"No data provided."}), 400
    except ValidationError as err:
        return jsonify({"message": err.messages}), 422
    
    command = LoginUserCommand(
        email=json_data.get('email'),
        password=json_data.get('password'),
        ip_address=request.remote_addr
    )

    mediator = current_app.config.get('mediator')

    result = mediator.send(command)
    
    return jsonify(result), result["status"]

@user_bp.route('/verify', methods=['POST'])
def verify_ssid():
    json_data = request.get_json()
    if not json_data:
        return jsonify({}), 400
    
    try:
        command = VerifySSIDCommand(
            ssid=json_data.get('ssid'),
            ip_address=request.remote_addr
        )

        mediator = current_app.config.get('mediator')
        result = mediator.send(command)
        if(result):
            http_status = 200
        else:
            http_status = 401
        
        return jsonify({}), http_status
    except Exception:
        return jsonify({}), 500
    
@user_bp.route('/profile-page/general-information', methods=['GET'])
def get_general_info():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"message": "User ID is required."}), 400
    
    try:
        query = GetGeneralInfoQuery(user_id=user_id)
        mediator = current_app.config.get('mediator')
        result = mediator.send(query)
        return jsonify(result), result["status"]
    except Exception as e:
        return jsonify({"message":"An unexpected error occurred."}), 500