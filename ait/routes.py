from flask import  render_template, url_for, redirect
from ait.models import User, Post
from ait import app

@app.route('/')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/login')
def login():
    return render_template('./auth_page/pages-login.html', title = 'Login')

@app.route('/register')
def register():
    return render_template('./auth_page/pages-register.html', title = 'Register')