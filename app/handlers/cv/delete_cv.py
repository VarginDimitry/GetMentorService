from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app, db
from app.models import UserModel, CVModel, CVSkillModel, CVTimeModel
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum
from utils.validation import validation_request


@app.route('/api/<api_version>/cv/delete_cv', methods=['DELETE'])
@validation_request(with_token=True)
def delete_cv(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])

    deleted_rows = CVModel.query.filter(
        CVModel.user_id == payload['id'], CVModel.id == request_body.get('cv_id')
    ).delete()
    db.session.commit()

    if deleted_rows == 0:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, 'This cv doesn\'t exist')
    else:
        return {'msg': 'ok'}, 200
