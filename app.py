#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask, flask.views
app = flask.Flask(__name__)

from flask import render_template
from flask import request
import json
import sqlite3

def on_init():
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

@app.route('/')
def index():
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
    
    
    #cursor.execute('''INSERT INTO users(gcm_id,name,email,tag_line,address,dob,ins_type,ins_name,subjects)
    #                  VALUES(?,?,?,?,?,?,?,?,?)''', (gcm_id,name,email,tag_line,address,dob,ins_type,ins_name,subjects))
    
    db.commit()
    
    cursor.execute('''SELECT * FROM users''')
    return json.dumps( cursor.fetchall() )

    return "{'status':200,\n\t'response':'User has been added'}"
    
if __name__ == '__main__':
    #on_init()
    app.debug = True
    app.run(host='0.0.0.0')
