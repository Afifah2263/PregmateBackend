from flask import render_template, request, redirect, url_for
from bson.objectid import ObjectId
from flask import jsonify
from bson import ObjectId
from db_config import mongo  # pastikan koneksi db-nya sudah disiapkan
from flask import jsonify


keluhan_collection = None
terapi_collection = None

def set_db(db):
    global keluhan_collection, terapi_collection
    keluhan_collection = db['keluhan']
    terapi_collection = db['terapi']

def index_keluhan():
    keluhan_list = list(keluhan_collection.find())
    return render_template('Keluhan/index.html', keluhan_list=keluhan_list)

def tambah_keluhan():
    if request.method == 'POST':
        nama = request.form['nama']
        deskripsi = request.form['deskripsi']
        terapi_ids = request.form.getlist('rekomendasi_terapi_id')

        keluhan_collection.insert_one({
            'nama': nama,
            'deskripsi': deskripsi,
            'rekomendasi_terapi_id': [ObjectId(tid) for tid in terapi_ids]
        })
        return redirect(url_for('keluhan.index_keluhan'))

    terapi_list = list(terapi_collection.find())
    return render_template('Keluhan/form.html', action='Tambah', keluhan={}, terapi_list=terapi_list)


def edit_keluhan(id):
    keluhan = keluhan_collection.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        nama = request.form['nama']
        deskripsi = request.form['deskripsi']
        terapi_ids = request.form.getlist('rekomendasi_terapi_id')

        keluhan_collection.update_one({'_id': ObjectId(id)}, {
            '$set': {
                'nama': nama,
                'deskripsi': deskripsi,
                'rekomendasi_terapi_id': [ObjectId(tid) for tid in terapi_ids]
            }
        })
        return redirect(url_for('keluhan.index_keluhan'))

    terapi_list = list(terapi_collection.find())
    return render_template('Keluhan/form.html', action='Edit', keluhan=keluhan, terapi_list=terapi_list)

def hapus_keluhan(id):
    keluhan_collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('keluhan.index_keluhan'))

#############################################################################################################
# MOBILE
#############################################################################################################

def get_all_keluhan():
    keluhan_list = keluhan_collection.find()

    result = []
    for keluhan in keluhan_list:
        result.append({
            "_id": str(keluhan["_id"]),
            "nama": keluhan["nama"],
            "deskripsi": keluhan.get("deskripsi", ""),
            "rekomendasi_terapi_id": [str(tid) for tid in keluhan.get("rekomendasi_terapi_id", [])]
        })

    return jsonify(result)

# def get_terapi_by_ids():
#     terapi_ids = request.args.get("ids")
    
#     if not terapi_ids:
#         return jsonify({"error": "ids are required"}), 400

#     # Pisahkan ID berdasarkan koma
#     ids_list = terapi_ids.split(',')
    
#     try:
#         # Ubah ke ObjectId jika perlu dan lakukan query ke database
#         object_ids = [ObjectId(id) for id in ids_list]
#         terapies = terapi_collection.find({"_id": {"$in": object_ids}})
#     except Exception as e:
#         return jsonify({"error": f"Invalid ObjectId: {e}"}), 400

#     result = []
#     for terapi in terapies:
#         result.append({
#             "_id": str(terapi["_id"]),
#             "nama": terapi["nama"],
#             "deskripsi": terapi.get("deskripsi", ""),
#             "gambar": terapi.get("gambar", ""),
#             "peringatan": terapi.get("peringatan", "Lakukan dengan hati-hati"),
#         })

#     return jsonify(result)

# def get_terapi_by_id():
#     terapi_ids = request.args.get("id")

#     if not terapi_ids:
#         return jsonify({"error": "id is required"}), 400

#     # Pisahkan ID berdasarkan koma
#     ids_list = terapi_ids.split(',')
    
#     try:
#         # Ubah ke ObjectId jika perlu dan lakukan query ke database
#         object_ids = [ObjectId(id) for id in ids_list]
#         terapies = terapi_collection.find({"_id": {"$in": object_ids}})
#     except Exception as e:
#         return jsonify({"error": f"Invalid ObjectId: {e}"}), 400

#     result = []
#     for terapi in terapies:
#         result.append({
#             "_id": str(terapi["_id"]),
#             "nama": terapi["nama"],
#             "deskripsi": terapi.get("deskripsi", ""),
#             "gambar": terapi.get("gambar", ""),
#             "peringatan": terapi.get("peringatan", "Lakukan dengan hati-hati"),
#         })

#     return jsonify(result)


from flask import request, jsonify
from bson import ObjectId
from flask import Blueprint
import controller.controller_keluhan as controller_keluhan


def get_terapi_by_ids():
    terapi_ids = request.args.get("ids")

    if not terapi_ids:
        return jsonify({"error": "ids are required"}), 400

    try:
        ids_list = terapi_ids.split(',')
        print("Terima ID terapi:", ids_list)

        object_ids = [ObjectId(id.strip()) for id in ids_list]
        terapies = terapi_collection.find({"_id": {"$in": object_ids}})

        result = []
        for terapi in terapies:
            result.append({
                "_id": str(terapi["_id"]),
                "nama": terapi.get("nama", ""),
                "deskripsi": terapi.get("deskripsi", ""),
                "gambar": terapi.get("gambar", ""),
                "peringatan": terapi.get("peringatan", "Lakukan dengan hati-hati"),
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Invalid ObjectId: {e}"}), 400

def get_keluhan_by_id(id):
    try:
        keluhan = keluhan_collection.find_one({'_id': ObjectId(id)})
        if keluhan:
            keluhan['_id'] = str(keluhan['_id'])
            keluhan['rekomendasi_terapi_id'] = [str(tid) for tid in keluhan.get('rekomendasi_terapi_id', [])]
            return jsonify(keluhan)
        else:
            return jsonify({'error': 'Keluhan tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500