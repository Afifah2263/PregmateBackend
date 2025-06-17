from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from flask_dance.contrib.google import google
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os

from models.admin_model import Admin
from controller.controller_admin import register_admin, login_admin as login_admin_controller, create_access_token
import controller.controller_keluhan as controller_keluhan

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin', template_folder='../templates')

# @admin_bp.route('/google_callback')
# def google_login_callback():
#     if not google.authorized:
#         return redirect(url_for("google.login"))
#     resp = google.get("/oauth2/v2/userinfo")
#     if not resp.ok:
#         flash("Gagal mengambil info Google", "danger")
#         return redirect(url_for('admin_bp.login_admin'))

#     info = resp.json()
#     username = info.get("email")

#     admin = Admin.find_by_username(username)
#     if not admin:
#         Admin.insert_admin(username, "randompassword1234")

#     access_token = create_access_token(identity=username)
#     session['access_token'] = access_token
#     session['username'] = username
#     flash("Login dengan Google berhasil", "success")
#     return redirect(url_for('admin_bp.dashboard_admin'))

@admin_bp.route('/register', methods=['GET', 'POST'])
def register_admin_route():
    return register_admin()

@admin_bp.route('/login', methods=['GET', 'POST'])
def login_admin():
    return login_admin_controller()

@admin_bp.route('/admin/dashboard')
def dashboard_admin():
    return controller_keluhan.index_keluhan()

@admin_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    if not username:
        flash("Anda harus login terlebih dahulu", "danger")
        return redirect(url_for('admin_bp.login_admin'))

    admin = Admin.find_by_username(username)
    if not admin:
        flash("Admin tidak ditemukan", "danger")
        return redirect(url_for('admin_bp.login_admin'))

    if request.method == 'POST':
        new_email = request.form.get('email')
        new_name = request.form.get('name')
        new_phone = request.form.get('phone')
        new_address = request.form.get('address')
        new_password = request.form.get('password')

        update_data = {
            'username': username,
            'email': new_email,
            'name': new_name,
            'phone': new_phone,
            'address': new_address,
        }

        if new_password:
            update_data['password'] = generate_password_hash(new_password)

        file = request.files.get('photo')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            file.save(upload_path)
            update_data['photo'] = filename

        Admin.update_admin(update_data)
        flash("Profil berhasil diperbarui", "success")
        return redirect(url_for('admin_bp.profile'))

    return render_template('profiladmin.html', admin=admin)

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash("Berhasil logout", "success")
    return redirect(url_for('admin_bp.login_admin'))
