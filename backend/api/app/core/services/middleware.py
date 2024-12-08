from functools import wraps
from flask import request, jsonify, g
from ...application.services.user_service import UserService

user_service = UserService()

def require_auth(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        auth_token = request.headers.get('Authorization')

        if not auth_token:
            return jsonify({'message': 'Not authorized!'}), 401
        
        token_parts = auth_token.split()

        if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
            return jsonify({'message': 'Not authorized!'}), 401
        
        token = token_parts[1]

        is_auth = user_service.verifySSID(token, request.remote_addr)

        if not is_auth:
            return jsonify({'message': 'Not authorized!'}), 401

        g.auth_token = token

        return f(*args, **kwargs)
    
    return check_token