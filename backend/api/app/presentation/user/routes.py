from flask import Blueprint, request, jsonify, current_app, g
from ...application.contracts.schemas.user.schemas import UserSchema, LoginSchema
from marshmallow import ValidationError
from ...application.features.user.commands.CreateUserCommand import CreateUserCommand
from ...application.features.user.commands.LoginUserCommand import LoginUserCommand
from ...application.features.user.commands.VerifySSIDCommand import VerifySSIDCommand
from ...application.features.user.commands.LogoutUserCommand import LogoutUserCommand
from ...application.features.user.commands.DeleteUserAccountCommand import DeleteUserCommand
from ...domains.user.repositories import SessionRepository
import uuid
from ...application.features.user.queries.GetGeneralInfoQuery import GetGeneralInfoQuery
from ...application.features.user.commands.ChangePasswordCommand import ChangePasswordCommand
from ...application.features.user.commands.UpdateGeneralInfoCommand import UpdateGeneralInformationCommand
from ...core.services.middleware import require_auth

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
    
@user_bp.route('/logout', methods=['POST'])
@require_auth
def logout_user():
    json_data = request.get_json()

    ssid = g.get("auth_token")
    ip_address = request.remote_addr

    command = LogoutUserCommand(
        ssid=ssid,
        ip_address=ip_address
    )

    mediator = current_app.config.get('mediator')
    try:
            result = mediator.send(command)
            return jsonify(result), result["status"]
    except Exception as e:
            return jsonify({"message": "There was an error during logout.", "error": str(e)}), 500
        
@user_bp.route('/general-information', methods=['GET'])
@require_auth
def get_general_info():
    ssid = g.get('auth_token')
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
                "message": "User not found",
                "status": 404
            }), 404
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred."}), 500
    
@user_bp.route('/change-password', methods=['PATCH'])
@require_auth
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

    ssid = g.get('auth_token')

    command = ChangePasswordCommand(
        ssid=ssid,
        ip_address=request.remote_addr,
        data=json_data
    )

    mediator = current_app.config.get('mediator')
    try:
        result = mediator.send(command)
        return jsonify(result), result["status"]
    except Exception as e:
        return jsonify({"message": "There was an error during logout."}), 500
    
@user_bp.route('/delete-account', methods=['POST'])
@require_auth
def delete_account():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No data provided."}), 400
    
    password = json_data.get('password')
    ssid = g.get("auth_token")
    
    if not password:
        return jsonify({"message": "Password is required."}), 400

    try:
        ses_id = uuid.UUID(ssid)
        session = SessionRepository.get_active_by_id(ses_id, request.remote_addr)
        if not session:
            return jsonify({"message": "Session not found"}), 404

        user_id = session.user_id  


        command = DeleteUserCommand(
            user_id=user_id,
            password=password
        )

        mediator = current_app.config.get('mediator')
        result = mediator.send(command)
        return jsonify(result), result["status"]
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as ex:
        return jsonify({"message": "An unexpected error occurred", "error": str(ex)}), 500
        
            
@user_bp.route('/save-general-information', methods=['PUT'])
@require_auth
def save_general_info():
    json_data = request.get_json()

    if not json_data:
        return jsonify({"message": "No data provided.", "status": 400}), 400
    
    ssid = g.get('auth_token')

    command = UpdateGeneralInformationCommand(
        ssid=ssid,
        ip_address=request.remote_addr,
        data=json_data  
    )

    mediator = current_app.config.get('mediator')
    try:
        result = mediator.send(command)
        return jsonify(result), result["status"]
    except Exception as e:
        current_app.logger.error(f"Error updating user information: {str(e)}")
        return jsonify({
            "message": "An unexpected error occurred."
        }), 500

