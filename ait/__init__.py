from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from flask_socketio import SocketIO, send

from firebase_admin import credentials
from firebase_admin import firestore
import pyrebase

import json
from datetime import datetime

admin_config = {
    "type": "service_account",
    "project_id": "day-planner-5165f",
    "private_key_id": "83e4ce0e84a5ea2c2a40f9101a00edd16a4edcaa",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDBYrwzBdpoTR4k\nkQ63nojx31S9mGTywbsZip2x2BeBjM2Bb/HL/UdYkW2ZDkefuo9gNLbNUQi2holB\nwkTWwMKXUty7Oq1lIhpl7kghIS87Q9by2txQAbuMDKS4+hXLG+36gJ0vbRJkyeX0\nPSQxrRuyrbo/IcG3jbDEsdpNOYa7UJ3nQFqSjiuuWlvRNfFADQa40AcxJrKNybo8\ndVjEhlFJuuqbfFaXTYGJaUIHvbKuc9Ro0s/WyIoGydcGcjItPCOkBRPuVnnb0JTJ\nSBFs2oDv4e4EE1jYHk3/X0heQpwTn/pCl7u4Zn6VY+YcZsRi8syBFS3pX045+DLi\nqoe6y4sdAgMBAAECggEAIP7luZbwEwfFctvFNRM5rns6jDbqUnk3oT4Ddgq2yAXs\nMn+VNAb9G2GE366ODfTY7cNQxWtkHzCJTs0EzdeJ3CPpQZDbcPwGoQmtCOoOkwAa\nNsmc+ZGyHE0z9dPF0CftzOYQ67yifMvuDmQ4PrmYlj4KHyd1VAo69PSbmL2N/XuR\nkofmdhUliFH4ER07L9BIQv8bW70+/iwJfwkLLcOXqeGzZTX+DA9tADFisVW2V9OE\na5YsWLCBYRVNy6+fS2CAaykF9y0Iqrw+snxshbxWoJxcM5LI5YqMNcClWF8AEu0P\naTXFoChfht0iEox+FZ/LrSf9m+Oo2E338CbhqppkiQKBgQD0X65KD/Ju8PCADTN/\n0cLhsD5yS2loxKth+vFL33ZIwZ8ypZEL8O1vQhk2f8L3oHCSGy75LuAVSxe2czIU\nco7GC3ovVtKR6owFXXF5NOFyRZkTkxPeKMZZYMClKiztNC81QPwMclNrNlnCfjwy\nZQgoSa6QEX6QXdN+7s0EKe1MewKBgQDKlg02Dn/QwutiLI8wKMAAPI1oJK8TxO2i\nUO8Y9ttAxW7LWpMqvAuFz2KpEhy2cNN/IU3CQrKELFF+pYh7+8rP2CeZW5oSKgYe\nWrAcFYVMFzyzboC6Rt5NiGSZYa53kBBslW4bSfdtUOv9QT/wT+zmrblt5/dYEwY/\nmlTLpdZvRwKBgENrlmlGhwtGnAOoILo2A/9CIahk19sYz3PDyQi2ySp/iM1vUloq\nCUe1w8D+dKre78/PgiErZpVZV1x14a40gOFwzy/6UzQAssrUIfdfuIdPXlFBNa0I\nMNj90Yh/308+I3wcxq0kaZFduFvpefApYZvD4E5NFU79I9mURqnMa3S7AoGBALPZ\nvuTMvoBRa7L+qCgzJTGQkGFyn9PHMsi1XW8mSMQaAyCZyqlXxEsJMCe1IrR9OeZV\nZLkfiWh6B+eNgbvAb+9RkOY/Qmr5z/DGxi5IlMxWnNcXNUUqgVUHz3e0FrWiulIL\n33JumjD8dGWjteXcrw6kEEkYdKhGS3fPxZP+KH8lAoGALCVvlpS7rfrOZPz5Bzrv\n1ou38dBHSH+bNxz3bqNNAf7PB1mjt9zxbisqPyZgyX+GYsb4WUy6/yU0C9qpDkE1\noRtgW65cayqPWQVx6BZ6OyEFCjDu6zDoRA/EZkAbk1zszbftpUBndpsUFavxM+AN\nzV0h8JpI75uo+Y6muyThqq8=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-rincw@day-planner-5165f.iam.gserviceaccount.com",
    "client_id": "101312543958252486473",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-rincw%40day-planner-5165f.iam.gserviceaccount.com"
}

firebaseConfig = {
	"apiKey": "AIzaSyAUBaH94HsV0b0BgKprPZ6uwcr4IT2De78",
	"authDomain": "day-planner-5165f.firebaseapp.com",
	"databaseURL": "https://day-planner-5165f-default-rtdb.firebaseio.com",
	"projectId": "day-planner-5165f",
	"storageBucket": "day-planner-5165f.appspot.com",
	"messagingSenderId": "957874282773",
	"appId": "1:957874282773:web:93bbb3ac3802131130091c",
	"measurementId": "G-BZHRXN4120"
}

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

from ait import routes