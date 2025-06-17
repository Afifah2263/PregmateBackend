from flask import request, jsonify, url_for
from flask_jwt_extended import jwt_required
from models.datauser_model import User
from models.userlog_model import UserLog
from werkzeug.utils import secure_filename
from datetime import datetime
from bson import ObjectId
import os
import hashlib

UPLOAD_FOLDER = os.path.join('static', 'images', 'Profile')
UPLOAD_URL_PATH = 'static/images/Profile'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def set_db(database):
    global db
    db = database

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@jwt_required()
def users():
    all_users = User.find_all()
    for user in all_users:
        user["_id"] = str(user["_id"])
    return jsonify(all_users), 200

@jwt_required()
def user_detail(id):
    user = User.find_by_id(id)
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404

@jwt_required()
def user_create():
    data = request.get_json()
    nama = data.get("nama")
    email = data.get("email")
    password = data.get("password")
    foto = data.get("foto")

    if not nama or not email or not password:
        return jsonify({"message": "Data tidak lengkap"}), 400

    user_id = User.create(nama, email, password, foto)
    return jsonify({"message": "User created", "user_id": str(user_id)}), 201

@jwt_required()
def user_delete(id):
    user = User.find_by_id(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    User.delete_user(id)
    return jsonify({"message": "User deleted"}), 200

@jwt_required()
def update_user_profile(user_id):
    data = request.get_json()
    nama = data.get("nama")
    email = data.get("email")
    password = data.get("password")

    user = User.find_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    updated_nama = nama if nama else user['nama']
    updated_email = email if email else user['email']
    updated_password = hashlib.sha256(password.encode()).hexdigest() if password else user['password']
    updated_foto = user.get('foto', None)

    foto_diganti = False
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(filepath)
            updated_foto = f"{UPLOAD_URL_PATH}/{filename}"
            foto_diganti = True

    updated_user = User.update(user_id, updated_nama, updated_email, updated_password, updated_foto)
    if not updated_user:
        return jsonify({"message": "Update failed"}), 500

    logger = UserLog(db)
    changes = []
    if nama and nama != user['nama']:
        changes.append("nama")
    if email and email != user['email']:
        changes.append("email")
    if password:
        changes.append("password")
    if foto_diganti:
        changes.append("foto")

    action_detail = ", ".join(changes) if changes else "tidak ada perubahan"
    logger.log_activity(user_id, action="update_profile", status="success", keterangan=f"Update: {action_detail}")

    user_updated = User.find_by_id(user_id)
    user_updated["_id"] = str(user_updated["_id"])
    return jsonify(user_updated), 200

@jwt_required()
def upload_profile_picture(user_id):
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        updated_user = User.update_profile_picture(user_id, filename)
        if not updated_user:
            return jsonify({"message": "Failed to update user profile picture"}), 500

        return jsonify({"message": "Profile picture updated", "filename": filename}), 200

    return jsonify({'message': 'File type not allowed'}), 400

def update_token():
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')

    if not user_id or not token:
        return jsonify({'message': 'User ID atau token kosong'}), 400

    try:
        from app import db
        users_collection = db['users']
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'message': 'User tidak ditemukan'}), 404

        users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'tokenFCM': token}})
        return jsonify({'message': 'Token berhasil diperbarui'}), 200
    except Exception as e:
        return jsonify({'message': f'Gagal memperbarui token: {str(e)}'}), 500
