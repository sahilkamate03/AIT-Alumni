from dotenv import load_dotenv
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user
from firebase_admin import auth
import pyrebase

from ait import db_fire
from ait.models import User
from ait import db_fire, pyrebase
from ait.forms import LoginForm, RegistrationForm, PasswordRestForm, EmailVerificationForm

import os
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()
authentication =Blueprint('authentication',__name__)
pyrebase_auth = pyrebase.auth()

def roleProvider(email):
    year =int('20' + email.split('@')[0].split('_')[1][0:2])
    currYear = int(date.today().year)

    if (year<currYear-4) :
        return 'Alumini'
    else :
        return 'Student'


def send_verification_email(email):
    sender = os.getenv('EMAIL')
    verification_link =auth.generate_email_verification_link(email)
    recipient = email
    subject = 'Verify your email for AIT-Website'

    body = f'''
    Hello {email.split('@')[0]},

    Follow this link to verify your email address.

    {verification_link}

    If you didn’t ask to verify this address, you can ignore this email.

    Thanks
    '''

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.getenv('EMAIL')
    smtp_password = os.getenv('EMAIL_PWD')

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail(sender, recipient, message.as_string())

def reset_password(email):
    sender = os.getenv('EMAIL')
    reset_link =auth.generate_password_reset_link(email)
    recipient = email
    subject = 'Reset your password for AIT-Website'

    body = f'''
    Hello {email.split('@')[0]},

    Follow this link to reset your email address.

    {reset_link}

    If you didn’t ask to reset this address, you can ignore this email.

    Thanks
    '''

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.getenv('EMAIL')
    smtp_password = os.getenv('EMAIL_PWD')

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail(sender, recipient, message.as_string())


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
            flash('User not found. Create Account.', 'info')
            return redirect(url_for('authentication.register'))
        
        print(user_id.email_verified)
        if not(user_id.email_verified):
            flash('Verify your email.', 'info')
            return render_template('./auth_page/pages-login.html', title = 'Login', form=form)
            
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
        role =roleProvider(email)
        data= {"name": form.name.data, 
        "username": email.split("@")[0],
        "email" : email,
        "role" : role,
        "add" : "-",
        "phone" : "-",
        "about" : "Write about yourself.",
        "profile_url" : "",
        "verified" : False
        }
        try:
            db_fire.collection(role).document(form.email.data.split("@")[0]).set(data)
            auth.create_user(email =email, password =password)
            send_verification_email(email)
            flash(f'Verification link send to email.','info')
            return redirect(url_for('authentication.login'))
        except Exception as e:
            print(e)
        
    return render_template('./auth_page/pages-register.html', title = 'Register', form =form)

@authentication.route('/password_reset', methods= ['GET', 'POST'])
def password_reset():
    form = PasswordRestForm()
    if form.validate_on_submit():
        email =form.email.data
        try:
            auth.get_user_by_email(email)
        except:
            return redirect(url_for('authentication.register'))
        
        try:
            reset_password(email)
            return redirect(url_for('authentication.login'))
        except Exception as e: 
            flash('Login Unsuccessful. Please check email and password', 'danger')
            print(e)
            return redirect(url_for('authentication.login'))
        
    return render_template('./auth_page/pwd_reset.html', title = 'Password Reset', form=form)

@authentication.route('/send_verification_email', methods= ['GET', 'POST'])
def verify_email():
    form = EmailVerificationForm()
    if form.validate_on_submit():
        email =form.email.data
        try:
            auth.get_user_by_email(email)
        except:
            flash('User not found. Create Account.', 'info')
            return redirect(url_for('authentication.register'))
        
        try:
            print(email)
            send_verification_email(email)
            flash('Verification email send.', 'info')
            return redirect(url_for('authentication.login'))
        except Exception as e: 
            flash('Unable to send. Please check later.', 'danger')
            print(e)
            return redirect(url_for('authentication.login'))
        
    return render_template('./auth_page/verify_email.html', title = 'Verify Account', form=form)
