from flask import request

from app import app
from utils import ErrorManager, ErrorEnum
from utils import schemas
from utils.models import UserModel
from utils.validation import validation_request

schema = {
    "first_name": {'type': 'string', 'required': True, 'maxlength': 128},
    "last_name": {'type': 'string', 'required': True, 'maxlength': 128},
    "gender": {'type': 'string', 'allowed': ['M', 'F'], 'required': False},

    "email": schemas.email_schema,

    "phone": schemas.phone_schema,
    "telegram_profile": {
        'type': 'string',
        'regex': r'.*\B@(?=\w{5,32}\b)[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*.*',
        'required': False,
        'maxlength': 128
    },
    "middle_name": {'type': 'string', 'required': False, 'maxlength': 128}
}


@app.route('/api/<api_version>/user/update_me', methods=['POST'])
@validation_request(schema=schema, with_token=True)
def update_me(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])
    request_body['id_'] = payload['id']

    user = UserModel.get_from_db(request_body['id_'])
    res = user.update(request_body)
    return ErrorManager.get_res(ErrorEnum.CONFLICT, msg=res['error'])\
        if res.get('error') else\
        user.to_dict()
