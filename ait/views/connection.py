from flask import Blueprint, render_template, abort, url_for, redirect
from flask_login import current_user, login_required
from ait import db_fire
from datetime import datetime
from ait.models import User

connect =Blueprint('connection',__name__)

@connect.route('/connection')
@login_required
def connection():
    doc_ref = db_fire.collection('connection').document(current_user.username)
    doc = doc_ref.get()
    type = db_fire.collection('connection').document(current_user.username).get().to_dict()
    print(type)
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    return render_template('connection.html', user_data = user_data, type = type)

@connect.route('/connection/send/<string:username>')
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

        return redirect(url_for('profile.user',username = username, role = role))

@connect.route('/connection/remove/<string:username>')
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

        return redirect(url_for('profile.user',username = username, role = role))

@connect.route('/connection/<string:type>/<string:username>')
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
                    accept_data.connectionend(username)
                else:
                    accept_data = [username]
                
                doc_ref.set({'accept': accept_data},merge = True)
                doc_ref.set({'pending': data},merge = True)

            if type == "reject":
                data = doc.to_dict()['pending']
                data.remove(username)
                doc_ref.set({'pending': data},merge = True)

        return redirect(url_for('home.home'))