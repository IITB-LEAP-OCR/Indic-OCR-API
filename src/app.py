#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import uuid
import shutil
import sqlite3
from utils import *
from config import *
import logging as lg
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify

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
def index():
    return "Running"
           
@app.route('/api/v0/upload',methods=['GET', 'POST'])
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
                filename_ext = filename.split('.')[-1]
                file_id = str(uuid.uuid4())
                total_ids.append(file_id)
                filename_new = f"img_{file_id}" + "." + filename_ext
                isExist = os.path.exists(upload)
                if not isExist:
                    os.makedirs(upload)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_new))
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename_new)
                conn = get_db_connection()
                posts = conn.execute("INSERT INTO request (file_path, file_id) VALUES (?, ?)",(path, file_id)).fetchall()
                conn.commit()
                conn.close()            
        return jsonify({'data': {'ids':total_ids}})
    elif request.method =="GET":
        return ("Error GET Not Configured")

@app.route('/api/v0/inference',methods=['GET', 'POST'])
def perform_inference():
    if request.method =="POST":
        json_data = request.get_json()
        folder_list = os.listdir(upload)
        for folder in folder_list:
            if folder.endswith(".jpeg") or folder.endswith(".jpg") or folder.endswith(".png") or folder.endswith(".DS_Store"):
                folder_list.remove(folder)
        if len(folder_list) == 0:
            os.mkdir(upload + "/1")
            batch_folder = upload + "/1"
        else:
            os.mkdir(upload + "/" + str(len(folder_list)+1))
            batch_folder = upload + "/" + str(len(folder_list)+1)
        for data in json_data:
            id = data['id']
            conn = get_db_connection()
            posts = conn.execute('SELECT file_path FROM request WHERE file_id=?',(id,)).fetchall()
            file_path = posts[0]['file_path']
            data['file_path']=file_path
            filename_name = file_path.split('/')
            shutil.move(file_path,batch_folder + "/" + filename_name[-1])
            
        result = infer_model(data["language"], data["modality"], MODEL_PATH, batch_folder, data["meta"]["device"])
        for data in json_data:
            for key in result.keys():
                img_name1 = "img_" + key.split('/')[-1]
                img_name2 = data['file_path'].split('/')[-1]
                if img_name1 == img_name2:
                    data["text"] = result[key]
        return jsonify({"data":json_data,"text":result})

if __name__ == '__main__':
	# when first starting the app from docker, we load the model into memory
	# and then start the flask app
	app.run(debug=False, host=HOST, port=PORT, use_reloader=False)