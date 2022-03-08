import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.template_folder = os.path.join(os.getcwd(), 'app/template')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:qwe321@localhost:5432/gms"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
from app.models import *
migrate = Migrate(app, db)
