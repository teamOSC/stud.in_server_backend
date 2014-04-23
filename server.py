#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import json
import os
import time
import ast

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class Notes(db.Model):
    __tablename__ = 'notes15'
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
    __tablename__ = 'user9'
    gcm_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    tag_line = db.Column(db.String(200))
    dob = db.Column(db.String(200))
    address = db.Column(db.String(200))
    ins_type = db.Column(db.String(200))
    ins_name = db.Column(db.String(200))
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

class Tutor(db.Model):
    __tablename__ = 'tutor1'
    email = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100))
    subjects = db.Column(db.String(200))

    def __init__(self,email,name,subjects):
        self.email = email
        self.name = name
        self.subjects = subjects

#/view/User,/view/Notes,/view/Tutor
@app.route('/view/<dbname>')
def view_table(dbname):
    if dbname == 'Notes':
        arr = []
        for u in db.session.query(Notes).all():
            d = {}
            d['name'] = str(u.__dict__['title']) 
            d['url'] = str(u.__dict__['img_path'])
            d['tags'] = str(u.__dict__['tags'])
            path = str(u.__dict__['img_path'])
            path = path.split('/')
            path[-1] = 'thumb_' + path[-1]
            path = "/".join(path)
            d['thumb_img'] = path
            arr.append(d)
        return json.dumps(arr)
    else:
        arr = []
        try:
            a = getattr(sys.modules[__name__], dbname)
        except:
            return '404'
        for u in db.session.query(a).all():
            arr.append(str(u.__dict__))
        return json.dumps(arr)

@app.route('/add/<entity>')
def add_entity():
    if entity == 'User':
        gcm_id = request.args.get('gcm_id')
        name = request.args.get('name')
        email = request.args.get('email')
        tag_line = request.args.get('tag_line')
        address = request.args.get('address')
        dob = request.args.get('dob')
        ins_type = request.args.get('ins_type')
        ins_name = request.args.get('ins_name')
        subjects = request.args.get('subjects')

        db.create_all()
        user_object = User(gcm_id,name,email,tag_line,address,dob,ins_type,ins_name,subjects)
        db.session.add(user_object)
        db.session.commit()
        return "{'status':200,\n\t'response':'User has been added'}"

    if entity == 'Tutor':
        email = request.args.get('email')
        subjects = request.args.get('subjects')
        name = request.args.get('name')
        db.create_all()
        tutor_object = Tutor(email,name,subjects)
        db.session.add(tutor_object)
        db.session.commit()
        return 'success'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/test')
def upload_test():
    return render_template('upload.html')

def gen_thumb(file_name):
    curr_path = os.path.abspath(__file__)
    curr_path = curr_path.split('/')[:-1]
    curr_path = "/".join(curr_path) + '/uploads'
    os.system("convert %s/%s -resize 250x250  %s/thumb_%s"%(curr_path,file_name,curr_path,file_name))

def gen_white(file_name):
    curr_path = os.path.abspath(__file__)
    curr_path = curr_path.split('/')[:-1]
    curr_path = "/".join(curr_path) + '/uploads'
    os.system("./whiteboard.sh %s/%s  %s/white_%s"%(curr_path,file_name,curr_path,file_name))

@app.route('/upload', methods=['POST'])
def upload():
    gcm_id = request.form.get('gcm_id')
    title = request.form.get('title')
    tags = request.form.get('tags')

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = "%d_%s"%(int(time.time()),filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img_path = "http://tosc.in:5002/uploads/%s"%filename
        thumb_path = "http://tosc.in:5002/uploads/thumb_%s"%filename
        #white_path = "http://tosc.in:5002/uploads/white_%s"%filename
        gen_thumb(filename)
        #gen_white(filename)

    db.create_all()
    id = str(time.time())
    notes_object = Notes(id,gcm_id,title,tags,img_path)
    db.session.add(notes_object)
    db.session.commit()
    return "{'status':200,\n\t'response':'%s,%s'}"%(img_path,thumb_path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == '__main__':
    #print gen_white('1397959352_daft-punk.jpg')
    app.debug = True
    app.run(host='0.0.0.0',port=5002)

