from datetime import datetime
from flask import  render_template, url_for, redirect, jsonify, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from firebase_admin import auth

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
        "about" : "Write about yourself."
        }
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.email.data.split("@")[0], email=form.email.data, password=hashed_password, role = form.role.data)
        db.session.add(user)
        db.session.commit()
        # auth.create_user(email = form.email.data , password = form.password.data)
        db_fire.collection(form.role.data).document(form.email.data.split("@")[0]).set(data)
        return redirect(url_for('login'))
        
    return render_template('./auth_page/pages-register.html', title = 'Register', form =form)

@app.route('/account')
@login_required
def account():
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    return render_template('users-profile.html', user_data = user_data)


@app.route('/get_post')
@login_required
def get_post():
    view_post = render_template('./post/view_post.html')

    data = {'remain': view_post}
    return jsonify(data)


@app.route('/post/new', methods= ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    if form.validate_on_submit():
        data = { "username" : current_user.username,
        "title" : form.title.data,
        "content" : form.content.data,
        "media" : {},
        "likes" : 0,
        "comments" : {},
        "date_created" : datetime.utcnow(),
        }
        db_fire.collection('post').document().set(data)
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post',form=form, legend='New Post', user_data = user_data)
