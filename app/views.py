from __future__ import absolute_import
from flask import render_template,request,redirect,url_for
import os
from .recommender_system import recommender_system_questions

import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# upload_path = 'static/uploads' 

def index():
    return render_template('index.html')
def base():
    return render_template('base.html') 
def recommender_system():
    if request.method == 'POST':
       pro_id = request.form['pro_id']
       time1 = request.form['from_day']
       time2 = request.form['to_day']
       print(pro_id,time1)
       return render_template('recommender_system.html',submited=True,pro_id=pro_id,time1=time1,time2=time2)       
    return render_template('recommender_system.html',submited=False)       