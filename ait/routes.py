from flask import  render_template, url_for, redirect, jsonify

import json

from ait import app, db
from ait.forms import PostForm
from ait.models import User, Post


@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', title = 'Home',posts = posts)

@app.route('/login')
def login():
    return render_template('./auth_page/pages-login.html', title = 'Login')

@app.route('/register')
def register():
    return render_template('./auth_page/pages-register.html', title = 'Register')


@app.route('/get_post')
def get_post():
    view_post = render_template('./post/view_post.html')

    data = {'remain': view_post}
    return jsonify(data)


@app.route('/new_post', methods= ['GET','POST'])
def new_post():
    create_post = PostForm()
    if create_post.validate_on_submit():
        post = Post(title = create_post.title.data, content = create_post.content.data, author = 1)
        db.session.add()
        db.session.commit()
        return redirect('home.html')
    return render_template('new_post.html', create_post = create_post)
