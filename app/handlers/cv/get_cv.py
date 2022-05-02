from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app
from utils.models import UserModel, CVModel
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum
from utils.validation import validation_request


@app.route('/api/<api_version>/cv/get_cv/<cv_id>', methods=['GET'])
@validation_request(with_token=True)
def get_cv(api_version: str, cv_id: str):
    payload = UserModel.decode_token(request.headers['Authorization'])

    cv = CVModel.get_from_db(
        id_=cv_id,
        user_id=payload['id']
    )
    if not cv:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, "CV with this id not found")
    user = UserModel.get_from_db(id_=cv.user_id)
    if not user:
        return ErrorManager.get_res(ErrorEnum.CONFLICT, "CV is invalid")
    return jsonify({
        'user': user.to_dict(),
        'cv': cv.to_dict(),
    })
