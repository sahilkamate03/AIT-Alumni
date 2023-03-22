from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user
from ait import db_fire
from ait.models import User
from ait import db, bcrypt, db_fire

from ait.forms import LoginForm, RegistrationForm

authentication =Blueprint('authentication',__name__)

@authentication.route('/login', methods= ['GET', 'POST'])
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
            return redirect(next_page) if next_page else redirect(url_for('home.home_latest'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('./auth_page/pages-login.html', title = 'Login', form=form)

@authentication.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))
    
@authentication.route('/register',methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
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
        return redirect(url_for('authentication.login'))
        
    return render_template('./auth_page/pages-register.html', title = 'Register', form =form)
