# ============================== IMPORT DAN SETUP DASAR ==============================

from flask import Flask, redirect, url_for, session, flash, jsonify, Blueprint, render_template, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask.json.provider import DefaultJSONProvider
from pymongo import MongoClient
from bson import ObjectId
import secrets
import os
import config

# Firebase & Scheduler (aktifkan jika kamu pakai)
from firebase_init import init_firebase
from scheduler import start_scheduler

# ============================== KONVERSI ObjectId AGAR BISA DI JSONIFY ==============================

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

# ============================== FLASK APP SETUP ==============================

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')
app.secret_key = secrets.token_hex(16)
app.json = CustomJSONProvider(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# JWT Configuration
app.config['JWT_SECRET_KEY'] = '12345'
jwt = JWTManager(app)

# ============================== DATABASE SETUP ==============================

client = MongoClient("mongodb://localhost:27017/")
db = client["capstone"]
users_collection = db["users"]
schedule_collection = db["schedules"]

# ============================== IMPORT MODEL & CONTROLLER ==============================

# Models
from models.admin_model import Admin
from models.datauser_model import User

# Controllers
import controller.controller_keluhan as controller_keluhan
import controller.controller_register as controller_register
import controller.controller_login as controller_login
import controller.controller_terapi as controller_terapi
import controller.controller_datauser as controller_datauser
import controller.controller_artikel as controller_artikel
from controller.controller_jadwal import jadwal_bp, set_db as set_jadwal_db
from route_halaman.route_histori import histori_bp, set_db as set_histori_db
from controller.userlog_controller import set_db as set_userlog_db
set_userlog_db(db)
# Set DB di controller dan model
User.set_db(db)
Admin.set_db(db)
controller_artikel.set_db(db)
controller_keluhan.set_db(db)
controller_register.set_db(db)
controller_login.set_db(db)
controller_terapi.set_db(db)
controller_datauser.set_db(db)
set_histori_db(db)
set_jadwal_db(db)

# ============================== BLUEPRINT REGISTRASI ==============================

def register_blueprints():
    from route_halaman.route_admin import admin_bp
    from route_halaman.route_keluhan import keluhan_bp
    from route_halaman.route_register import register_bp
    from route_halaman.route_login import login_bp
    from route_halaman.route_histori import histori_bp
    from route_halaman.route_terapi import terapi_bp
    from route_halaman.route_datauser import datauser_bp
    from route_halaman.route_artikel import artikel_bp
    from route_halaman.forgot_password_route import forgot_password_bp
    from route_halaman.histori_user_route import histori_user_bp

    app.register_blueprint(histori_user_bp)

    app.register_blueprint(forgot_password_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(artikel_bp, url_prefix='/api')
    app.register_blueprint(keluhan_bp)
    app.register_blueprint(register_bp, url_prefix='/auth')
    app.register_blueprint(login_bp, url_prefix='/auth')
    app.register_blueprint(terapi_bp)
    app.register_blueprint(datauser_bp,)
    app.register_blueprint(jadwal_bp)
    app.register_blueprint(histori_bp)
register_blueprints()

# ============================== ROUTES UTAMA ==============================

@app.route('/')
def home():
    return redirect('/admin/login')

@app.route('/keluhan')
def index_keluhan():
    return controller_keluhan.index_keluhan()

# ============================== RUN APLIKASI ==============================

if __name__ == '__main__':
    init_firebase()        # aktifkan jika kamu gunakan Firebase Admin SDK
    start_scheduler(db)    # aktifkan jika kamu gunakan fitur penjadwalan
    app.run(host='0.0.0.0', port=5000, debug=True)
