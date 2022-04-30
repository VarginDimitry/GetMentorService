import time
from flask import render_template

from app import app


@app.route('/')
def index():
    return render_template('qwe.html')


@app.route('/time', methods=['GET'])
def get_time():
    return {'time': time.time()}
