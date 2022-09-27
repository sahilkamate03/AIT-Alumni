from flask import  render_template, url_for, redirect, jsonify, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from firebase_admin import auth
from firebase_admin import firestore

from ait import app, db, bcrypt
# from ait import firebase
from ait.forms import PostForm
from ait.models import User
from ait.forms import RegistrationForm, LoginForm

@app.route('/')
@app.route('/home')
@login_required
def home():
    # posts = Post.query.all()
    return render_template('home.html', title = 'Home')

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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.email.data.split("@")[0], email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        auth.create_user(email = form.email.data , password = form.password.data)
        return redirect(url_for('login'))
        
    return render_template('./auth_page/pages-register.html', title = 'Register', form =form)


@app.route('/get_post')
@login_required
def get_post():
    view_post = render_template('./post/view_post.html')

    data = {'remain': view_post}
    return jsonify(data)


@app.route('/new_post', methods= ['GET','POST'])
@login_required
def new_post():
    create_post = PostForm()
    if create_post.validate_on_submit():
        # post = Post(title = create_post.title.data, content = create_post.content.data, author = 1)
        db.session.add()
        db.session.commit()
        return redirect('home.html')
    return render_template('new_post.html', create_post = create_post)
