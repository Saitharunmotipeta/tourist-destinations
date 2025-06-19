from flask import Flask, request, redirect, url_for, render_template, send_from_directory 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from models import db, User, Place, PlaceImage, LikedPlace
from extensions import db
from flask_socketio import SocketIO
import os


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
    os.makedirs(app.config['UPLOAD_FOLDER'] , exist_ok=True)

from routes import *
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

