from datetime import datetime, timedelta
import hashlib
from enum import Enum
from typing import Union, List

import jwt
from pymongo.collection import Collection
from pymongo.database import Database

from app import app
from uuid import uuid4

from utils.MongoConnector import MongoConnector
from utils.enums import GenderEnum, TokenType
from utils.models import BaseModel, CVModel


class BidStatus(Enum):
    NOT_SEEN = 'not seen'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    def __missing__(self, key):
        return self.NOT_SEEN


class BidModel(BaseModel):
    coll_name = 'bid'
    coll: Collection = MongoConnector().bid

    def __init__(self, **kwargs):
        self.id_: str = kwargs.get('id_', None)
        self.from_id: str = kwargs.get('from_id')
        self.from_name: str = kwargs.get('from_name')
        self.to_id: str = kwargs.get('to_id')
        self.to_name: str = kwargs.get('to_name')
        if isinstance(kwargs.get('status'), str):
            self.status: BidStatus = BidStatus(kwargs.get('status'))
        else:
            self.status: BidStatus = kwargs.get('status')
        self.description: str = kwargs.get('description')
        self.answer: str = kwargs.get('answer')
        if kwargs.get('date_time_add'):
            if isinstance(kwargs.get('date_time_add'), datetime):
                self.date_time_add: datetime = kwargs.get('date_time_add')
            else:
                self.date_time_add: datetime = datetime.fromtimestamp(kwargs.get('date_time_add'))
        else:
            self.date_time_add: datetime = None
        if kwargs.get('date_time'):
            if isinstance(kwargs.get('date_time'), datetime):
                self.date_time: datetime = kwargs.get('date_time')
            else:
                self.date_time: datetime = datetime.fromtimestamp(kwargs.get('date_time'))
        else:
            self.date_time: datetime = None

    @staticmethod
    def get_from_db(id_: str):
        res = BidModel.coll.find_one({'id_': id_}, {'_id': 0})
        return BidModel.get_from_dict(res) if res else None

    def save(self):
        self.id_ = self.id_ or str(uuid4())
        self.date_time_add = self.date_time_add or int(datetime.now().timestamp())
        if BidModel.coll.count_documents({
            'id_': self.id_,
            'from_id': self.from_id,
            'to_id': self.to_id,
        }) > 0:
            return {'error': 'Bid already send'}
        else:
            BidModel.coll.insert_one(self.to_dict())
            return self.to_dict()

    def update(self, set_dict: dict):
        if BidModel.coll.count_documents({
            'id_': self.id_,
            'from_id': self.from_id,
            'to_id': self.to_id,
        }) == 0:
            return {'error': 'Bid with this data doesn\'t exists'}
        else:
            BidModel.coll.update_one(
                {'id_': self.id_},
                {'$set': set_dict},
                upsert=False
            )
            self.from_id = set_dict.get('from_id', self.from_id)
            self.from_name = set_dict.get('from_name', self.from_name)
            self.to_id = set_dict.get('to_id', self.to_id)
            self.to_name = set_dict.get('to_name', self.to_name)
            if set_dict.get('status'):
                if isinstance(set_dict.get('status'), str):
                    self.status: BidStatus = BidStatus(set_dict.get('status'))
                else:
                    self.status: BidStatus = set_dict.get('status')
            self.description = set_dict.get('description', self.description)
            self.answer = set_dict.get('answer', self.answer)
            return self.to_dict()

    def to_dict(self) -> dict:
        return {
            'id_': self.id_,
            'from_id': self.from_id,
            'from_name': self.from_name,
            'to_id': self.to_id,
            'to_name': self.to_name,
            'status': self.status.value,
            'description': self.description,
            'answer': self.answer,
            'date_time_add': self.date_time_add,
            'date_time': int(self.date_time.timestamp()),
        }

    @staticmethod
    def get_all_by_from_id(from_id: str, as_dicts=True) -> List:
        res = BidModel.coll.find(
            {'from_id': from_id},
            {'_id': 0}
        )
        if as_dicts:
            return list(res)
        else:
            return [BidModel.get_from_dict(x) for x in res]

    @staticmethod
    def get_all_by_to_id(to_id: str, as_dicts=True):
        res = BidModel.coll.find(
            {'to_id': to_id},
            {'_id': 0}
        )
        if as_dicts:
            return list(res)
        else:
            return [BidModel.get_from_dict(x) for x in res]

    def delete(self):
        return BidModel.coll.delete_one({
            'id_': self.id_,
            'from_id': self.from_id,
            'to_id': self.to_id,
        })
