from flask import Blueprint
from .controller import (
    get_all_users,
    get_user,
    create_user,
    update_user,
    delete_user,
)

user_bp = Blueprint("user_bp", __name__)
user_bp.route("", methods=["GET"])(get_all_users)
user_bp.route("/<int:id>", methods=["GET"])(get_user)
user_bp.route("", methods=["POST"])(create_user)
user_bp.route("/<int:id>", methods=["POST"])(update_user)
user_bp.route("/<int:id>", methods=["DELETE"])(delete_user)
