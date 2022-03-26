from datetime import timedelta, datetime
from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app, db
from app.models.user import UserModel
from utils import ErrorManager

from utils.enums import GenderEnum, ErrorEnum, TokenType
from utils.validation import validation_request, validate_token


@app.route('/api/<api_version>/auth/refresh_token', methods=['GET'])
@validation_request(with_token=True)
def refresh_token(api_version):
    request_body: dict = request.json

    payload = UserModel.decode_token(request_body.get('refreshToken'))
    if 'error' not in payload:
        user: UserModel = UserModel.query.filter(
            UserModel.email == payload.get('email')
        ).first()
        return {
           'accessToken': user.encode_token(TokenType.ACCESS),
           'accessExp': (datetime.utcnow() + timedelta(
               minutes=app.config.get('ACCESS_TOKEN_LIFE'))).timestamp().__int__(),
           'refreshToken': user.encode_token(TokenType.REFRESH),
           'refreshExp': (datetime.utcnow() + timedelta(
               minutes=app.config.get('REFRESH_TOKEN_LIFE'))).timestamp().__int__(),
       }, 200
    else:
        return ErrorManager.get_res(ErrorEnum.UNAUTHORIZED, msg='Refresh token is incorrect')
