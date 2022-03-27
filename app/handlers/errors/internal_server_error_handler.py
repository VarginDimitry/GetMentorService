from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app, db
from utils import ErrorManager, ErrorEnum


@app.errorhandler(500)
def internal_server_error_handler(e):
    print(type(e))
    return ErrorManager.get_res(ErrorEnum.INTERNAL_SERVER_ERROR, )
