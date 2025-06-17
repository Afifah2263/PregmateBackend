from flask import Blueprint
from controller import controller_register

register_bp = Blueprint('register_bp', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    return controller_register.register_user()

@register_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    return controller_register.verify_otp()
