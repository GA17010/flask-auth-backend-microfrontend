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
        return {'data': {'message': "Datos invalidos"}}, 400
    
    email = validated_data.get('email')
    user = find_user_by_email(email)
    if not user:
        return {'data': {'message': 'El usuario no existe'}}, 409
    
    otp = generate_otp()
    
    result = save_otp_to_db(email, otp)

    if not result:
        return jsonify({'data': {'message': 'Error de conexion!' }}), 500

    try:
        send_email(user.full_name, otp, email)
    except Exception as e:
        return jsonify({'data': {'message': 'Error al enviar correo!' }}), 500

    response = jsonify({'data': {'message': 'Correo de recuperación enviado' }})
    return response, 200

def verify_otp_service(data):
    email = data.get('email')
    otp = data.get('otp')

    if verify_otp(email, otp, False):
        return jsonify({'data': {'message': 'OTP válido, procede a cambiar la contraseña'}}), 200
    return jsonify({'data': {'message': 'OTP incorrecto o expirado'}}), 400

def reset_password(data):
    try:
        reset_password_schema = ResetPasswordSchema()
        validated_data = reset_password_schema.load(data)
    except ValidationError as err:
        return {'data': {'message': 'Datos invalidos'}}
    
    otp = validated_data.get('otp')
    email = validated_data.get('email')
    new_password = validated_data.get('password')

    user = find_user_by_email(email)

    if verify_otp(email, otp, True) and user:
        user.password = hash_password(new_password)
        update_password_user(user)

        return jsonify({'data': {'message': 'Contraseña actualizada correctamente'}}), 200
    
    return jsonify({'data': {'message': 'Codigo inválido o expirado'}}), 400
