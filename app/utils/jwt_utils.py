import jwt
from datetime import datetime, timezone
from flask import current_app

def create_access_token(identity):
    expires = datetime.now(timezone.utc) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    payload = {
        'exp': expires,
        'type': 'access',
        'iat': datetime.now(timezone.utc),
        'identity': identity,
        'user_agent': None # Se establecerá en el servicio
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def create_refresh_token(identity):
    expires = datetime.now(timezone.utc) + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
    payload = {
        'exp': expires,
        'type': 'refresh',
        'iat': datetime.now(timezone.utc),
        'identity': identity,
        'user_agent': None # Se establecerá en el servicio
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token: str, token_type: str):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        if payload.get("type") != token_type:
            return None, "Tipo de token inválido"
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, 'Token expirado'
    except jwt.InvalidTokenError:
        return None, 'Token inválido'