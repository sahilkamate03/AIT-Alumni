from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from flask_socketio import SocketIO, send

from firebase_admin import credentials
from firebase_admin import firestore
import pyrebase

import os
import json
from datetime import datetime

with open(os.path.join(os.path.dirname(__file__), 'config/admin_config.json')) as f:
    admin_config = json.load(f)

with open(os.path.join(os.path.dirname(__file__), 'config/firebase_config.json')) as f:
    firebaseConfig =  json.load(f)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'

cred = credentials.Certificate(admin_config)
firebase_admin.initialize_app(cred)

db = SQLAlchemy(app)
db_fire = firestore.client()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

firebase = pyrebase.initialize_app(firebaseConfig)

from ait.views import authentication, chat, connection, error_handling, home, post, profile

app.register_blueprint(authentication.authentication)
app.register_blueprint(chat.chat)
app.register_blueprint(connection.connect)
app.register_blueprint(error_handling.error_handling)
app.register_blueprint(home.home)
app.register_blueprint(post.post)
app.register_blueprint(profile.profile)
