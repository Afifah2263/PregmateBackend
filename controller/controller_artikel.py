from flask import request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
from bson import ObjectId

db = None
artikel_collection = None

def set_db(database):
    global db, artikel_collection
    db = database
    artikel_collection = db['artikel']

def get_all_articles(search=''):
    query = {}
    if search:
        query = {
            "$or": [
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}}
            ]
        }
    articles = list(artikel_collection.find(query))
    for article in articles:
        article['_id'] = str(article['_id'])
        # Jika imageUrl ada dan belum ada host
        if 'imageUrl' in article and article['imageUrl'] and not article['imageUrl'].startswith('http'):
            # request.host_url sudah termasuk protokol dan host, misal: http://localhost:5000/
            article['imageUrl'] = request.host_url.rstrip('/') + article['imageUrl']
    return articles


def get_article_by_id(article_id):
    article = artikel_collection.find_one({'_id': ObjectId(article_id)})
    if article:
        article['_id'] = str(article['_id'])
        if 'imageUrl' in article and article['imageUrl'] and not article['imageUrl'].startswith('http'):
            article['imageUrl'] = request.host_url.rstrip('/') + article['imageUrl']
    return article


def create_article(title, content, image_file):
    filename = None
    if image_file:
        filename = secure_filename(image_file.filename)
        image_path = os.path.join('static/images/artikel', filename)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)  # Pastikan folder ada
        image_file.save(image_path)
    artikel_collection.insert_one({
        'title': title,
        'content': content,
        'imageUrl': f'/static/images/artikel/{filename}' if filename else ''
    })

def update_article(article_id, title, content, image_file):
    update_data = {
        'title': title,
        'content': content,
    }
    if image_file:
        filename = secure_filename(image_file.filename)
        image_path = os.path.join('static/images/artikel', filename)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        image_file.save(image_path)
        update_data['imageUrl'] = f'/static/images/artikel/{filename}'
    artikel_collection.update_one({'_id': ObjectId(article_id)}, {'$set': update_data})

def delete_article(article_id):
    artikel_collection.delete_one({'_id': ObjectId(article_id)})
