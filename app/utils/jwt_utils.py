import jwt
from datetime import datetime
from flask import current_app, request, jsonify
from functools import wraps

def create_access_token(identity):
    expires = datetime.now(current_app.config['TIME_ZONE']) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    payload = {
        'exp': expires,
        'type': 'access',
        'iat': datetime.now(current_app.config['TIME_ZONE']),
        'identity': identity,
        'user_agent': None # Will be established in the service
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def create_refresh_token(identity):
    expires = datetime.now(current_app.config['TIME_ZONE']) + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
    payload = {
        'exp': expires,
        'type': 'refresh',
        'iat': datetime.now(current_app.config['TIME_ZONE']),
        'identity': identity,
        'user_agent': None # Will be established in the service
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token: str, token_type: str):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        if payload.get("type") != token_type:
            return None, "Invalid token type"
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, 'Token expired'
    except jwt.InvalidTokenError:
        return None, 'Token invalid'
    
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token_cookie = request.cookies.get('accessToken')

        if not access_token_cookie:
            return {'data': {'message': 'Not authorized'}}, 401

        payload, error = verify_token(access_token_cookie, "access")

        if error:
            return jsonify({'data': {'message': error}}), 401
        if payload and payload.get('user_agent') != request.headers.get('User-Agent'):
            return jsonify({'data': {'message': 'User-Agent does not match'}}), 403

        return f(*args, **kwargs)

    return decorated
