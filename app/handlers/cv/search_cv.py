from pprint import pprint
from typing import List, Dict

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
import json

from app import app, db
from app.models import UserModel, CVModel, CVSkillModel, CVTimeModel
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum
from utils.validation import validation_request


@app.route('/api/<api_version>/cv/search_cv', methods=['GET'])
@validation_request(with_token=True)
def search_cv(api_version):
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])
    user: UserModel = UserModel.query.get(payload['id'])

    sort_by: Dict = get_sort_by()
    req_filters = request_body.get('filters', {})
    filters = {
        "skill_category": req_filters.get('skill_category'),
        "skill_name": req_filters.get('skill_name'),
        'skill_grade': req_filters.get('skill_grade'),
    }


    return {
        'cvs': []
    }

def get_sort_by():
    request_body: dict = request.json
    sort_by: dict = request_body.get('sort_by', {})
    sort_by['row'] = 'click_count' if sort_by['row'] is None else sort_by['row']
    sort_by['order'] = 'ASC' if sort_by['order'] is None else sort_by['order']
    return sort_by
