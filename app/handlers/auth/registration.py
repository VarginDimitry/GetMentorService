from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum
from utils.models import UserModel


@app.route('/api/<api_version>/auth/registration', methods=['POST'])
def registration(api_version):
    request_body: dict = request.json
    user = UserModel.get_from_dict(request_body)
    res = user.save()
    return user.to_dict() if 'error' not in res else ErrorManager.get_res(ErrorEnum.BAD_REQUEST, msg=res['error'])

