from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user
from firebase_admin import auth
import pyrebase

from ait import db_fire
from ait.models import User
from ait import db, bcrypt, db_fire, pyrebase
from ait.forms import LoginForm, RegistrationForm

from datetime import date

authentication =Blueprint('authentication',__name__)
pyrebase_auth = pyrebase.auth()

def roleProvider(email):
    year =int('20' + email.split('@')[0].split('_')[1][0:2])
    currYear = int(date.today().year)

    if (year<currYear-4) :
        return 'Alumini'
    else :
        return 'Student'

@authentication.route('/login', methods= ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_latest'))
    form = LoginForm()
    if form.validate_on_submit():
        email =form.email.data
        password =form.password.data
        try:
            user_id =auth.get_user_by_email(email)
        except:
            return redirect(url_for('authentication.register'))
        
        try:
            info= pyrebase_auth.sign_in_with_email_and_password(email, password)
            user_id =info['localId']
            user = User(user_id,email)
            next_page = request.args.get('next')
            login_user(user)
            return redirect(next_page) if next_page else redirect(url_for('home.home_latest'))
        except Exception as e: 
            flash('Login Unsuccessful. Please check email and password', 'danger')
            print(e)
            return redirect(url_for('authentication.login'))
        
    return render_template('./auth_page/pages-login.html', title = 'Login', form=form)

@authentication.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))
    
@authentication.route('/register',methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_latest'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print('success')
        email =form.email.data
        password =form.password.data
        user =auth.create_user(email =email, password =password)
        role =roleProvider(email)
        data= {"name": form.name.data, 
        "username": email.split("@")[0],
        "email" : email,
        "role" : role,
        "add" : "-",
        "phone" : "-",
        "about" : "Write about yourself.",
        "profile_url" : ""
        }
        
        return redirect(url_for('authentication.login'))
        
    return render_template('./auth_page/pages-register.html', title = 'Register', form =form)
