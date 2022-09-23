import os
import json

from utils import *
from config import *

from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='template')
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/v1/upload')
def upload_ui():
    return render_template('upload.html')

@app.route('/v1/upload', methods=['POST'])
def my_form_post():
    data = request.form
    processed_text = infer_model(data["language"], data["modality"], MODEL_PATH, data["input_path"], data["device"])
    return jsonify(processed_text)

# ------------upload-file-----------------------------------------#
@app.route('/v0/upload', methods=['POST'])
def receave_file():
    if request.method == 'POST':
        print("POST request stored.")
        print(log("Started Infering..."))
        data = request.get_json()
        result = infer_model(data["language"], data["modality"], MODEL_PATH, data["meta"]["input_path"], data["meta"]["device"])
        print(log("Completed Inference..."))
        with open("sample_results.json", "w") as outfile:
            json.dump(result, outfile)
        return jsonify(result)


@app.route('/v0/results', methods=['GET'])
def get_results():
    if(os.path.exists('./sample_results.json')):
        result = {}
        with open('sample_results.json', 'r') as openfile:
            result = json.load(openfile)
        os.remove('./sample_results.json')
        return jsonify(result)
    else:
        return(jsonify({"Post":"Post did not happened yet"}))



if __name__ == '__main__':
	# when first starting the app from docker, we load the model into memory
	# and then start the flask app
	app.run(debug=True, host=HOST, port=PORT, use_reloader=False)