from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId

jadwal_bp = Blueprint('jadwal', __name__)
db = None

def set_db(database):
    global db
    db = database

@jadwal_bp.route('/jadwal', methods=['POST'])
def buat_jadwal():
    try:
        data = request.get_json()

        required_fields = ("user_id", "tanggal", "jam", "pesan", "fcmToken")
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Data tidak lengkap"}), 400

        user_id = data["user_id"]
        fcm_token = data["fcmToken"]

        # ❗ Error terjadi di sini jika db = None
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"token": fcm_token}}
        )

        jadwal_data = {
            "user_id": user_id,
            "tanggal": data["tanggal"],
            "jam": data["jam"],
            "pesan": data["pesan"],
            "dikirim": data.get("dikirim", False)
        }

        db.schedules.insert_one(jadwal_data)

        return jsonify({"message": "Jadwal berhasil disimpan"}), 201

    except Exception as e:
        print(f"❌ Error memproses jadwal: {e}")
        return jsonify({"error": str(e)}), 500
