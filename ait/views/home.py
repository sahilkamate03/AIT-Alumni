from flask import Blueprint, render_template
from flask_login import current_user, login_required
from ait import db_fire
from firebase_admin import firestore

home =Blueprint('home',__name__)

@home.route('/')
@home.route('/home/latest')
@login_required
def home_latest():
    print(current_user.role)
    print(current_user.email)
    print(current_user.uid)
    # user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    # posts = db_fire.collection('post').order_by("date_created", direction=firestore.Query.DESCENDING).get()
    return render_template('test.html', title = 'Home')

@home.route('/home/top')
@login_required
def home_top():
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    posts = db_fire.collection("post").order_by("likes", direction=firestore.Query.DESCENDING).get()
    return render_template('home_top.html', title = 'Home', user_data = user_data, posts = posts)
