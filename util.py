#Implement sorting for the question list.
#The question list can be sorted by title, submission time, message, number of views, and number of votes
#You can choose the direction: ascending or descending
#The order is passed as query string parameters, for example /list?order_by=title&order_direction=desc

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


