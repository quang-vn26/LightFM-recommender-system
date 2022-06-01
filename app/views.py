from __future__ import absolute_import
from flask import render_template,request,redirect,url_for
import os
from .recommender_system import recommender_system_questions
import datetime
import csv
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
       print(pro_id,time1,time2)
       string_time = ""
       string_time = str(time1)+" to "+str(time2)


       if(time1=="" or time2==""):
            results = []
            rs_file_name = "module/display_csv.csv"
            with open(rs_file_name) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    results.append(dict(row))
                fieldnames = [key for key in results[0].keys()]    
            return render_template('recommender_system.html',submited=True,pro_id=pro_id,string_time="No valid time range",results=results, fieldnames=fieldnames,len=len)       
       return render_template('recommender_system.html',submited=True,pro_id=pro_id,string_time=string_time)       
    return render_template('recommender_system.html',submited=False)       