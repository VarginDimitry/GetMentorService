import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.template_folder = os.path.join(os.getcwd(), 'app/template')
app.config.from_object('utils.configs.LocalConfig')

db = SQLAlchemy(app)
from app.models import *
migrate = Migrate(app, db)
