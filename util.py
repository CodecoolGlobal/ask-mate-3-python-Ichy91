import bcrypt
from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret'


def upload_file(my_request, picture_id, QandA):
    if 'image' in my_request.files:
        file = my_request.files['image']
        filename = secure_filename(file.filename)
        filepath = "/" + UPLOAD_FOLDER + "/" + QandA + str(picture_id) + secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], QandA + str(picture_id) + filename))

        return filepath


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)