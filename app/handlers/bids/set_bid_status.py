from flask import request

from app import app
from utils import ErrorManager, ErrorEnum
from utils.models import UserModel
from utils.models.BidModel import BidModel, BidStatus
from utils.validation import validation_request

schema = {
    'status': {'required': True, 'allowed': [BidStatus.ACCEPTED.value, BidStatus.REJECTED.value]},
    'bid_id': {'required': True, 'type': 'string'}
}


@app.route('/api/<api_version>/bids/set_bid_status', methods=['POST'])
@validation_request(with_token=True, schema=schema)
def set_bid_status(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])
    bid = BidModel.get_from_db(request_body['bid_id'])
    if not bid or bid.to_id != payload['id']:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, f"User has not this bid")
    upd_res = bid.update({'status': request_body.get('status')})
    if 'error' not in upd_res:
        return {'msg': 'ok', 'bid': upd_res}, 200
    else:
        return ErrorManager.get_res(ErrorEnum.NOT_FOUND, f"Update error")
