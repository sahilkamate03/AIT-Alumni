from flask import  render_template, url_for, redirect, jsonify

import json

from ait import app
from ait.models import User, Post


@app.route('/')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/login')
def login():
    return render_template('./auth_page/pages-login.html', title = 'Login')

@app.route('/register')
def register():
    return render_template('./auth_page/pages-register.html', title = 'Register')

@app.route('/get_post')
def get_post():
    view_post = render_template(
        './post/view_post.html')

    data = {'remain': view_post}
    return jsonify(data)