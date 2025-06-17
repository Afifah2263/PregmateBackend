# @admin_bp.route('/admin/register', methods=['POST'])
# def register_admin():
#     username = request.form.get('username')
#     password = request.form.get('password')
#     # Lanjutkan proses validasi dan simpan ke database

import jwt
from datetime import datetime, timedelta

SECRET_KEY = "rahasiaJWT"

def generate_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
