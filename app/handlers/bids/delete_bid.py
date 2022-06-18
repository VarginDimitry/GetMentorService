import requests
from flask import request

from app import app
from utils import ErrorManager, ErrorEnum
from utils.MongoConnector import MongoConnector
from utils.models import UserModel
from utils.models.BidModel import BidModel, BidStatus
from utils.validation import validation_request


@app.route('/api/<api_version>/bids/delete_bid', methods=['DELETE'])
@validation_request(with_token=True)
def delete_bid(api_version):
    request_body: dict = request.args
    payload = UserModel.decode_token(request.headers['Authorization'])
    delete_res = BidModel.coll.delete_one({
        'id_': request_body.get('id_'),
        '$or': [
            {'from_id': payload['id']},
            {'to_id': payload['id']},
        ]
    })
    if delete_res.deleted_count:
        return {'msg': 'ok'}, 200
    else:
        return ErrorManager.get_res(
            ErrorEnum.NOT_FOUND,
            "The bid doesn't exists or you have no permissions for this bid"
        )
