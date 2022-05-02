from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
import json

from app import app
from utils.models import UserModel, CVModel
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum
from utils.validation import validation_request


schema = {
    "category": {'type': 'string', 'required': False, 'maxlength': 520},
    "skills": {
        'type': 'list',
        'required': False,
        'schema': {
            'type': 'dict',
            'required': False,
            'schema': {
                "grade": {
                    'type': 'integer',
                    'allowed': list(range(11)),
                    'required': True,
                },
                "name": {
                    'type': 'string',
                    'maxlength': 520,
                    'required': True,
                },
                "category": {
                    'type': 'string',
                    'maxlength': 520,
                    'required': True,
                }
            }
        }
    }
}


@app.route('/api/<api_version>/cv/create_cv', methods=['POST'])
@validation_request(schema=schema, with_token=True)
def create_cv(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])
    user: UserModel = UserModel.get_from_db(id_=payload['id'])

    skills = [
        CVModel.SkillModel(**skill)
        for skill in request_body.get('skills')
    ]
    cv = CVModel(
        user_id=user.id_,
        category=request_body.get('categories'),
        cv_skills=skills,
        cv_times=[]
    )
    cv.save()

    return {'msg': 'ok', 'inserted': cv.to_dict()}, 200
