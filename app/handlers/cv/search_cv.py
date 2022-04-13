from pprint import pprint
from typing import List, Dict

import sqlalchemy
from flask import request, make_response, jsonify
import flask_sqlalchemy
from sqlalchemy import text, func
from sqlalchemy.exc import IntegrityError
import json

from app import app, db
from app.models import UserModel, CVModel, CVSkillModel, CVTimeModel
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum, SortType, CVSortRow
from utils.validation import validation_request


@app.route('/api/<api_version>/cv/search_cv', methods=['GET'])
@validation_request(with_token=True)
def search_cv(api_version):
    skill_joined = False
    request_body: dict = request.json
    payload = UserModel.decode_token(request.headers['Authorization'])
    user: UserModel = UserModel.query.get(payload['id'])

    if CVSortRow(request_body.get('sort_by', {}).get('row')) == CVSortRow.SKILL_NUM:
        query = db.session.query(
            CVModel,
            func.count(CVSkillModel.id)
                .label(CVSortRow.SKILL_NUM.value)
        ).join(CVSkillModel).group_by(CVModel)
        skill_joined = True
    else:
        query = db.session.query(CVModel)
    query, skill_joined = get_sort_by(query, skill_joined)

    req_filters = request_body.get('filters', {})
    filters = {
        "skill_category": req_filters.get('skill_category'),
        "skill_name": req_filters.get('skill_name'),
        'skill_grade': req_filters.get('skill_grade'),
    }
    print(query)
    print()
    cvs: List[sqlalchemy.engine.row.Row] = query.all()
    return {
        'cvs': [{"cv": cv.to_dict, "skill_count": skill_count} for cv, skill_count in cvs]
    }

def get_sort_by(query, skill_joined):
    request_body: dict = request.json
    sort_by: dict = request_body.get('sort_by', {})

    row = CVSortRow(sort_by.get('row'))
    order = SortType(sort_by.get('order'))

    res = CVModel.dateTimeAdd
    if row == CVSortRow.CLICK_COUNT:
        res = CVModel.click_count
    elif row == CVSortRow.SKILL_NUM:
        res = CVSortRow.SKILL_NUM
    elif row == CVSortRow.DATE_TIME_ADD:
        res = CVModel.dateTimeAdd
    res = text(f"{res.value} {order.value}")

    return query.order_by(res), skill_joined
