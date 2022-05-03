from flask import request

from app import app
from utils import ErrorManager, ErrorEnum
from utils.models import UserModel, CVModel
from utils.validation import validation_request

schema = {
    "cv_id": {'type': 'string', 'required': False, 'maxlength': 37},
}


@app.route('/api/<api_version>/cv/delete_cv', methods=['DELETE'])
@validation_request(schema=schema, with_token=True)
def delete_cv(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])

    deleted_count = CVModel.coll.delete_one({
        'id_': request_body.get('cv_id'),
        'user_id': payload['id'],
    }).deleted_count

    if deleted_count == 0:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, 'This cv doesn\'t exist')
    else:
        return {'msg': 'ok'}, 200
