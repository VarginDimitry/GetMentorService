from datetime import datetime

from flask import request

from app import app
from utils import ErrorManager, ErrorEnum
from utils.models import UserModel
from utils.models.BidModel import BidModel, BidStatus
from utils.validation import validation_request

schema = {
    'to_id': {'type': 'string', 'required': True},
    'description': {'type': 'string', 'required': False, 'maxlength': 2048, 'default': ""},
    'date_time': {'type': 'number', 'required': False, 'min': 0, 'max': 14277919609}
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
    elif user.id_ == to_user.id_:
        return ErrorManager.get_res(ErrorEnum.CONFLICT, f"Can not send bid to self")
    bid = BidModel(
        from_id=user.id_,
        from_name=f"{user.first_name} {user.last_name}",
        to_id=to_user.id_,
        to_name=f"{to_user.first_name} {user.last_name}",
        status=BidStatus.NOT_SEEN,
        description=request_body['description'],
        date_time=datetime.fromtimestamp(int(request_body['date_time'])) if request_body['date_time'] else None,
    )
    save_res = bid.save()
    if 'error' not in save_res.keys():
        return {'msg': 'ok', 'bid': bid.to_dict()}, 200
    else:
        return ErrorManager.get_res(ErrorEnum.CONFLICT, f"Bid with this users already exists")
