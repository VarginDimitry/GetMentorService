import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.template_folder = os.path.join(os.getcwd(), 'app/template')
app.config.from_object('utils.configs.DockerConfig')
