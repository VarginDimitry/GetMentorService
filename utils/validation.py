import functools
from pprint import pprint

from flask import request

from app import UserModel
from utils import ErrorManager, ErrorEnum


def validation_request(schema=None, with_token=False):
    def inner(func):
        def wrapper(*args, **kwargs):
            if with_token and not validate_token():
                return ErrorManager.get_res(ErrorEnum.UNAUTHORIZED, msg=f"Your access token is incorrect")
            if schema:
                validation = schema()
                if validation['ok']:
                    return func(*args, **kwargs)
                else:
                    return ErrorManager.get_res(ErrorEnum.BAD_REQUEST, msg=validation['msg'])
            else:
                return func(*args, **kwargs)

        return wrapper
    return inner


def validate_token() -> bool:
    return 'error' not in UserModel.decode_token(request.headers.get('Authorization')).keys()
