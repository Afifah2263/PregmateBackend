from flask import Blueprint
from controller import controller_login

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    return controller_login.login_user()

@login_bp.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    return controller_login.get_user_by_id(user_id)

@login_bp.route("/user/<user_id>", methods=["PUT"])
def update_user(user_id):
    return controller_login.update_user_profile(user_id)


@login_bp.route("/google", methods=["POST"])
def login_google():
    return controller_login.login_google()