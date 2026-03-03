from flask import Blueprint, request, jsonify
from app.services.services import AuthService
from app.schemas.schemas import UserSchema

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields: name, email, password'}), 400
        
    user, error = AuthService.register(data.get('name'), data.get('email'), data.get('password'))
    if error:
        return jsonify({'message': error}), 400
    return jsonify({'message': 'User registered successfully!'}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    result, error = AuthService.login(data.get('email'), data.get('password'))
    if error:
        return jsonify({'message': error}), 401
    return jsonify(token=result['token']), 200
