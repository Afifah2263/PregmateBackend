import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import controller.controller_terapi as controller_terapi

terapi_bp = Blueprint('terapi', __name__)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@terapi_bp.route('/terapi')
def index_terapi():
    terapi_list = controller_terapi.get_all_terapi()
    return render_template('terapi/index.html', terapi_list=terapi_list)

@terapi_bp.route('/terapi/create', methods=['GET', 'POST'])
def create_terapi():
    if request.method == 'POST':
        data = {
            'nama': request.form['nama'],
            'deskripsi': request.form['deskripsi'],
            'video_url': request.form['video_url'],
            'model_id': request.form['model_id'],
            'landmark_referensi_id': request.form['landmark_referensi_id'],
            'gambar': '',
            'peringatan': request.form.get('peringatan', '')
        }

        gambar_file = request.files['gambar']
        if gambar_file and allowed_file(gambar_file.filename):
            filename = secure_filename(gambar_file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            gambar_file.save(filepath)
            data['gambar'] = filepath
        else:
            flash("Gambar tidak valid")
            return redirect(request.url)

        controller_terapi.add_terapi(data)
        return redirect(url_for('terapi.index_terapi'))

    return render_template('terapi/form.html', action="Tambah", terapi=None)

@terapi_bp.route('/terapi/edit/<id>', methods=['GET', 'POST'])
def edit_terapi(id):
    terapi = controller_terapi.get_terapi_by_id(id)
    if not terapi:
        flash("Terapi tidak ditemukan")
        return redirect(url_for('terapi.index_terapi'))

    if request.method == 'POST':
        data = {
            'nama': request.form['nama'],
            'deskripsi': request.form['deskripsi'],
            'video_url': request.form['video_url'],
            'model_id': request.form['model_id'],
            'landmark_referensi_id': request.form['landmark_referensi_id'],
            'gambar': terapi['gambar'],  # default
            'peringatan': request.form.get('peringatan', terapi.get('peringatan', ''))
        }

        gambar_file = request.files['gambar']
        if gambar_file and allowed_file(gambar_file.filename):
            filename = secure_filename(gambar_file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            gambar_file.save(filepath)
            data['gambar'] = filepath

        controller_terapi.update_terapi(id, data)
        return redirect(url_for('terapi.index_terapi'))

    return render_template('terapi/form.html', action="Edit", terapi=terapi)

@terapi_bp.route('/terapi/delete/<id>', methods=['GET'])
def hapus_terapi(id):
    controller_terapi.delete_terapi(id)
    return redirect(url_for('terapi.index_terapi'))

@terapi_bp.route('/detail/<id>')
def detail_terapi(id):
    terapi = controller_terapi.get_terapi_by_id(id)
    return render_template('terapi/detail_terapi.html', terapi=terapi)

# ------------------- API ROUTE UNTUK FLUTTER -------------------
from flask import jsonify

@terapi_bp.route('/api/terapi', methods=['GET'])
def api_terapi_list():
    terapi_list = controller_terapi.get_all_terapi()
    for terapi in terapi_list:
        terapi['_id'] = str(terapi['_id'])

        # Ubah path lokal menjadi URL yang bisa diakses
        if 'gambar' in terapi and terapi['gambar']:
            terapi['gambar'] = request.host_url + terapi['gambar']
    return jsonify(terapi_list)
