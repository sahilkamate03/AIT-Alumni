from ait import login_manager
from flask_login import UserMixin

from firebase_admin import auth

@login_manager.user_loader
def load_user(user_id):
    user = auth.get_user(user_id)
    return User(user.uid)

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
    def __init__(self, uid):
        self.uid = uid
        self._user = None
    
    def get_id(self):
        return self.uid
    
    @staticmethod
    def get(user_id):
        user = User(user_id)
        user._user = auth.get_user(user_id)
        if not user._user:
            return None
        return user

    @property
    def email(self):
        return self._user.email if self._user else None

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
