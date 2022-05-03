from datetime import timedelta, datetime

from flask import request

from app import app
from utils import ErrorManager
from utils.enums import ErrorEnum, TokenType
from utils.models import UserModel
from utils.validation import validation_request

schema = {
    'refreshToken': {'type': 'string', 'required': False, 'maxlength': 520}
}


@app.route('/api/<api_version>/auth/refresh_token', methods=['GET'])
@validation_request(schema=schema, with_token=True)
def refresh_token(api_version):
    request_body: dict = request.json

    payload = UserModel.decode_token(request_body.get('refreshToken'))
    if 'error' not in payload:
        user: UserModel = UserModel.get_from_db(
            email=payload.get('email')
        )
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
