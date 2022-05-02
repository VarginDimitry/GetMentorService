from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app
from utils import ErrorManager, ErrorEnum


@app.errorhandler(Exception)
def internal_server_error_handler(e: Exception):
    pprint(e)
    return ErrorManager.get_res(
        ErrorEnum.INTERNAL_SERVER_ERROR,
        e.args[0]
    )