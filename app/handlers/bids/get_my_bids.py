from flask import request

from app import app
from utils import ErrorManager, ErrorEnum
from utils.models import UserModel
from utils.models.BidModel import BidModel, BidStatus
from utils.validation import validation_request


@app.route('/api/<api_version>/bids/get_my_bids', methods=['GET'])
@validation_request(with_token=True)
def get_my_bids(api_version):
    payload = UserModel.decode_token(request.headers['Authorization'])
    return{
        "msg": "ok",
        "bids": BidModel.get_all_by_to_id(payload['id'])
    }, 200
