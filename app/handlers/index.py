import time
from flask import render_template

from app import app


@app.route('/api/time', methods=['GET'])
def get_time():
    return {'time': time.time()}
