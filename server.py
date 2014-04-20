#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import json
import os
import time

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class Notes(db.Model):
    __tablename__ = 'notes7'
    id = db.Column(db.String,primary_key = True)
    gcm_id = db.Column(db.String(100))
    title = db.Column(db.String(100))
    tags = db.Column(db.String(100))
    img_path = db.Column(db.String(200))
    def __init__(self,id,gcm_id,title,tags,img_path):
        # Initializes the fields with entered data
        self.id = id
        self.gcm_id = gcm_id
        self.title = title
        self.tags = tags
        self.img_path = img_path

class User(db.Model):
    __tablename__ = 'user6'
    gcm_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    tag_line = db.Column(db.String(200))
    dob = db.Column(db.String(200))
    address = db.Column(db.String(200))
    ins_type = db.Column(db.String(200))
    subjects = db.Column(db.String(200))

    def __init__(self,gcm_id,name,email,tag_line,address,dob,ins_type,ins_name,subjects):
        # Initializes the fields with entered data
        self.gcm_id = gcm_id
        self.name = name
        self.email = email
        self.tag_line = tag_line
        self.address = address
        self.dob = dob
        self.ins_type = ins_type
        self.ins_name = ins_name
        self.subjects = subjects

def db_init():
    db.create_all()
    comment = User("a1","b","c","d","e","f","g","h","i")
    db.session.add(comment)
    db.session.commit()

@app.route('/view_all')
def foo():
    arr = []
    for u in db.session.query(User).all():
        arr.append(str(u.__dict__))
    return str(arr)

@app.route('/add')
def add_user():
    gcm_id = request.args.get('gcm_id')
    name = request.args.get('name') or ''
    email = request.args.get('email') or 'aaasd'
    tag_line = request.args.get('tag_line') or ''
    address = request.args.get('address') or ''
    dob = request.args.get('dob') or ''
    ins_type = request.args.get('ins_type') or ''
    ins_name = request.args.get('ins_name') or ''
    subjects = request.args.get('subjects') or ''

    db.create_all()
    user_object = User(gcm_id,name,email,tag_line,address,dob,ins_type,ins_name,subjects)
    db.session.add(user_object)
    db.session.commit()    
    return "{'status':200,\n\t'response':'User has been added'}"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/test-upload')
def upload_test():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    gcm_id = request.args.get('gcm_id') or ''
    title = request.args.get('title') or ''
    tags = request.args.get('tags') or 'food,icecream,biology'

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = "%d_%s"%(int(time.time()),filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img_path = "http://tosc.in:5002/uploads/%s"%filename
    db.create_all()
    id = str(time.time())
    notes_object = Notes(id,gcm_id,title,tags,img_path)
    db.session.add(notes_object)
    db.session.commit()
    return "{'status':200,\n\t'response':'%s'}"%img_path

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    tags = request.args.get('tags') or ''
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/notes')
def notes():
    arr = []
    for u in db.session.query(Notes).all():
        d = {}
        d['name'] = str(u.__dict__['title']) 
        d['url'] = str(u.__dict__['img_path'])
        d['tags'] = str(u.__dict__['tags'])
        arr.append(d)
    return json.dumps(arr)

if __name__ == '__main__':
    #db_init()
    app.debug = True
    app.run(host='0.0.0.0',port=5002)

