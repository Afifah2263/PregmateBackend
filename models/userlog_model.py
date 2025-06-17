from bson import ObjectId
from datetime import datetime

class UserLog:
    def __init__(self, db):
        self.collection = db["user_logs"]

    def log_activity(self, user_id, action, status="success", keterangan=None):
        log_entry = {
            "user_id": ObjectId(user_id),
            "action": action,  # e.g., "login", "ganti password"
            "status": status,  # "success" / "failed"
            "keterangan": keterangan,
            "timestamp": datetime.utcnow()
        }
        self.collection.insert_one(log_entry)

    def get_all_logs(self):
        return list(self.collection.find({}).sort("timestamp", -1))
