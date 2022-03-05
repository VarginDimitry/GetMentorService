import os

from flask import Flask

app = Flask(__name__)
app.template_folder = os.path.join(os.getcwd(), 'app/template')
