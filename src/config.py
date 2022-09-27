import os

HOST = "0.0.0.0"
PORT = 5000

# INPUT_PATH = "./../datasets/"
BASEPATH = os.path.dirname(os.path.realpath(__file__))
MODELPATH = os.path.join(BASEPATH, 'models/')
UPLOAD = os.path.join(BASEPATH, 'uploads/')
ALLOWED_EXTENSIONS = (['png','jpg','jpeg'])