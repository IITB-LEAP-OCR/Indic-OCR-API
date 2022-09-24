# -*- coding:utf-8 -*-
import os
import uuid
import sqlite3
from utils import *
from config import *
import logging as lg
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template

#logging basic configuration
lg.basicConfig(filename="log.txt",level=lg.DEBUG)

app = Flask(__name__, template_folder='template')
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = upload

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/',methods=['GET', 'POST'])
def hello_world():
    return "Hello World"
           
@app.route('/v0/upload',methods=['GET', 'POST'])
def perform_upload():
    if request.method =="POST":
        if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
        files = request.files.getlist("file")
        for file in files:
            if file.filename == '':
                resp = jsonify({'message' : 'No file selected for uploading'})
                resp.status_code = 400
                return resp
            total_ids = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename_ext = filename.split('.')[1]
                file_id = str(uuid.uuid4())
                total_ids.append(file_id)
                filename_new = f"img_{file_id}" + "." + filename_ext
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_new))
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename_new)
                conn = get_db_connection()
                posts = conn.execute("INSERT INTO request (file_path, file_id) VALUES (?, ?)",(path, file_id)).fetchall()
                conn.commit()
                conn.close()            
        return jsonify({'data': {'ids':total_ids}})
    elif request.method =="GET":
        return ("Error GET Not Configured")

@app.route('/v0/interference',methods=['GET', 'POST'])
def perform_inference():
    if request.method =="POST":
        main_context = []
        json_data = request.get_json()
        for data in json_data:
            id = data['id']
            conn = get_db_connection()
            posts = conn.execute('SELECT file_path FROM request WHERE file_id=?',(id,)).fetchall()
            file_path = posts[0]['file_path']
            data['file_path']=file_path
            #result = infer_model(data["language"], data["modality"], MODEL_PATH, file_path, data["meta"]["device"])
            result = ""
            context = {"text":result}
            context.update(data)
            main_context.append(context.copy())
        return jsonify({"data":main_context})

if __name__ == '__main__':
	# when first starting the app from docker, we load the model into memory
	# and then start the flask app
	app.run(debug=True, host=HOST, port=PORT, use_reloader=True)