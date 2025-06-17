from flask import Flask, redirect, url_for
from flask_cors import CORS
from route import init_routes
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["Capstone2"]

app.config['db'] = db  # Pass DB via config

init_routes(app)  # inisialisasi routes

@app.route('/')
def home():
    return redirect(url_for('index_keluhan'))

if __name__ == "__main__":
    app.run(debug=True)
