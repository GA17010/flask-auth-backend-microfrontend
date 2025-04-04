from flask import Blueprint, request
from app.services import recovery_service

recovery_bp = Blueprint('recovery', __name__)

@recovery_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    return recovery_service.forgot_password(data)

@recovery_bp.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.get_json()
    return recovery_service.verify_otp_service(data)

@recovery_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    return recovery_service.reset_password(data)
