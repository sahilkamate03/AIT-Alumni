import secrets
from flask import  render_template, url_for, redirect, jsonify, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from flask_socketio import send

from firebase_admin import auth, firestore

import os
from datetime import datetime

from ait import app, db, bcrypt, db_fire, socketio
from ait import firebase
from ait.forms import PostForm
from ait.models import User
from ait.forms import RegistrationForm, LoginForm, PostForm



@app.route('/')
@app.route('/home/latest')
@login_required
def home():
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    posts = db_fire.collection('post').order_by("date_created", direction=firestore.Query.DESCENDING).get()
    return render_template('home.html', title = 'Home', user_data = user_data, posts = posts)

@app.route('/')
@app.route('/home/top')
@login_required
def home_top():
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    posts = db_fire.collection("post").order_by("likes", direction=firestore.Query.DESCENDING).get()
    return render_template('home_top.html', title = 'Home', user_data = user_data, posts = posts)

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

def save_profile(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static\profile_pic' , picture_fn)
    form_picture.save(picture_path)
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
        name = request.form.get("fullName")
        about = request.form.get("about")
        address = request.form.get("address")
        phone = request.form.get("phone")
        twitter = request.form.get("twitter")
        facebook = request.form.get("facebook")
        instagram = request.form.get("instagram")
        linkedin = request.form.get("linkedin")
        cv_link = request.form.get("cv_link")
        data ={
            'name' : name,
            'about' : about,
            'add' : address,
            'phone' : phone,
            'twitter' : twitter,
            'facebook' : facebook,
            'instagram' : instagram,
            'linkedin' : linkedin,
            'cv_link' : cv_link,
        }
        
        picture_url = request.files["picture_url"]
        if picture_url.filename:
            final = save_profile(picture_url)
            current_user.profile_url = final
            data["profile_url"] = final
            db.session.commit()
        
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
                result['likes'].append(current_user.username)
                db_fire.collection('post').document(post_id).set(result, merge = True)

        return redirect(url_for('home'))

@app.route('/user/<string:role>/<string:username>')
@login_required
def user(username,role):
    if username == current_user.username:
        return redirect (url_for('account'))
    else:
        posts = db_fire.collection('post').where('username','==',username).get()
        user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
        profile_data = db_fire.collection(role).document(username).get().to_dict()
        type = db_fire.collection('connection').document(current_user.username).get()
        
        value = False
        
        if type.exists:
            if username in type.to_dict().keys():
                value = True 
        return render_template('user.html', profile_data = profile_data,user_data = user_data, posts = posts, value = value  )


#--------------------------connection-----------------------------------------

@app.route('/connection')
@login_required
def connection():
    doc_ref = db_fire.collection('connection').document(current_user.username)
    doc = doc_ref.get()
    type = db_fire.collection('connection').document(current_user.username).get().to_dict()
    print(type)
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    return render_template('connection.html', user_data = user_data, type = type)

@app.route('/connection/send/<string:username>')
@login_required
def send_req(username):
    if username == current_user.username:
        abort(403)
    else:
        doc_ref =   db_fire.collection('connection').document(current_user.username)
        user_data = db_fire.collection('Alumini').document(username).get().to_dict()
        data = db_fire.collection('connection').document(current_user.username).get()
        
        print(data.exists)
        if data.exists:
            print(data.to_dict())
            temp = data.to_dict()
            if user_data['username'] in data.to_dict().keys():
                print("hello in userdata")
                temp.pop(user_data['username'])
            
            else:    
                temp.update({ 
                    user_data['username'] :{
                    'username' : user_data['username'],
                    'profile_url' : user_data['profile_url'],
                    'created_at' : datetime.utcnow()
                    }
                    })
            db_fire.collection('connection').document(current_user.username).set( temp ,merge = True)
            
        else:
            temp = { 
                user_data['username'] :{
                'username' : user_data['username'],
                'profile_url' : user_data['profile_url'],
                'created_at' : datetime.utcnow()
                }
                }
            doc_ref.set(temp, merge = True)
                

        user = User.query.filter_by(username=username).first()
        role = user.role

        return redirect(url_for('user',username = username, role = role))

@app.route('/connection/remove/<string:username>')
@login_required
def remove_req(username):
    if username == current_user.username:
        abort(403)
    else:
        data_user = db_fire.collection('connection').document(current_user.username).get().to_dict()
        data_user.pop(username,None)
        db_fire.collection('connection').document(current_user.username).set( data_user ,merge = True)
        user = User.query.filter_by(username=username).first()
        role = user.role

        return redirect(url_for('user',username = username, role = role))

@app.route('/connection/<string:type>/<string:username>')
@login_required
def action_req(username,type):
    if username == current_user.username:
        abort(403)
    else:
        doc_ref =   db_fire.collection('connection').document(current_user.username)
        doc = doc_ref.get()

        if doc.exists:
            if type == "accept":
                data = doc.to_dict()['pending']
                data.remove(username)
                
                if 'accept' in doc.to_dict().keys():
                    accept_data = doc.to_dict()['accept']
                    accept_data.append(username)
                else:
                    accept_data = [username]
                
                doc_ref.set({'accept': accept_data},merge = True)
                doc_ref.set({'pending': data},merge = True)

            if type == "reject":
                data = doc.to_dict()['pending']
                data.remove(username)
                doc_ref.set({'pending': data},merge = True)

        return redirect(url_for('home'))

#--------------------------chat-app--------------------------------------------------
@socketio.on("message")
def sendMessage(message):
    message = current_user.username+ ": " + message
    print(message)
    send(message, broadcast=True)

@app.route('/chat')
@login_required
def chat():
    username = current_user.username
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()

    return render_template('chat.html', username = username, user_data = user_data)

#----------------------------------Error handle ---------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    return render_template('pages-error-404.html', user_data = user_data), 404