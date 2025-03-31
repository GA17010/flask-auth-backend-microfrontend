from flask import request, jsonify
from app.database import db
from app.models.user_model import User
from app.utils.password_utils import hash_password

def find_user_by_email(email):
    return User.query.filter_by(email=email).first()

def create_new_user(user_data):
    new_user = User(
        id=user_data.get('id'),
        full_name=user_data.get('full_name'),
        company=user_data.get('company'),
        email=user_data.get('email'),
        password=hash_password(user_data.get('password'))
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user

def delete_user(user):
    if not user:
        return jsonify({"data": {"message": "Usuario no encontrado"}}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"data": {"message": "Usuario eliminado exitosamente"}}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"data": {"message": "Error Interno del Servidor"}}), 500