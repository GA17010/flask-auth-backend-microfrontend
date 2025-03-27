import jwt
from datetime import datetime, timezone
from flask import current_app

def create_access_token(identity):
    expires = datetime.now(timezone.utc) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    payload = {
        'exp': expires,
        'iat': datetime.now(timezone.utc),
        'identity': identity,
        'user_agent': None # Se establecerá en el servicio
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def create_refresh_token(identity):
    expires = datetime.now(timezone.utc) + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
    payload = {
        'exp': expires,
        'iat': datetime.now(timezone.utc),
        'identity': identity,
        'user_agent': None # Se establecerá en el servicio
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token, token_type='access'):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, 'Token expirado'
    except jwt.InvalidTokenError:
        return None, 'Token inválido'