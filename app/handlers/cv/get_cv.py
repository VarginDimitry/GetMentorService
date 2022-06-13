from flask import request, jsonify

from app import app
from utils import ErrorManager, ErrorEnum
from utils.models import UserModel, CVModel
from utils.validation import validation_request


@app.route('/api/<api_version>/cv/get_cv/', methods=['GET'])
@validation_request(with_token=True)
def get_cv(api_version: str):
    payload = UserModel.decode_token(request.headers['Authorization'])
    cv_id = request.args['cv_id']

    cv = CVModel.get_from_db(
        id_=cv_id,
        user_id=payload['id']
    )
    if not cv:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, "CV with this id not found")
    user = UserModel.get_from_db(id_=cv.user_id)
    if not user:
        return ErrorManager.get_res(ErrorEnum.CONFLICT, "CV is invalid")
    user_dict: dict = user.to_dict()
    user_dict.pop('password', None)
    return jsonify({
        'user': user_dict,
        'cv': cv.to_dict(),
    })
