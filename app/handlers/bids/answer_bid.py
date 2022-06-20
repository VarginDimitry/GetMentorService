import requests
from flask import request

from app import app
from utils import ErrorManager, ErrorEnum
from utils.models import UserModel
from utils.models.BidModel import BidModel, BidStatus
from utils.validation import validation_request

schema = {
    'status': {'required': True, 'allowed': [BidStatus.ACCEPTED.value, BidStatus.REJECTED.value]},
    'bid_id': {'required': True, 'type': 'string'},
    'answer': {'required': False, 'type': 'string', 'maxlength': 2048}
}


@app.route('/api/<api_version>/bids/answer_bid', methods=['POST'])
@validation_request(with_token=True, schema=schema)
def answer_bid(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])
    bid = BidModel.get_from_db(request_body['bid_id'])
    if not bid or bid.to_id != payload['id']:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, f"User has not this bid")
    upd_res = bid.update({
        'status': request_body.get('status'),
        'answer': request_body.get('answer', ''),
    })
    if 'error' not in upd_res:
        to_user = UserModel.get_from_db(bid.to_id)
        if BidStatus(request_body.get('status')) == BidStatus.ACCEPTED:
            to_user.update({'help_count': to_user.help_count+1})
        return {
                   'msg': 'ok',
                   'bid': upd_res,
                   'from_user': UserModel.get_from_db(bid.from_id).to_dict(safe=True),
                   'to_user': to_user.to_dict(safe=True),
               }, 200
    else:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, f"Update error")
