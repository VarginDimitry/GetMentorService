from flask import request

from app import app
from utils import ErrorManager, ErrorEnum
from utils.models import UserModel
from utils.models.BidModel import BidModel, BidStatus
from utils.validation import validation_request

schema = {
    'to_id': {'type': 'string', 'required': True},
    'description': {'type': 'string', 'required': False, 'maxlength': 2048, 'default': ""},
}


@app.route('/api/<api_version>/bids/send_bid', methods=['POST'])
@validation_request(with_token=True, schema=schema)
def send_bid(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])

    user: UserModel = UserModel.get_from_db(id_=payload['id'])
    if not user:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, f"User with id={payload['id']} not found")
    to_user: UserModel = UserModel.get_from_db(id_=request_body['to_id'])
    if not to_user:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, f"User with id={request_body['to_id']} not found")

    bid = BidModel(
        from_id=user.id_,
        from_name=user.first_name,
        to_id=to_user.id_,
        to_name=to_user.first_name,
        status=BidStatus.NOT_SEEN,
        description=request_body['description'],
    )
    save_res = bid.save()
    if 'error' not in save_res.keys():
        return {'msg': 'ok', 'bid': bid.to_dict()}, 200
    else:
        return ErrorManager.get_res(ErrorEnum.CONFLICT, f"Bid with this users already exists")
