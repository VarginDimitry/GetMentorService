from pymongo.collection import Collection
from pymongo.database import Database

from utils.MongoConnector import MongoConnector


class BaseModel:
    coll_name = 'user'
    conn: Database = MongoConnector()
    coll: Collection = MongoConnector().user

    @staticmethod
    def get_from_db(*args, **kwargs):
        raise NotImplemented()

    @staticmethod
    def get_from_dict(data: dict):
        raise NotImplemented()

    def save(self):
        raise NotImplemented()

    def to_dict(self) -> dict:
        raise NotImplemented()


