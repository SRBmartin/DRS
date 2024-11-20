from flask import Blueprint, request, jsonify
#from .services import UserService
from ...domains.user.schemas import UserSchema

user_bp = Blueprint('user', __name__, url_prefix='/users')
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('/', methods=['POST'])
def create_user():
    pass

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    pass

@user_bp.route('/', methods=['GET'])
def get_users():
    pass