from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app, db
from app.models.user import UserModel
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum


@app.route('/api/<api_version>/auth/registration', methods=['POST'])
def registration(api_version):
    request_body: dict = request.json
    try:
        new_user = UserModel(
            # must have
            first_name=request_body.get('first_name'),
            last_name=request_body.get('last_name'),
            gender=GenderEnum(request_body.get('gender', 'M')),

            # SUPER MUST HAVE
            email=request_body.get('email'),
            password=request_body.get('password'),

            # optional
            phone=request_body.get('phone'),
            telegram_profile=request_body.get('telegram_profile'),
            middle_name=request_body.get('middle_name'),
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'msg': 'ok', 'inserted': new_user.to_json_res}), 200
    except IntegrityError as ex:
        pprint(ex.params)
        return ErrorManager.get_res(ErrorEnum.CONFLICT, msg="User with this email already exists")
