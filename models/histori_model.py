from bson import ObjectId
from datetime import datetime, timedelta

class HistoriModel:
    def __init__(self, db):
        self.db = db
        self.collection = self.db["histori"]

    def get_history(self, user_id, filter_type):
        query = {"user_id": ObjectId(user_id)}  # filter user id

        now = datetime.now()

        if filter_type == "harian":
            start = datetime(now.year, now.month, now.day)
            end = start + timedelta(days=1)
            query["tanggal"] = {"$gte": start, "$lt": end}
        elif filter_type == "mingguan":
            start = now - timedelta(days=now.weekday())  # Senin minggu ini
            start = datetime(start.year, start.month, start.day)
            end = start + timedelta(days=7)
            query["tanggal"] = {"$gte": start, "$lt": end}
        elif filter_type == "bulanan":
            start = datetime(now.year, now.month, 1)
            if now.month == 12:
                end = datetime(now.year + 1, 1, 1)
            else:
                end = datetime(now.year, now.month + 1, 1)
            query["tanggal"] = {"$gte": start, "$lt": end}
        else:
            return {"message": "Invalid filter type"}

        cursor = self.collection.find(query).sort("tanggal", 1)

        result = []
        for doc in cursor:
            result.append({
                "terapi": doc.get("terapi", ""),
                "tanggal": doc.get("tanggal").strftime("%d %B %Y %H:%M") if doc.get("tanggal") else "",
                "akurasi": doc.get("akurasi", "")
            })

        return result
