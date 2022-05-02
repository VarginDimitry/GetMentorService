from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum
from utils.models import UserModel
from utils import schemas
from utils.validation import validation_request

schema = {
    "first_name": {'type': 'string', 'required': True, 'maxlength': 128},
    "last_name": {'type': 'string', 'required': True, 'maxlength': 128},
    "gender": {'type': 'string', 'allowed': ['M', 'F'], 'required': False},

    "email": schemas.email_schema,
    "password": schemas.password_schema,

    "phone": schemas.phone_schema,
    "telegram_profile": {
        'type': 'string',
        'regex': r'.*\B@(?=\w{5,32}\b)[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*.*',
        'required': False,
        'maxlength': 128
    },
    "middle_name": {'type': 'string', 'required': False, 'maxlength': 128}
}


@app.route('/api/<api_version>/auth/registration', methods=['POST'])
@validation_request(schema=schema, with_token=False)
def registration(api_version):
    request_body: dict = request.json
    user = UserModel.get_from_dict(request_body)
    res = user.save()
    return user.to_dict() \
        if res.get('error') else\
        ErrorManager.get_res(ErrorEnum.CONFLICT, msg=res['error'])