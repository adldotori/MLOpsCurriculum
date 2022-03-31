from flask import Blueprint
from .controller import Controller
from .model import User

user_bp = Blueprint("user_bp", __name__)
controller = Controller(User)

user_bp.route("", methods=["GET"])(controller.get_all_users)
user_bp.route("/<int:id>", methods=["GET"])(controller.get_user)
user_bp.route("", methods=["POST"])(controller.create_user)
user_bp.route("/<int:id>", methods=["POST"])(controller.update_user)
user_bp.route("/<int:id>", methods=["DELETE"])(controller.delete_user)
