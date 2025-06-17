from flask import Blueprint
from controller import forgot_password_controller

forgot_password_bp = Blueprint('forgot_password', __name__, url_prefix='/forgot_password')

@forgot_password_bp.route('/request_otp', methods=['POST'])
def request_otp():
    return forgot_password_controller.request_otp()

@forgot_password_bp.route('/reset', methods=['POST'])
def reset_password():
    return forgot_password_controller.reset_password()
