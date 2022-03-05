from flask import Flask, render_template
from app import app
from app.handlers import *


if __name__ == '__main__':
    app.run(debug=True)
