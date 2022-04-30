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
@validation_request(with_token=False)
def search_cv(api_version):
    request_body: dict = request.json
    # payload = UserModel.decode_token(request.headers['Authorization'])
    # user: UserModel = UserModel.query.get(payload['id'])

    skill_count_label = func.count(CVSkillModel.id).label(CVSortRow.SKILL_NUM.value)
    print(skill_count_label, type(skill_count_label))
    query: flask_sqlalchemy.BaseQuery = db.session.query(
        CVModel,
        skill_count_label
    ).join(CVSkillModel).group_by(CVModel.id).with_labels()

    query = get_sort_by(query)
    query = get_filters(query)
    query = get_limit_offset(query)

    print('\n', query, '\n')
    cvs: List[sqlalchemy.engine.row.Row] = query.all()
    return {
        'cvs': [cv.to_dict | {"skill_count": skill_count} for cv, skill_count in cvs]
    }


def get_sort_by(query: flask_sqlalchemy.BaseQuery) -> flask_sqlalchemy.BaseQuery:
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

    return query.order_by(res)


def get_filters(query: flask_sqlalchemy.BaseQuery) -> flask_sqlalchemy.BaseQuery:
    req_filters = request.json.get('filters', {})
    filters = {
        "skill": req_filters.get('skill'),  # {"categories": ["", ""], "names": ["", ""], "grade": 0}
        "skill_num": req_filters.get('skill_num'),
    }
    query_filter = [CVModel.is_hidden == False]
    if filters.get('skill'):
        skill_filter: dict = filters.get('skill')
        if skill_filter.get('categories'):
            query_filter.append(CVSkillModel.category.in_(skill_filter.get('categories')))
        if skill_filter.get('names'):
            query_filter.append(CVSkillModel.category.in_(skill_filter.get('names')))
        if skill_filter.get('grade'):
            if isinstance(skill_filter.get('grade'), int):
                query_filter.append(CVSkillModel.grade == skill_filter.get('grade'))
            else:
                query_filter.append(CVSkillModel.grade.between(
                    skill_filter.get('grade').get('from', 0),
                    skill_filter.get('grade').get('to', 10)
                ))

    if filters.get('skill_num'):
        if isinstance(filters.get('skill_num'), int):query = query.having(
                func.count(CVSkillModel.id) == filters.get('skill_num')
            )
        else:
            having_condition = filters.get('skill_num').get('from', 0) <= func.count(CVSkillModel.id)
            if filters.get('skill_num').get('to'):
                having_condition &= func.count(CVSkillModel.id) <= filters.get('skill_num').get('to', 10)
            query = query.having(having_condition)

    if filters.get('dateTimeAdd'):
        if isinstance(filters.get('dateTimeAdd'), int):
            query_filter.append(CVSkillModel.grade == filters.get('dateTimeAdd'))
        else:
            query_filter.append(CVSkillModel.dateTimeAdd >= filters.get('dateTimeAdd').get('from', 0))
            if filters.get('dateTimeAdd').get('to'):
                query_filter.append(CVSkillModel.dateTimeAdd <= filters.get('dateTimeAdd').get('to'))

    return query.filter(*query_filter)


def get_limit_offset(query: flask_sqlalchemy.BaseQuery) -> flask_sqlalchemy.BaseQuery:
    request_body: dict = request.json
    if request_body.get('limit'):
        query = query.limit(request_body.get('limit'))
    if request_body.get('offset', {}):
        query = query.offset(request_body.get('offset'))
    return query


def get_search_text(query: flask_sqlalchemy.BaseQuery) -> flask_sqlalchemy.BaseQuery:
    search_text: str = request.json.get('search_text')
    if not search_text:
        return query
    return query.filter(*query_filter)

