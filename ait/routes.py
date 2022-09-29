import secrets
from flask import  render_template, url_for, redirect, jsonify, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from firebase_admin import auth

import os
from datetime import datetime

from ait import app, db, bcrypt, db_fire
from ait import firebase
from ait.forms import PostForm
from ait.models import User
from ait.forms import RegistrationForm, LoginForm, PostForm



@app.route('/')
@app.route('/home')
@login_required
def home():
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    posts = db_fire.collection('post').get()
    return render_template('home.html', title = 'Home', user_data = user_data, posts = posts)

@app.route('/login', methods= ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            user_data = db_fire.collection(form.role.data).document(form.email.data.split('@')[0]).get().to_dict()
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('./auth_page/pages-login.html', title = 'Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
    

@app.route('/register',methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        data= {"name": form.name.data, 
        "username": form.email.data.split("@")[0],
        "email" : form.email.data,
        "role" : form.role.data,
        "add" : "-",
        "phone" : "-",
        "about" : "Write about yourself.",
        "profile_url" : ""
        }
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.email.data.split("@")[0], email=form.email.data, password=hashed_password, role = form.role.data)
        db.session.add(user)
        db.session.commit()
        # auth.create_user(email = form.email.data , password = form.password.data)
        db_fire.collection(form.role.data).document(form.email.data.split("@")[0]).set(data)
        return redirect(url_for('login'))
        
    return render_template('./auth_page/pages-register.html', title = 'Register', form =form)

def save_profile(form_media):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_media.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
    form_media.save(picture_path)
    return picture_fn

@app.route('/account')
@login_required
def account():
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    return render_template('users-profile.html', user_data = user_data)

@app.route('/account/edit/<string:username>', methods=['POST'])
@login_required
def edit_account(username):
    if username != current_user.username:
        abort()
    if request.method == "POST":
        print(request.form.get("picture_url"))
        if request.form.get("picture_url"):
            print(request.form.get("picture_url"))
        name = request.form.get("fullName")
        about = request.form.get("about")
        address = request.form.get("address")
        phone = request.form.get("phone")
        twitter = request.form.get("twitter")
        facebook = request.form.get("facebook")
        instagram = request.form.get("instagram")
        linkedin = request.form.get("linkedin")
        # print(name,about,address,phone,twitter,facebook,instagram,linkedin)
        data ={
            'name' : name,
            'about' : about,
            'add' : address,
            'phone' : phone,
            'twitter' : twitter,
            'facebook' : facebook,
            'instagram' : instagram,
            'linkedin' : linkedin
        }
        db_fire.collection(current_user.role).document(username).set(data, merge = True)

    return redirect(url_for('account'))

@app.route('/get_post')
@login_required
def get_post():
    view_post = render_template('./post/view_post.html')
    data = {'remain': view_post}
    return jsonify(data)

def save_post_media(form_picture,username):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static\media' , picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route('/post/new', methods= ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    if form.validate_on_submit():
            
        data = { "username" : current_user.username,
        "title" : form.title.data,
        "content" : form.content.data,
        "media" : '',
        "likes" : [],
        "comments" : {},
        "date_created" : datetime.utcnow(),
        "profile_url" : current_user.profile_url,
        "post_id" : current_user.username + datetime.utcnow().strftime(r'%Y%m%d%H%M%S'),
        "role" : current_user.role
        }
        print(form.picture.data)
        if form.picture.data:
            picture_file = save_post_media(form.picture.data, current_user.username)
            data['media'] = picture_file

        id = current_user.username + data['date_created'].strftime(r'%Y%m%d%H%M%S')
        db_fire.collection('post').document(id).set(data)
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post',form=form, legend='New Post', user_data = user_data)

@app.route('/comment/<string:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    if request.method == "POST":
        username = current_user.username
        date_created = datetime.utcnow()
        comment = request.form.get("comment")
        id = username + date_created.strftime(r'%Y%m%d%H%M%S')
        data = {
            id :{
            "date_created" : date_created,
            "comment" : comment,
            "username" : current_user.username,
            "profile_url" : current_user.profile_url
            }
        }
        db_fire.collection('post').document(post_id).set({"comments": data}, merge = True)
        return redirect(url_for('home'))

@app.route('/like/<string:post_id>', methods=['POST'])
@login_required
def like(post_id):
        if request.method == "POST":
            result = db_fire.collection('post').document(post_id).get().to_dict()
            if current_user.username in result['likes']:
                temp = db_fire.collection('post').document(post_id).get().to_dict()['likes']
                temp.remove(current_user.username)
                db_fire.collection('post').document(post_id).set({'likes': temp}, merge =True)

            else:
                db_fire.collection('post').document(post_id).set({'likes': [current_user.username]}, merge = True)

        return redirect(url_for('home'))

@app.route('/user/<string:role>/<string:username>')
@login_required
def user(username,role):
    if username == current_user.username:
        return redirect (url_for('account'))
    else:
        posts = db_fire.collection('post').where('username','==',username).get()
        user_data = db_fire.collection(role).document(username).get().to_dict()
        return render_template('user.html', user_data = user_data, posts = posts )

