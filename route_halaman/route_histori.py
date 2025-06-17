from flask import Blueprint, request, jsonify
from datetime import datetime
from controller.controller_histori import (
    format_histori_data,
    get_histori,
    get_histori_stats,
    get_histori_filtered,
)

histori_bp = Blueprint('histori_bp', __name__)

# Variabel global untuk koleksi MongoDB histori
histori_collection = None

def set_db(database):
    global histori_collection
    histori_collection = database["histori"]

@histori_bp.route('/histori', methods=['POST'])
def simpan_histori():
    data = request.get_json()
    user_id = data.get("user_id")
    label = data.get("label")
    accuracy = data.get("accuracy")
    tanggal = datetime.utcnow()

    if not all([user_id, label, accuracy is not None]):
        return jsonify({"message": "Data tidak lengkap"}), 400

    histori_baru = {
        "user_id": user_id,
        "label": label,
        "accuracy": float(accuracy),
        "tanggal": tanggal
    }

    histori_collection.insert_one(histori_baru)
    return jsonify({"message": "Histori berhasil disimpan"}), 201

@histori_bp.route('/histori/<string:user_id>', methods=['GET'])
def tampilkan_histori(user_id):
    if histori_collection is None:
        return jsonify({"error": "Database belum diinisialisasi"}), 500
    data = get_histori(histori_collection, user_id)
    return jsonify(data), 200

@histori_bp.route('/histori/stats/<string:user_id>', methods=['GET'])
def histori_stats(user_id):
    if histori_collection is None:
        return jsonify({"error": "Database belum diinisialisasi"}), 500
    stats = get_histori_stats(histori_collection, user_id)
    return jsonify(stats), 200

@histori_bp.route('/histori/filter/<string:filter_type>', methods=['GET'])
def histori_filtered(filter_type):
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400
    if histori_collection is None:
        return jsonify({"error": "Database belum diinisialisasi"}), 500

    data = get_histori_filtered(histori_collection, user_id, filter_type)
    return jsonify(data), 200
