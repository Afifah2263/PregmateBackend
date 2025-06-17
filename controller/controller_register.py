import random
import datetime
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from dateutil import parser
from models.datauser_model import User
from utils.mailer import send_email

def set_db(database):
    global db
    db = database
    User.set_db(database)

def register_user():
    try:
        data = request.get_json()
        nama = data.get("nama")
        email = data.get("email")
        password = data.get("password")

        if not nama or not email or not password:
            return jsonify({"message": "Nama, email, dan password harus diisi"}), 400

        if User.find_by_email(email):
            return jsonify({"message": "Email sudah digunakan"}), 400

        hashed_password = generate_password_hash(password)
        otp = str(random.randint(100000, 999999))

        user_data = {
            "nama": nama,
            "email": email,
            "password": hashed_password,
            "otp": otp,
            "otp_verified": False,
            "otp_created_at": datetime.datetime.utcnow().isoformat()
        }

        user_id = User.insert_user(user_data)
        if not user_id:
            return jsonify({"message": "Gagal menyimpan user"}), 500

        subject = "Kode Verifikasi OTP PyhsioCare"
        body = f"Halo {nama},\n\nKode OTP Anda: {otp}\n\nKode ini berlaku 10 menit."
        send_email(email, subject, body)

        return jsonify({
            "message": "Registrasi berhasil, silakan verifikasi OTP yang dikirim ke email Anda",
            "user_id": str(user_id),
        }), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": f"Gagal registrasi: {e}"}), 500

def verify_otp():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        otp_input = data.get("otp")

        if not user_id or not otp_input:
            return jsonify({"message": "User ID dan OTP harus diisi"}), 400

        user = User.find_by_id(user_id)
        if not user:
            return jsonify({"message": "User tidak ditemukan"}), 404

        if user.get("otp_verified"):
            return jsonify({"message": "Email sudah terverifikasi"}), 400

        now = datetime.datetime.utcnow()
        otp_created = parser.isoparse(user.get("otp_created_at"))
        if (now - otp_created).total_seconds() > 600:
            return jsonify({"message": "Kode OTP sudah kedaluwarsa"}), 400

        if otp_input == user.get("otp"):
            User.update_fields(user_id, {
                "otp_verified": True,
                "otp": None,
                "otp_created_at": None
            })
            token = create_access_token(identity=str(user_id), expires_delta=datetime.timedelta(hours=1))
            return jsonify({"message": "Verifikasi berhasil", "token": token}), 200
        else:
            return jsonify({"message": "Kode OTP salah"}), 400
    except Exception as e:
        print(f"Error OTP: {e}")
        return jsonify({"message": f"Terjadi kesalahan: {e}"}), 500
