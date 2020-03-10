from flask import Flask, flash, request, redirect, url_for
from flask_cors import CORS
from flask_pusher import Pusher
from werkzeug.utils import secure_filename
from contextlib import redirect_stdout

import subprocess
import os



app_id = "960906"
key = "d18ed2e42cf337876806"
secret = "ffd3ef254ef8617ab31a"
cluster = "us2"

app = Flask(__name__)
pusher = Pusher(app, secret = secret, app_id = app_id, key = key, cluster = cluster)


app.secret_key = 'secret key'
CORS(app)

UPLOAD_FOLDER = './data_upload'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def build_data(data_file_path):
    
    subprocess.run(['python3', './data-parsing/data_util.py', data_file_path])


# def train_model(data_folder_path = "./"):

#     subprocess.run(['python3', 'question_answering/run_all.py', data_file_path])


@app.route('/upload', methods=['POST'])
def upload_file():

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file in request')
        return 'No file in request'

    file = request.files['file']
 
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        pusher.trigger('pipeline', 'progress', {'message':'File uploaded'}) # trigger `some-event` event on `progress` channel


        build_data(file_path)
        print('File uploaded')
        return 'File uploaded'

    print('Reach end error')
    return 'Reach end error'
