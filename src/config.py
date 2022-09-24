MODEL_PATH = "./../models/recognition/handwritten/"
INPUT_PATH = "./../datasets/"

HOST = "0.0.0.0"
PORT = 5000

import os

basepath = os.path.dirname(os.path.realpath(__file__))

modelpath = os.path.join(basepath, 'models')

upload = os.path.join(basepath, 'uploads')

ALLOWED_EXTENSIONS = (['png','jpg','jpeg'])