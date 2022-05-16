import argparse
import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import logging.config as logging_config


logging_config.dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.template_folder = os.path.join(os.getcwd(), 'app/template')
