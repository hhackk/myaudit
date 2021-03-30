#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta
from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists
from sqlalchemy.sql import func
from sqlalchemy.orm.exc import MultipleResultsFound
import csv
import os
from flask_cors import CORS

app = Flask(__name__,
            static_url_path='',
            static_folder='static')
app.config.from_pyfile("config.cfg")
db = SQLAlchemy(app)
CORS(app, supports_credentials=True)

class Match_Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(1024))
    line = db.Column(db.String(256))
    linenum = db.Column(db.Integer)
    hightligth_key = db.Column(db.String(1024))
    hightligth_offset = db.Column(db.Integer)
    hightligth_length = db.Column(db.Integer)

@app.route("/init")
def init_db():
    db.drop_all()
    db.create_all()
    
    item1 = Match_Item(path='/opt/gcf/Main.java',
                                         line='xxx',
                                         linenum=10,
                                         hightligth_key = 'xx',
                                         hightligth_offset = 1,
                                         hightligth_length = 5)
    db.session.add(item1)
    db.session.commit()
    return 'ok'

@app.route("/api/result_ids")
def get_result_ids():
    return jsonify({'total':2, 'result_ids': [1, 2]})  

@app.route("/api/resultsbyids")
def get_resultsbyids():
    match_items = Match_Item.query.all()
    items_view = []
    for item in match_items:
        items_view.append({'id':item.id, 'path':item.path, 'line':item.line})
    return jsonify(items_view)

@app.route('/')
def root():
    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
