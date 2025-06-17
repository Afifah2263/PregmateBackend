from flask import Blueprint, request, render_template
from controller import controller_keluhan
from flask import jsonify

keluhan_bp = Blueprint('keluhan', __name__)

@keluhan_bp.route('/keluhan')
def index_keluhan():
    return controller_keluhan.index_keluhan()

@keluhan_bp.route('/tambah_keluhan', methods=['GET', 'POST'])
def tambah_keluhan():
    return controller_keluhan.tambah_keluhan()

@keluhan_bp.route('/edit_keluhan/<id>', methods=['GET', 'POST'])
def edit_keluhan(id):
    return controller_keluhan.edit_keluhan(id)

@keluhan_bp.route('/hapus_keluhan/<id>', methods=['GET'])
def hapus_keluhan(id):
    return controller_keluhan.hapus_keluhan(id)

@keluhan_bp.route("/keluhan_all", methods=["GET"])
def get_all_keluhan():
    return controller_keluhan.get_all_keluhan()

@keluhan_bp.route("/terapi_by_ids", methods=["GET"])
def get_terapi_by_ids():
    return controller_keluhan.get_terapi_by_ids()

@keluhan_bp.route('/keluhan/<id>', methods=['GET'])
def get_keluhan_by_id(id):
    return controller_keluhan.get_keluhan_by_id(id)

