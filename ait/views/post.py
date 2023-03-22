import os
import secrets
from flask import Blueprint, render_template, abort, url_for, redirect, jsonify, request
from flask_login import current_user, login_required
from ait import db_fire
from datetime import datetime

from ait.forms import PostForm

post =Blueprint('post',__name__)

@post.route('/get_post')
@login_required
def get_post():
    view_post = render_template('./post/view_post.html')
    data = {'remain': view_post}
    return jsonify(data)

def save_post_media(form_picture,username):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(post.root_path, f'static\media' , picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@post.route('/post/new', methods= ['GET','POST'])
@login_required
def new_post():
    if current_user.role != "Alumini":
        abort(403)
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
        if form.picture.data:
            picture_file = save_post_media(form.picture.data, current_user.username)
            data['media'] = picture_file

        id = current_user.username + data['date_created'].strftime(r'%Y%m%d%H%M%S')
        db_fire.collection('post').document(id).set(data)
        return redirect(url_for('home.home'))
    return render_template('new_post.html', title='New Post',form=form, legend='New Post', user_data = user_data)

@post.route('/comment/<string:post_id>', methods=['POST'])
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
        return redirect(url_for('home.home'))

@post.route('/like/<string:post_id>', methods=['POST'])
@login_required
def like(post_id):
        if request.method == "POST":
            result = db_fire.collection('post').document(post_id).get().to_dict()
            if current_user.username in result['likes']:
                temp = db_fire.collection('post').document(post_id).get().to_dict()['likes']
                temp.remove(current_user.username)
                db_fire.collection('post').document(post_id).set({'likes': temp}, merge =True)

            else:
                result['likes'].postend(current_user.username)
                db_fire.collection('post').document(post_id).set(result, merge = True)

        return redirect(url_for('home.home'))