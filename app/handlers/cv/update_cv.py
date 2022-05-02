from pprint import pprint
from typing import List, Dict

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app
from utils.models import UserModel, CVModel
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum
from utils.validation import validation_request


@app.route('/api/<api_version>/cv/update_cv', methods=['PATCH'])
@validation_request(with_token=True)
def update_cv(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])
    user: UserModel = UserModel.get_from_db(payload['id'])
    cv: CVModel = CVModel.get_from_db(
        id_=request_body.get('cv_id'),
        user_id=payload['id'],
    )
    if not cv:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, "CV has not found")

    cv.update(
        category=request_body.get('categories'),
        cv_skills=request_body.get('cv_skills', [])
    )

    return {'msg': 'ok', 'cv': cv.to_dict()}, 200
