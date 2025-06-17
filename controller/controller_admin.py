from flask import request, render_template, redirect, url_for, flash, session
from models.admin_model import Admin
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

# Registrasi admin manual
def register_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not password or not confirm_password:
            flash("Semua field wajib diisi", "danger")
            return redirect(url_for('admin_bp.register_admin_route'))

        if password != confirm_password:
            flash("Password dan konfirmasi password tidak cocok", "danger")
            return redirect(url_for('admin_bp.register_admin_route'))

        if Admin.find_by_username(username):
            flash("Username sudah digunakan", "danger")
            return redirect(url_for('admin_bp.register_admin_route'))

        Admin.insert_admin(username, password)
        flash("Registrasi berhasil, silakan login", "success")
        return redirect(url_for('admin_bp.login_admin'))

    return render_template('registeradmin.html')

# Login admin manual
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.verify_password(username, password)
        if admin:
            access_token = create_access_token(identity=str(admin['_id']))
            session['access_token'] = access_token
            session['username'] = admin['username']
            flash("Login berhasil", "success")
            return redirect(url_for('admin_bp.dashboard_admin'))

        flash("Username atau password salah", "danger")
        return redirect(url_for('admin_bp.login_admin'))

    return render_template('loginadmin.html')

# Dashboard contoh
def dashboard_admin():
    if 'access_token' not in session:
        flash("Anda harus login terlebih dahulu", "warning")
        return redirect(url_for('admin_bp.login_admin'))
    return f"Selamat datang Admin: {session.get('username')}"
