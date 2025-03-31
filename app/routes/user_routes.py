from flask import Blueprint, request, jsonify
from app.models.user_model import User
from app.services import user_service

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    user = User.query.get(user_id)
    return user_service.delete_user(user)
