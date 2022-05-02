import re
import string
from pprint import pprint
from typing import List, Dict, Union

import pymongo
import sqlalchemy
from flask import request, make_response, jsonify
import flask_sqlalchemy
from sqlalchemy import text, func
import json

from app import app
from utils.models import UserModel, CVModel
from utils import ErrorManager, ErrorEnum

from utils.enums import GenderEnum, SortType, CVSortRow
from utils.validation import validation_request


@app.route('/api/<api_version>/cv/search_cv', methods=['GET'])
@validation_request(with_token=False)
def search_cv(api_version):
    request_body: dict = request.json
    filters: dict = request_body.get('filters', {})
    sort_by: dict = request_body.get('sort_by', {})
    limit: int = request_body.get('limit', 20)
    offset: int = request_body.get('offset', 0)

    sort = [(
        sort_by.get('sort_row', 'date_time_add'),
        pymongo.DESCENDING if sort_by.get('order', 'DESC') == 'DESC' else pymongo.ASCENDING
    )]

    filter_ = get_filters(filters)
    if request_body.get('search_text'):
        filter_ = get_search_filter(request_body.get('search_text')) | filter_

    filter_.pop('is_hidden', '')
    # print(f"{limit=}\n{offset=}\n{sort}")
    pprint(filter_)
    cvs: List[Dict] = list(CVModel.coll.find(
        filter_,
        {'_id': 0}
    ).sort(sort).limit(limit).skip(offset))
    return {
               'msg': 'ok',
               'cvs': cvs
           }, 200


def get_filters(filters: dict) -> dict:
    filter_ = {'is_hidden': False}
    if filters.get('skill_num'):
        skill_num: Union[Dict[str, int], int] = filters.get('skill_num')
        if isinstance(skill_num, int):
            filter_['cv_skills'] = {'$size': skill_num}
        else:
            where = f"this.cv_skills.length >= {skill_num.get('from', 0)}"
            if skill_num.get('to'):
                where = f"{where} || this.cv_skills.length >= {skill_num.get('to')}"
            filter_['$where'] = where
    if filters.get('categories'):
        filter_['categories'] = filters.get('categories')
    if filters.get('user_id'):
        filter_['user_id'] = filters.get('user_id')
    if filters.get('click_count'):
        filter_['click_count'] = filters.get('click_count')
    if filters.get('date_time_add'):
        date_time_add: Union[Dict[str, int], int] = filters.get('date_time_add')
        if isinstance(date_time_add, int):
            filter_['date_time_add'] = date_time_add
        else:
            filter_['date_time_add'] = {
                '$gte': date_time_add.get('from')
            }
            if date_time_add.get('to'):
                filter_['skill_num']['$lte'] = date_time_add.get('to')
    return filter_


def get_search_filter(text_: str) -> dict:
    text_ = normalize_text(text_)
    regex = re.compile(text_, re.IGNORECASE)
    filter_ = {
        '$or': [
            {'categories': {'$regex': regex}},
            {'cv_skills.name': {'$regex': regex}},
            {'cv_skills.categories': {'$regex': regex}},
        ]
    }
    return filter_


def normalize_text(text_: str) -> str:
    text_ = re.sub(rf'[{string.whitespace[1:]}]+', ' ', text_)
    text_ = re.sub(r'[\s]+', ' ', text_)
    text_ = re.sub(rf'[{string.punctuation}]+', '', text_)
    text_ = text_.lower()
    RU_TO_ENG = {
        u'а': u'a',
        u'б': u'b',
        u'в': u'v',
        u'г': u'g',
        u'д': u'd',
        u'е': u'e',
        u'ё': u'e',
        u'ж': u'zh',
        u'з': u'z',
        u'и': u'i',
        u'й': u'y',
        u'к': u'k',
        u'л': u'l',
        u'м': u'm',
        u'н': u'n',
        u'о': u'o',
        u'п': u'p',
        u'р': u'r',
        u'с': u's',
        u'т': u't',
        u'у': u'u',
        u'ф': u'f',
        u'х': u'h',
        u'ц': u'ts',
        u'ч': u'ch',
        u'ш': u'sh',
        u'щ': u'sch',
        u'ъ': u'',
        u'ы': u'y',
        u'ь': u'',
        u'э': u'e',
        u'ю': u'yu',
        u'я': u'ya'
    }
    for ru_c, eng_c in RU_TO_ENG.items():
        text_ = text_.replace(ru_c, eng_c)
    return text_.strip()
