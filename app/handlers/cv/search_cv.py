import re
import string
from pprint import pprint
from typing import List, Dict

import pymongo
from flask import request

from app import app
from utils.models import CVModel
from utils.schemas import int_filter_schema
from utils.validation import validation_request

schema = {
    'search_text': {'type': 'string', 'required': False, 'maxlength': 520},
    "limit": {'type': 'integer', 'required': False},
    "offset": {'type': 'integer', 'required': False},
    "sort_by": {
        "type": 'dict',
        'required': False,
        'schema': {
            "row": {'type': 'string', 'allowed': ['date_time_add', 'category'], 'required': True},
            "order": {'type': 'string', 'allowed': ["DESC", "ASC"], 'required': True},
        }
    },
    'filter': {
        'type': 'dict',
        'required': False,
        'schema': {
            'skill_num': int_filter_schema,
            'categories': {'type': 'list', 'required': False},
            'user_id': {'type': 'string', 'required': False, 'maxlength': 37},
            'click_count': int_filter_schema,
            'date_time_add': int_filter_schema,
        },
    }
}


@app.route('/api/<api_version>/cv/search_cv', methods=['POST'])
@validation_request(schema=schema, with_token=False)
def search_cv(api_version):
    request_body: dict = request.json

    filters: dict = request_body.get('filter', {})
    sort_by: dict = request_body.get('sort_by', {})
    limit: int = request_body.get('limit', 20)
    offset: int = request_body.get('offset', 0)
    search_text: str = request_body.get('search_text')

    sort = [(
        sort_by.get('sort_row', 'date_time_add'),
        pymongo.DESCENDING if sort_by.get('order', 'DESC') == 'DESC' else pymongo.ASCENDING
    )]

    filter_ = get_filters(filters)
    if search_text:
        filter_ = get_search_filter(search_text) | filter_

    # print(f"{limit=}\n{offset=}\n{sort}")
    pprint(filter_)
    cvs: List[Dict] = list(CVModel.coll.aggregate([
        {
            '$match': filter_
        },
        {
            '$sort': {
                row: order
                for row, order in sort
            }
        },
        {
            "$lookup": {
                "from": 'user',
                'localField': 'user_id',
                'foreignField': 'id_',
                'as': 'user'
            }
        },
        {'$skip': offset},
        {'$limit': limit},
        {'$project': {'_id': 0}},
    ]))
    for cv in cvs:
        cv['user'] = cv.get('user')[0]
        cv.get('user').pop('_id', None)
    # cvs: List[Dict] = list(CVModel.coll.find(
    #     filter_,
    #     {'_id': 0}
    # ).sort(sort).limit(limit).skip(offset))
    return {
               'msg': 'ok',
               'cvs': cvs
           }, 200


def get_filters(filters: dict) -> dict:
    filter_ = {'is_hidden': False}
    if filters.get('skill_num'):
        skill_num: Dict[str, int] = filters.get('skill_num')
        if skill_num.get('eq'):
            filter_['cv_skills'] = {'$size': skill_num.get('eq')}
        else:
            where = f"this.cv_skills.length >= {skill_num.get('from', 0)}"
            if skill_num.get('to'):
                where = f"{where} || this.cv_skills.length >= {skill_num.get('to')}"
            filter_['$where'] = where
    if filters.get('categories') is not None:
        filter_['category'] = {'$in': filters.get('categories')}
    if filters.get('user_id'):
        filter_['user_id'] = filters.get('user_id')
    if filters.get('click_count'):
        click_count: Dict[str, int] = filters.get('click_count')
        if click_count.get('eq'):
            filter_['click_count']: int = click_count.get('eq')
        else:
            filter_['click_count']: dict = {
                '$gte': click_count.get('from', 0)
            }
            if click_count.get('to'):
                filter_['click_count']['$lte'] = click_count.get('to')
    if filters.get('date_time_add'):
        date_time_add: Dict[str, int] = filters.get('date_time_add')
        if date_time_add.get('eq'):
            filter_['date_time_add'] = date_time_add.get('eq')
        else:
            filter_['date_time_add'] = {
                '$gte': date_time_add.get('from', 0)
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
