from datetime import datetime, timedelta
from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
import json

from app import app
from utils.models import UserModel

from utils.enums import GenderEnum, TokenType
from utils.ErrorManager import ErrorEnum, ErrorManager
from utils import schemas
from utils.validation import validation_request


schema = {
    'email': schemas.email_schema,
    'password': schemas.password_schema,
}

@app.route('/api/<api_version>/auth/login', methods=['GET', 'POST'])
@validation_request(schema=schema, with_token=False)
def login(api_version):
    request_body: dict = request.json
    find_by = {
        'id_': request_body.get('id_'),
        'email': request_body.get('email'),
    }
    user: UserModel = UserModel.get_from_db(**find_by)
    if user:
        if user.assert_password(request_body.get('password')):
            return {
                'accessToken': user.encode_token(TokenType.ACCESS),
                'accessExp': (datetime.utcnow() + timedelta(minutes=app.config.get('ACCESS_TOKEN_LIFE'))).timestamp().__int__(),
                'refreshToken': user.encode_token(TokenType.REFRESH),
                'refreshExp': (datetime.utcnow() + timedelta(minutes=app.config.get('REFRESH_TOKEN_LIFE'))).timestamp().__int__(),
            }, 200
        else:
            return ErrorManager.get_res(ErrorEnum.BAD_REQUEST, msg='Password is incorrect')
    else:
        return ErrorManager.get_res(ErrorEnum.BAD_REQUEST, msg="User doesn't exist")
