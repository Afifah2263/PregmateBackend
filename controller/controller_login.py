from flask import request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required

from models.datauser_model import User
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
#import requests  # pastikan ini dari pip install requests
from google.auth.transport import requests as google_requests
from utils.jwt_utils import generate_token
from models.userlog_model import UserLog

# GOOGLE_CLIENT_ID_USER = '945236677336-pl4ua4gp1p388u0131uouanod6av77gp.apps.googleusercontent.com'
GOOGLE_CLIENT_ID = '945236677336-pl4ua4gp1p388u0131uouanod6av77gp.apps.googleusercontent.com'

def set_db(database):
    global db
    db = database
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    user = User.find_by_email(email)
   
    if not user:
        UserLog(db).log_activity(None, "login", status="failed", keterangan=f"Email tidak terdaftar: {email}")
        return jsonify({"message": "Email tidak terdaftar"}), 401

    if not check_password_hash(user["password"], password):
        UserLog(db).log_activity(user["_id"], "login", status="failed", keterangan=f"Password salah untuk user {user['email']}")
        return jsonify({"message": "Password salah"}), 401
    
    if not user.get("otp_verified", False):
        UserLog(db).log_activity(None, "login", status="failed", keterangan="Akun belum diverifikasi melalui OTP")
        return jsonify({"message": "Akun belum diverifikasi melalui OTP"}), 403


    token = create_access_token(identity=str(user["_id"]), expires_delta=timedelta(hours=1))
    UserLog(db).log_activity(user["_id"], "login", status="success",keterangan="Login manual berhasil")
    return jsonify({
        "message": "Login berhasil",
        "token": token,
        "user": {
            "_id": str(user["_id"]),
            "nama": user["nama"],
            "email": user["email"]
        }
    }), 200


# def login_google():
#     try:
#         data = request.get_json()
#         token = data.get('id_token')  # bisa jadi access_token

#         if not token:
#             return jsonify({"message": "Token Google diperlukan"}), 400

#         # Coba verifikasi sebagai access token
#         userinfo_url = f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={token}'
#         userinfo_response = requests.get(userinfo_url)

#         if userinfo_response.status_code != 200:
#             return jsonify({"message": "Access token Google tidak valid"}), 401

#         userinfo = userinfo_response.json()

#         email = userinfo.get('email')
#         name = userinfo.get('name')
#         picture = userinfo.get('picture')

#         if not email:
#             return jsonify({"message": "Email tidak ditemukan di data user"}), 400

#         # Cari user di database
#         user = db.db.users.find_one({"email": email})
#         if not user:
#             new_user = {
#                 "nama": name,
#                 "email": email,
#                 "picture": picture,
#                 "confirmed": True,
#                 "created_at": datetime.utcnow()
#             }
#             inserted = db.db.users.insert_one(new_user)
#             user = db.db.users.find_one({"_id": inserted.inserted_id})

#         access_token = create_access_token(identity=str(user['_id']), expires_delta=timedelta(days=1))

#         return jsonify({
#             "message": "Login Google berhasil",
#             "user": {
#                 "_id": str(user["_id"]),
#                 "nama": user["nama"],
#                 "email": user["email"],
#                 "picture": user.get("picture")
#             },
#             "token": access_token
#         }), 200

#     except Exception as e:
#         print(f"Error internal: {e}")
#         return jsonify({"message": "Terjadi kesalahan internal"}), 500
# def login_google():
#     try:
#         data = request.get_json()
#         id_token_str = data.get('idToken') or data.get('id_token')

#         if not id_token_str:
#             return jsonify({"message": "Token Google diperlukan"}), 400

#         # Verifikasi id_token Google
#         try:
#             # Ganti CLIENT_ID dengan OAuth 2.0 client ID dari Google Cloud Console kamu
#             CLIENT_ID = "945236677336-pl4ua4gp1p388u0131uouanod6av77gp.apps.googleusercontent.com"
#             idinfo = id_token.verify_oauth2_token(id_token_str, google_requests.Request(), CLIENT_ID)

#             # Pastikan token valid dan dari audience yang sesuai
#             if idinfo['aud'] != CLIENT_ID:
#                 return jsonify({"message": "Token Google tidak valid"}), 401

#             email = idinfo.get('email')
#             name = idinfo.get('name')
#             picture = idinfo.get('picture')

#             if not email:
#                 return jsonify({"message": "Email tidak ditemukan di data user"}), 400

#             # Cari user di DB berdasarkan email
#             user = User.find_by_email(email)
#             if not user:
#                 new_user = {
#                     "nama": name,
#                     "email": email,
#                     "picture": picture,
#                     "confirmed": True,
#                     "created_at": datetime.utcnow()
#                 }
#                 user_id = User.insert_user(new_user)
#                 user = User.find_by_id(user_id)

#             # Generate JWT untuk app kamu
#             access_token = generate_token(user["_id"])

#             return jsonify({
#                 "message": "Login Google berhasil",
#                 "user": {
#                     "_id": str(user["_id"]),
#                     "nama": user["nama"],
#                     "email": user["email"],
#                     "picture": user.get("picture")
#                 },
#                 "token": access_token
#             }), 200

#         except ValueError:
#             # Token tidak valid
#             return jsonify({"message": "Token Google tidak valid"}), 401

#     except Exception as e:
#         print(f"Error internal: {e}")
#         return jsonify({"message": "Terjadi kesalahan internal"}), 500
def login_google():
    data = request.get_json()
    token = data.get('idToken')  # Bisa juga 'id_token'

    if not token:
        UserLog(db).log_activity(None, "login", status="failed", keterangan="Token Google tidak ditemukan")
        return jsonify({"message": "Token Google diperlukan"}), 400

    try:
        # Verifikasi idToken Google
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), GOOGLE_CLIENT_ID)

        email = idinfo.get('email')
        name = idinfo.get('name')
        picture = idinfo.get('picture')

        if not email:
            UserLog(db).log_activity(None, "login", status="failed", keterangan="Email tidak ditemukan di token Google")
            return jsonify({"message": "Email tidak ditemukan di token Google"}), 400

        # Cek apakah user sudah ada di DB
        user = User.find_by_email(email)

        if not user:
            new_user = {
                "nama": name or "Pengguna Baru",
                "email": email,
                "foto": picture or "",
                "password": None,
                "confirmed": True,
                "created_at": datetime.utcnow()
            }
            inserted_id = User.insert_user(new_user)
            user = User.find_by_id(inserted_id)
            UserLog(db).log_activity(inserted_id, "register", status="success", keterangan="Register via Google")

        # Buat JWT token
        access_token = create_access_token(identity=str(user["_id"]), expires_delta=timedelta(hours=1))

        # Simpan histori login
        UserLog(db).log_activity(user["_id"], "login", status="success", keterangan="Login via Google")

        # Kirim response
        return jsonify({
            "message": "Login Google berhasil",
            "token": access_token,
            "user": {
                "_id": str(user["_id"]),
                "nama": user.get("nama", ""),
                "email": user["email"],
                "foto": user.get("foto", "")
            }
        }), 200

    except ValueError:
        UserLog(db).log_activity(None, "login", status="failed", keterangan="Token Google tidak valid")
        return jsonify({"message": "Token Google tidak valid"}), 401

    except Exception as e:
        print(f"[LOGIN GOOGLE ERROR] {e}")
        UserLog(db).log_activity(None, "login", status="failed", keterangan="Kesalahan internal saat login Google")
        return jsonify({"message": "Terjadi kesalahan internal"}), 500
