from flask import Blueprint, request
from app.services import auth_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return auth_service.register_user(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return auth_service.login_user(data)

@auth_bp.route('/checkAuth', methods=['GET'])
def check_auth():
    return auth_service.check_auth()

@auth_bp.route('/refreshToken', methods=['POST'])
def refresh_token():
    return auth_service.refresh_token()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return auth_service.logout_user()