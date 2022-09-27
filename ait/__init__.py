from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials
import pyrebase

from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'

cred = credentials.Certificate(r'D:\code\hackathon\De`Verse-22\test\config\admin_config.json')
firebase_admin.initialize_app(cred)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# with open('D:/code/hackathon/De`Verse-22/test/config/firebase_config.json', 'r') as f:
#     firebaseConfig = json.load(f)
# firebase = pyrebase.initialize_app(firebaseConfig)

from ait import routes