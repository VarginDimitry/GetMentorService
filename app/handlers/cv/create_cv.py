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


@app.route('/api/<api_version>/cv/create_cv', methods=['POST'])
@validation_request(with_token=True)
def create_cv(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])
    user: UserModel = UserModel.query.get(payload['id'])

    cv = CVModel(user_id=user.id)
    db.session.add(cv)
    db.session.commit()

    skills = [
        CVSkillModel(
            cv_id=cv.id,
            grade=skill.get('grade', 0),
            name=skill.get('name'),
            category=skill.get('category')
        )
        for skill in request_body.get('skills')
    ]

    db.session.bulk_save_objects(skills)
    db.session.commit()

    return {'msg': 'ok', 'inserted': cv.to_dict}, 200
