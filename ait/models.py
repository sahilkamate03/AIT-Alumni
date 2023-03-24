from ait import login_manager
from flask_login import UserMixin

from firebase_admin import auth

from datetime import date

def roleProvider(email):
    year =int('20' + email.split('@')[0].split('_')[1][0:2])
    currYear = int(date.today().year)

    if (year<currYear-4) :
        return 'Alumini'
    else :
        return 'Student'


@login_manager.user_loader
def load_user(uid):
    user = auth.get_user(uid)
    return User(uid, user.email)

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     profile_url = db.Column(db.String(500), nullable=False, default='')
#     role = db.Column(db.String(10), unique=False, nullable=False)
#     password = db.Column(db.String(60), nullable=False)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# from flask_login import UserMixin
# from firebase_admin import auth
class User(UserMixin):
    def __init__(self, uid, email):
        self.uid = uid
        self._email = email
        self.username = email.split('@')[0]
        self.role = roleProvider(email)
    
    def get_id(self):
        return str(self.uid)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
