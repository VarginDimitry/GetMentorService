from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app, db
from app.models.user import UserModel
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum
from utils.validation import validation_request


@app.route('/api/<api_version>/user/get_me', methods=['GET'])
@validation_request(with_token=True)
def get_me(api_version):
    payload = UserModel.decode_token(request.headers['Authorization'])
    user: UserModel = UserModel.query.get(payload['id'])
    return {'user': user.to_json_res}, 200
