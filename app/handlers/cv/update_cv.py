from flask import request

from app import app
from utils import ErrorManager, ErrorEnum
from utils.models import UserModel, CVModel
from utils.validation import validation_request

schema = {
    "cv_id": {'type': 'string', 'required': False, 'maxlength': 37},
    'job': {'type': 'string', 'required': False, 'maxlength': 512},
    'price': {'type': 'string', 'required': False, 'maxlength': 512},
    'experience': {'type': 'string', 'required': False, 'maxlength': 512},
    'about': {'type': 'string', 'required': False, 'maxlength': 2048},
    "category": {'type': 'string', 'required': False, 'maxlength': 520},
    "skills": {
        'type': 'list',
        'required': False,
        'schema': {
            'type': 'dict',
            'required': False,
            'schema': {
                "grade": {
                    'allowed': ['bad', 'average', 'good'],
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
                    'required': False,
                }
            }
        }
    }
}


@app.route('/api/<api_version>/cv/update_cv', methods=['PATCH'])
@validation_request(schema=schema, with_token=True)
def update_cv(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])
    user: UserModel = UserModel.get_from_db(payload['id'])
    cv: CVModel = CVModel.get_from_db(id_=request_body.get('cv_id'))
    if not cv or user.id_ != cv.user_id:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, "CV has not found")

    cv.update(
        category=request_body.get('category'),
        cv_skills=request_body.get('cv_skills', []),
        experience=request_body.get('experience'),
        about=request_body.get('about'),
        price=request_body.get('price'),
        job=request_body.get('job'),
    )

    return {'msg': 'ok', 'cv': cv.to_dict()}, 200
