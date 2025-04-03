from flask import request, make_response, jsonify
from app.schemas.user_schema import RegistrationSchema, LoginSchema
from marshmallow import ValidationError
from app.utils.jwt_utils import create_access_token, create_refresh_token, verify_token
from app.utils.password_utils import check_password
from app.services.user_service import find_user_by_email, create_new_user

def register_user(data):
    try:
        registration_schema = RegistrationSchema()
        validated_data =registration_schema.load(data)
    except ValidationError as err:
        return {'data': {'message': "Datos invalidos"}}, 400
    
    if find_user_by_email(validated_data.get('email')):
        return {'data': {'message': 'El usuario ya existe'}}, 409

    new_user = create_new_user(validated_data)

    access_token = create_access_token(identity=new_user.email)
    refresh_token = create_refresh_token(identity=new_user.email)

    access_token_payload = jwt.decode(access_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    refresh_token_payload = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    
    access_token_payload['user_agent'] = request.headers.get('User-Agent')
    refresh_token_payload['user_agent'] = request.headers.get('User-Agent')

    encoded_access_token = jwt.encode(access_token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    encoded_refresh_token = jwt.encode(refresh_token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    response = jsonify({'data': {'message': 'Registrado exitosamente', 'user': {'id': new_user.id, 'full_name': new_user.full_name, 'email': new_user.email}}})
    set_auth_cookies(response, encoded_access_token, encoded_refresh_token)
    return response, 201

def login_user(data):
    try:
        login_schema = LoginSchema()
        validated_data = login_schema.load(data)
    except ValidationError as err:
        return {'data': {'message': "Datos invalidos"}}, 400

    user = find_user_by_email(validated_data.get('email'))
    
    if not user or not check_password(user.password, validated_data.get('password')):
        return {'data': {'message': 'Credenciales incorrectas'}}, 401
    
    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    access_token_payload = jwt.decode(access_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    refresh_token_payload = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    access_token_payload['user_agent'] = request.headers.get('User-Agent')
    refresh_token_payload['user_agent'] = request.headers.get('User-Agent')

    encoded_access_token = jwt.encode(access_token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    encoded_refresh_token = jwt.encode(refresh_token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    response = jsonify({'data': {'message': 'Autenticado exitosamente', 'user': {'id': user.id, 'full_name': user.full_name, 'email': user.email}}})
    set_auth_cookies(response, encoded_access_token, encoded_refresh_token)
    return response, 200

def check_auth():
    access_token_cookie = request.cookies.get('accessToken')
    if not access_token_cookie:
        return {'data': {'message': 'No autorizado'}}, 401
    
    payload, error = verify_token(access_token_cookie, 'access')
    if error:
        return {'data': {'message': error}}, 401
    if payload and payload.get('user_agent') != request.headers.get('User-Agent'):
        return {'data': {'message': 'User-Agent no coincide'}}, 403
    
    user = find_user_by_email(payload['identity'])

    if not user:
        return {'data': {'message': 'No autorizado'}}, 401
    
    return {'data': {'message': 'Token valido', 'user': {'id': user.id, 'full_name': user.full_name, 'email': user.email}}}, 200

def refresh_token():
    refresh_token_cookie = request.cookies.get('refreshToken')

    if not refresh_token_cookie:
        return {'data': {'message': 'No se proporcionó un token de refresco'}}, 401
    
    payload, error = verify_token(refresh_token_cookie, 'refresh')
    if error:
        return {'data': {'message': error}}, 401
    if payload and payload.get('user_agent') != request.headers.get('User-Agent'):
        return {'data': {'message': 'User-Agent no coincide'}}, 403

    new_access_token = create_access_token(identity=payload['identity'])

    new_access_token_payload = jwt.decode(new_access_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    new_access_token_payload['user_agent'] = request.headers.get('User-Agent')

    encoded_new_access_token = jwt.encode(new_access_token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    response = jsonify({'data': {'message': 'Token renovado exitosamente'}})

    # set_auth_cookies(response, encoded_new_access_token)
    response.set_cookie('accessToken', encoded_new_access_token, httponly=True, secure=True, samesite='None')
    return response, 200

def logout_user():
    response = jsonify({'data': {'message': 'Seccion Cerrada'}})
    response.delete_cookie('accessToken', httponly=True, secure=True, samesite='None')
    response.delete_cookie('refreshToken', httponly=True, secure=True, samesite='None')
    return response, 200

def set_auth_cookies(response, access_token, refresh_token):
    response.set_cookie('accessToken', access_token, httponly=True, secure=True, samesite='None')
    response.set_cookie('refreshToken', refresh_token, httponly=True, secure=True, samesite='None')

from .. import bcrypt
from app.models.user_model import User
from flask import current_app
import jwt