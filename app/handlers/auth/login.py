from datetime import datetime, timedelta
from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app, db
from app.models.user import UserModel

from utils.enums import GenderEnum, TokenType
from utils.ErrorManager import ErrorEnum, ErrorManager


@app.route('/api/<api_version>/auth/login', methods=['GET', 'POST'])
def login(api_version):
    request_body: dict = request.json
    user: UserModel = UserModel.query.filter(
        UserModel.email == request_body.get('email')
    ).first()
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
