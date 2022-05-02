from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
import json

from app import app
from utils.models import UserModel, CVModel
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum
from utils.validation import validation_request


@app.route('/api/<api_version>/cv/create_cv', methods=['POST'])
@validation_request(with_token=True)
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
