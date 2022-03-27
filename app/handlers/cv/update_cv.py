from pprint import pprint
from typing import List, Dict

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app, db
from app.models import UserModel, CVModel, CVSkillModel, CVTimeModel
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum
from utils.validation import validation_request


@app.route('/api/<api_version>/cv/update_cv', methods=['PATCH'])
@validation_request(with_token=True)
def update_cv(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])
    user: UserModel = UserModel.query.get(payload['id'])
    cv: CVModel = CVModel.query.filter(
        CVModel.id == request_body.get('cv_id'), CVModel.user_id == user.id,
    ).first()
    if not cv:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, "CV has not found")

    skills: dict = request_body.get('skills')

    skills_to_delete: List[int] = skills.get('delete')
    if skills_to_delete:
        CVSkillModel.query.filter(
            CVSkillModel.id.in_(skills_to_delete), CVSkillModel.cv_id == cv.id
        ).delete()

    skills_to_update: Dict[str, dict] = skills.get('update')
    if skills_to_update:
        for skill in cv.cv_skills:
            skill: CVSkillModel
            if str(skill.id) in skills_to_update.keys():
                skill_from_req: Dict = skills_to_update.get(str(skill.id))
                skill.update(
                    name=skill_from_req.get('name'),
                    category=skill_from_req.get('category'),
                    grade=skill_from_req.get('grade'),
                )
        db.session.bulk_save_objects(cv.cv_skills)
    if skills.get('add'):
        new_skills = [
            CVSkillModel(
                cv_id=cv.id,
                grade=skill.get('grade'),
                name=skill.get('name'),
                category=skill.get('category')
            )
            for skill in skills.get('add')
        ]
        db.session.bulk_save_objects(new_skills)

    db.session.commit()
    return {'msg': 'ok'}, 200
