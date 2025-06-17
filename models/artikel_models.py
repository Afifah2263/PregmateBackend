# models/artikel_models.py
from bson import ObjectId

db = None

def set_db(database):
    global db
    db = database

def get_all_articles():
    articles = db["artikel"].find()
    result = []
    for article in articles:
        result.append({
            "_id": str(article["_id"]),
            "title": article.get("title", ""),
            "content": article.get("content", ""),
            "imageUrl": article.get("imageUrl", "")  # PASTIKAN DISINI SAMA imageUrl bukan image_url
        })
    return result

