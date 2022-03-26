from flask import Flask, render_template
from app import app, db
from app.handlers import *
from utils import ErrorManager


def main():
    ErrorManager.init_class()


if __name__ == '__main__':
    main()
    app.run(debug=True)
