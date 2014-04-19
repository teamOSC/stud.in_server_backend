#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, send_from_directory

from werkzeug import secure_filename

import json
import sqlite3
import os

app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#to initialize db on first run
def db_init():
    db = sqlite3.connect('data/main.db',timeout=10)
    cursor = db.cursor()

    try:
        cursor.execute('DROP TABLE users;')
        print 'Dropped table users'
    except:
        pass
    
    cursor.execute('''
        CREATE TABLE users(gcm_id TEXT PRIMARY KEY, name TEXT,email TEXT,
                           tag_line TEXT, address TEXT,dob TEXT 
                           ins_type TEXT, ins_name TEXT,subjects TEXT )
    ''')
    print 'Created new table users'
    db.close()

@app.route('/add')
def add_user():
    db = sqlite3.connect('data/main.db',timeout=10)
    cursor = db.cursor()

    try:
        gcm_id = request.args.get('gcm_id ') or '3'
        name = request.args.get('name') or ''
        email = request.args.get('email') or 'aaasd'
        tag_line = request.args.get('tag_line') or ''
        address = request.args.get('address') or ''
        dob = request.args.get('dob') or ''
        ins_type = request.args.get('ins_type') or ''
        ins_name = request.args.get('ins_name') or ''
        subjects = request.args.get('subjects') or ''

    except:
        return '{"status":400,\n\t"response":"one or more parameters is/are missing"}'
    
    cursor.execute('INSERT INTO users VALUES(?,?,?,?,?,?,?,?)', (gcm_id,name,email,tag_line,address,dob,ins_type,ins_name))
    
    db.commit()
    return "{'status':200,\n\t'response':'User has been added'}"

@app.route('/view_all')
def view_all():
    db = sqlite3.connect('data/main.db',timeout=10)
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM users''')
    return json.dumps( cursor.fetchall() )


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/test')
def upload_test():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return '<img src="/uploads/%s">'%filename
        return redirect(url_for('uploaded_file',
                                filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    #db_init()
    app.debug = True
    app.run(host='0.0.0.0')
