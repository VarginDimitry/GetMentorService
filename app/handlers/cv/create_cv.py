from flask import request

from app import app
from utils.models import UserModel, CVModel
from utils.validation import validation_request

schema = {
    "category": {'type': 'string', 'required': False, 'maxlength': 512},
    'job': {'type': 'string', 'required': False, 'maxlength': 512},
    'price': {'type': 'string', 'required': False, 'maxlength': 512},
    'experience': {'type': 'string', 'required': False, 'maxlength': 512},
    'about': {'type': 'string', 'required': False, 'maxlength': 2048},
    "skills": {
        'type': 'list',
        'required': False,
        'schema': {
            'type': 'dict',
            'required': False,
            'schema': {
                "grade": {
                    'allowed': ['bad', 'average', 'good'],  # list(range(11)),  # 0-10
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


@app.route('/api/<api_version>/cv/create_cv', methods=['POST'])
@validation_request(schema=schema, with_token=True)
def create_cv(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])
    user: UserModel = UserModel.get_from_db(id_=payload['id'])

    skills = [CVModel.SkillModel(**skill) for skill in request_body.get('skills')]
    cv = CVModel(
        user_id=user.id_,
        category=request_body.get('category'),
        cv_skills=skills,
        cv_times=[],
        experience=request_body.get('experience'),
        about=request_body.get('about'),
        price=request_body.get('price'),
        job=request_body.get('job'),
    )
    cv.save()

    return {
        'msg': 'ok',
        'inserted': cv.to_dict(),
        'user': user.to_dict(safe=True),
    }, 200
