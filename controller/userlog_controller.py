from flask import jsonify, render_template
from models.userlog_model import UserLog
from bson import ObjectId
from flask import redirect, url_for
userlog_model = None
db = None  # simpan juga db di sini

def set_db(database):
    global userlog_model, db
    db = database
    userlog_model = UserLog(database)

def get_all_user_logs():
    logs = userlog_model.get_all_logs()
    
    # Ambil nama user dari koleksi users berdasarkan user_id
    for log in logs:
        user_id = log.get("user_id")
        if user_id:
            user = db["users"].find_one({"_id": ObjectId(user_id)})
            log["user_name"] = f"{user.get('nama')} {user.get('nama_belakang', '')}" if user else "Tidak Diketahui"
        else:
            log["user_name"] = "Tidak Diketahui"
    
    return render_template("histori_user.html", logs=logs)


def delete_log_by_id(log_id):
    try:
        userlog_model.collection.delete_one({"_id": ObjectId(log_id)})
    except Exception as e:
        print(f"Error deleting log: {e}")
    return redirect(url_for("histori_user_bp.histori_user_page"))