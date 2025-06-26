from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from models import db, User, Place, PlaceImage, LikedPlace
from extensions import db
from flask_socketio import SocketIO
import os
import logging
import subprocess

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECRET_KEY"] = "ashborn"
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

db.init_app(app)

# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from routes import *

# Run insert_places.py at the start of the app
def run_insert_places():
    try:
        subprocess.run(["python", "insert_places.py"], check=True)
    except Exception as e:
        print(f"Error running insert_places.py: {e}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    run_insert_places()  # Execute insert_places.py when the app starts
    app.run(debug=True)

# Suppress werkzeug logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
