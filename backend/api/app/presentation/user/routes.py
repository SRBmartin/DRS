from flask import Blueprint, request, jsonify, current_app
from ...application.contracts.schemas.user.schemas import UserSchema, LoginSchema
from marshmallow import ValidationError
from ...application.features.user.commands.CreateUserCommand import CreateUserCommand
from ...application.features.user.commands.LoginUserCommand import LoginUserCommand

user_bp = Blueprint('user', __name__, url_prefix='/users')
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('/', methods=['POST'])
def create_user():
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

    if "message" in result and "status" in result:
        return jsonify(result["message"]), result["status"]

    return jsonify(result), 201

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

    if "message" in result and "status" in result:
        return jsonify(result["message"]), result["status"]
    
    return jsonify(result), 200