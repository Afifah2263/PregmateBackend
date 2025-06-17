from flask import Blueprint, redirect, url_for, request
from controller.userlog_controller import get_all_user_logs, delete_log_by_id

histori_user_bp = Blueprint("histori_user_bp", __name__)

@histori_user_bp.route("/admin/histori_user")
def histori_user_page():
    return get_all_user_logs()

@histori_user_bp.route("/admin/histori_user/delete/<log_id>", methods=["POST"])
def delete_log(log_id):
    return delete_log_by_id(log_id)
