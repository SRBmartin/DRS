from flask import Blueprint, request, jsonify, current_app
from ...application.contracts.schemas.user.schemas import UserSchema, LoginSchema
from marshmallow import ValidationError
from ...application.features.user.commands.CreateUserCommand import CreateUserCommand
from ...application.features.user.commands.LoginUserCommand import LoginUserCommand
from ...application.features.user.commands.VerifySSIDCommand import VerifySSIDCommand
from ...application.features.user.queries.GetGeneralInfoQuery import GetGeneralInfoQuery
from ...application.features.user.commands.ChangePasswordCommand import ChangePasswordCommand
from ...application.features.user.commands.UpdateGeneralInfoCommand import UpdateGeneralInformationCommand

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
    
@user_bp.route('/profile-page/general-information', methods=['POST'])
def get_general_info():
    
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Authorization header is missing or invalid", "status": 401}), 401
    
    ssid = auth_header.split(" ")[1]
    ip_address = request.remote_addr

    query = GetGeneralInfoQuery(ssid=ssid, ip_address=ip_address)
    mediator = current_app.config.get('mediator')

    try:
        result = mediator.send(query)
        if "user" in result:
            return jsonify({
                "message": "User information retrieved successfully",
                "data": result["user"],
                "status": 200
            }), 200
        else:
            return jsonify({
                "message": "Userrr not found",
                "status": 404
            }), 404
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred.", "status": 500}), 500
    
@user_bp.route('/profile-page/change-password', methods=['POST'])
def change_password():
    json_data = request.get_json()

    if not json_data:
        return jsonify({"message": "No data provided.", "status": 400}), 400

    required_fields = ["old_password", "new_password"]
    missing_fields = [field for field in required_fields if field not in json_data]
    if missing_fields:
        return jsonify({
            "message": f"Missing required fields: {', '.join(missing_fields)}",
            "status": 400
        }), 400

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({
            "message": "Authorization header is missing or invalid.",
            "status": 401
        }), 401

    ssid = auth_header.split(" ")[1]

    command = ChangePasswordCommand(
        ssid=ssid,
        ip_address=request.remote_addr,
        old_password=json_data.get('old_password'),
        new_password=json_data.get('new_password')
    )

    mediator = current_app.config.get('mediator')
    try:
        result = mediator.send(command)
        return jsonify(result), result["status"]
    except Exception as e:
        current_app.logger.error(f"Error changing password: {str(e)}")
        return jsonify({
            "message": "An unexpected error occurred.",
            "status": 500
        }), 500
            
@user_bp.route('/profile-page/save-general-information', methods=['POST'])
def save_general_info():
    json_data = request.get_json()

    if not json_data:
        return jsonify({"message": "No data provided.", "status": 400}), 400

    required_fields = ["name", "lastname", "email", "phone_number", "address", "city", "country"]
    missing_fields = [field for field in required_fields if field not in json_data]
    if missing_fields:
        return jsonify({
            "message": f"Missing required fields: {', '.join(missing_fields)}",
            "status": 400
        }), 400

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({
            "message": "Authorization header is missing or invalid.",
            "status": 401
        }), 401

    ssid = auth_header.split(" ")[1]

    command = UpdateGeneralInformationCommand(
        ssid=ssid,
        ip_address=request.remote_addr,
        name=json_data.get('name'),
        lastname=json_data.get('lastname'),
        email=json_data.get('email'),
        phone_number=json_data.get('phone_number'),
        address=json_data.get('address'),
        city=json_data.get('city'),
        country=json_data.get('country')
    )

    mediator = current_app.config.get('mediator')
    try:
        result = mediator.send(command)
        return jsonify(result), result["status"]
    except Exception as e:
        current_app.logger.error(f"Error updating user information: {str(e)}")
        return jsonify({
            "message": "An unexpected error occurred.",
            "status": 500
        }), 500

