import functools
from pprint import pprint

from cerberus import Validator
from flask import request

from utils.models import UserModel
from utils import ErrorManager, ErrorEnum

validator: Validator = Validator()


def validation_request(schema=None, with_token=False):
    def inner(func):
        def wrapper(*args, **kwargs):
            if with_token and not validate_token():
                return ErrorManager.get_res(ErrorEnum.UNAUTHORIZED, msg=f"Your access token is incorrect")
            if schema is not None:
                if validator.validate(request.json, schema):
                    return func(*args, **kwargs)
                else:
                    return ErrorManager.get_res(ErrorEnum.BAD_REQUEST, msg=validator.errors)
            else:
                return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    return inner


def validate_token() -> bool:
    return 'error' not in UserModel.decode_token(request.headers.get('Authorization')).keys()
