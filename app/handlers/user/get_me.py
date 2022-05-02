from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app
from utils.models import UserModel
from utils import ErrorManager, ErrorEnum

from utils.validation import validation_request


@app.route('/api/<api_version>/user/get_me', methods=['GET'])
@validation_request(with_token=True)
def get_me(api_version):
    payload = UserModel.decode_token(request.headers['Authorization'])
    user: UserModel = UserModel.get_from_db(id_=payload['id'])
    if user:
        return {'user': user.to_dict(with_cvs=True)}, 200
    else:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, "")
