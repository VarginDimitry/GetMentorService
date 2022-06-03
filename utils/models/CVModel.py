from collections import namedtuple
from datetime import datetime, timedelta
import hashlib
from typing import Union, Dict, List

import jwt
from pymongo import UpdateOne
from pymongo.collection import Collection
from pymongo.database import Database

from app import app
from uuid import uuid4

from utils.MongoConnector import MongoConnector
from utils.models import BaseModel


class CVModel(BaseModel):
    coll_name = 'cv'
    coll: Collection = BaseModel.conn.cv

    class SkillModel:
        def __init__(self, name: str = None,
                     category: str = None,
                     grade=0,
                     **kwargs):
            self.name = name
            self.category = category
            self.grade = grade

        def to_dict(self):
            return {
                'name': self.name,
                'categories': self.category,
                'grade': self.grade,
            }

    def __init__(self,
                 user_id: str,
                 category: str = None,
                 id_: str = None,
                 cv_skills: list = None,
                 cv_times: list = None,
                 click_count=0,
                 is_hidden=False,
                 **kwargs):
        self.id_: str = id_
        self.user_id: str = user_id
        self.category: str = category

        if cv_skills:
            if isinstance(cv_skills[0], dict):
                cv_skills = [CVModel.SkillModel(**x) for x in cv_skills]
        else:
            cv_skills = []
        self.cv_skills: List[CVModel.SkillModel] = cv_skills
        self.cv_times: list = cv_times if cv_times else []

        self.click_count = click_count
        self.is_hidden = is_hidden

        self.date_time_add: int = None

    def to_dict(self):
        return {
            'id_': self.id_,
            'user_id': self.user_id,
            'categories': self.category,
            'cv_skills': [x.to_dict() for x in self.cv_skills],
            'cv_times': self.cv_times,
            'is_hidden': self.is_hidden,
            'date_time_add': self.date_time_add,
        }

    @staticmethod
    def get_from_db(id_: str, user_id: str = None):
        query = {'id_': id_}
        if user_id:
            query['$or'] = [
                {'id_': user_id},
                {'is_hidden': False}
            ]

        db_res = CVModel.coll.find_one(
            query,
            {'_id': 0}
        )
        return CVModel(**db_res) if db_res else None

    @staticmethod
    def get_many_from_db(user_id: str, as_dict=False) -> List:
        db_res = CVModel.coll.find(
            {'user_id': user_id},
            {'_id': 0},
        )
        if as_dict:
            return [dict(x) for x in db_res]
        else:
            return [
                CVModel(**x)
                for x in
                db_res
            ]

    def save(self):
        if CVModel.coll.count_documents({
            'id_': self.id_,
            'user_id': self.user_id,
        }) > 0:
            return {'error': 'User with this data already exists'}
        else:
            self.id_ = str(uuid4())
            self.date_time_add = int(datetime.now().timestamp())
            CVModel.coll.insert_one(self.to_dict())
            return self.to_dict()

    def update(self, inplace=True, **kwargs) -> Union[UpdateOne, None]:
        filter_ = {
            'id_': self.id_,
            'user_id': self.user_id,
        }
        update = {
            '$set': {
                'categories': kwargs.get('categories', self.category),
                'cv_skills':
                    [
                        x if isinstance(x, dict) else x.to_dict()
                        for x in kwargs.get('cv_skills', self.cv_skills)
                    ]
            }
        }
        upsert = False
        self.category = kwargs.get('categories', self.category)
        self.cv_skills = [
            CVModel.SkillModel(**x) if isinstance(x, dict) else x
            for x in kwargs.get('cv_skills', self.cv_skills)
        ]
        if inplace:
            self.coll.update_one(filter_, update, upsert)
        else:
            return UpdateOne(filter_, update, upsert)
