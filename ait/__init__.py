from flask import Flask, send_from_directory
from flask_login import LoginManager
from flask_socketio import SocketIO, send
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
import pyrebase

from cryptography.fernet import Fernet
import os
import json
from datetime import datetime

fernet = Fernet(os.getenv("FERNET_KEY"))

with open(
        os.path.join(os.path.dirname(__file__),
                     'config/encrypted_admin_config.txt')) as f:
    encrypted_admin_config = f.read()
    admin_config = json.loads(fernet.decrypt(encrypted_admin_config).decode())

with open(
        os.path.join(os.path.dirname(__file__),
                     'config/encrypted_firebase_config.txt')) as f:
    encrypted_firebase_config = f.read()
    firebase_config = json.loads(
        fernet.decrypt(encrypted_firebase_config).decode())

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['SECRET_KEY'] = os.getenv("SQL_ACLCHEMY_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

cred = credentials.Certificate(admin_config)
firebase_admin.initialize_app(
    cred, {'storageBucket': 'day-planner-5165f.appspot.com'})
pyrebase = pyrebase.initialize_app(firebase_config)

db_fire = firestore.client()
login_manager = LoginManager(app)
login_manager.login_view = 'authentication.login'
login_manager.login_message_category = 'info'

from ait.views import authentication, chat, connection, error_handling, home, post, profile

app.register_blueprint(authentication.authentication)
app.register_blueprint(chat.chat)
app.register_blueprint(connection.connect)
app.register_blueprint(error_handling.error_handling)
app.register_blueprint(home.home)
app.register_blueprint(post.post)
app.register_blueprint(profile.profile)
