from flask import request, make_response, jsonify
from marshmallow import ValidationError
from app.schemas.user_schema import ForgotPasswordSchema, ResetPasswordSchema
from app.utils.otp_utils import verify_otp, generate_otp, save_otp_to_db
from app.utils.email_utils import send_email
from app.utils.password_utils import hash_password
from app.services.user_service import find_user_by_email, update_password_user

def forgot_password(data):
    try:
        forgot_password_schema = ForgotPasswordSchema()
        validated_data =forgot_password_schema.load(data)
    except ValidationError as err:
        return {'data': {'message': "Invalid Data"}}, 400
    
    email = validated_data.get('email')
    user = find_user_by_email(email)
    if not user:
        return {'data': {'message': 'The user already exists'}}, 409
    
    otp = generate_otp()
    
    result = save_otp_to_db(email, otp)

    if not result:
        return jsonify({'data': {'message': 'Error saving Code, please try again later' }}), 500

    try:
        send_email(user.full_name, otp, email)
    except Exception as e:
        return jsonify({'data': {'message': 'Error sending email, please try again later' }}), 500

    response = jsonify({'data': {'message': 'Recovery mail sent' }})
    return response, 200

def verify_otp_service(data):
    email = data.get('email')
    otp = data.get('otp')

    if verify_otp(email, otp, False):
        return jsonify({'data': {'message': 'Valid code, proceed to change the password'}}), 200
    return jsonify({'data': {'message': 'Incorrect or expired code'}}), 400

def reset_password(data):
    try:
        reset_password_schema = ResetPasswordSchema()
        validated_data = reset_password_schema.load(data)
    except ValidationError as err:
        return {'data': {'message': 'Invalid Data'}}, 400
    
    otp = validated_data.get('otp')
    email = validated_data.get('email')
    new_password = validated_data.get('password')

    user = find_user_by_email(email)

    if verify_otp(email, otp, True) and user:
        user.password = hash_password(new_password)
        update_password_user(user)

        return jsonify({'data': {'message': 'Password updated correctly'}}), 200
    
    return jsonify({'data': {'message': 'Invalid or expired code'}}), 400
