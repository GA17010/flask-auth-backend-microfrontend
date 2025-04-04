from flask import Blueprint, request, jsonify
from app.models.user_model import User
from app.services import user_service
from app.database import db
from app.utils.jwt_utils import token_required

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
@token_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@token_required
def delete_user_by_id(user_id):
    user = db.session.get(User, user_id)
    return user_service.delete_user(user)
