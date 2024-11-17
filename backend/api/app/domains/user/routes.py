from flask import Blueprint, request, jsonify
#from .services import UserService
from .schemas import UserSchema

user_bp = Blueprint('user', __name__, url_prefix='/users')
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user = UserService.create_user(**data)
    return user_schema.jsonify(user), 201

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return user_schema.jsonify(user), 200

@user_bp.route('/', methods=['GET'])
def get_users():
    users = UserService.get_all_users()
    return users_schema.jsonify(users), 200