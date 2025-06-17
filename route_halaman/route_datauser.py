from flask import Blueprint
from controller.controller_datauser import (
    users,
    user_detail,
    user_create,
    user_delete,
    upload_profile_picture,
    update_user_profile,
    update_token
)

datauser_bp = Blueprint('datauser', __name__)

datauser_bp.add_url_rule('/user', 'user', users, methods=['GET'])
datauser_bp.add_url_rule('/user/<id>', 'user_detail', user_detail, methods=['GET'])
datauser_bp.add_url_rule('/user/create', 'user_create', user_create, methods=['POST'])
datauser_bp.add_url_rule('/user/delete/<id>', 'user_delete', user_delete, methods=['DELETE'])
datauser_bp.add_url_rule('/upload_profile_picture/<user_id>', 'upload_profile_picture', upload_profile_picture, methods=['POST'])
datauser_bp.add_url_rule('/user/<user_id>', 'update_user_profile', update_user_profile, methods=['PUT'])
datauser_bp.add_url_rule('/update_token', 'update_token', update_token, methods=['POST'])
