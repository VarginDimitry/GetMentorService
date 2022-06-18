from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
import json

from app import app

from utils.enums import GenderEnum
from utils.models import UserModel


@app.route('/api/<api_version>/users/get_users', methods=['GET', 'POST'])
def users_get_users(api_version: str):
    if request.method == 'GET':
        if request.args.get('user_id'):
            user_id = int(request.args.get('user_id'))
            user: UserModel = UserModel.get_from_db(id_=request.args.get('user_id'))

            return {
                'user': user.to_dict(safe=True)
            }, 200
        else:
            users: List[UserModel] = list(UserModel.conn.user.find({}))
            for user in users:
                user.pop('_id', None)
            return jsonify(users), 200
    # else:
    #     new_user_json: dict = request.json
    #     pprint(new_user_json)
    #     new_user = UserModel(
    #         first_name=new_user_json.get('first_name'),
    #         last_name=new_user_json.get('last_name'),
    #         gender=GenderEnum(new_user_json.get('gender')),
    #         email=new_user_json.get('email'),
    #         password=new_user_json.get('password'),
    #
    #     )
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return jsonify({'msg': 'ok', 'inserted': new_user.to_dict()})
