import logging

from utils.configs import Config
from pymongo import MongoClient
from pymongo.database import Database
from app import app


class MongoConnector:
    conn: MongoClient = None
    mongo_host: str = None
    mongo_db: str = None

    def __new__(cls) -> Database:
        if not hasattr(cls, 'instance'):
            setattr(cls, 'instance', cls.create_connection())
        app.logger.info(f"LOGGER {cls.mongo_host=}")
        return getattr(cls, 'instance')

    @classmethod
    def create_connection(cls) -> Database:
        cls.mongo_host = app.config.get('MONGO_HOST')
        cls.mongo_db = app.config.get('MONGO_DB')
        app.logger.info(f"{cls.mongo_host=}")
        cls.conn = MongoClient(
            host=cls.mongo_host[:cls.mongo_host.rfind(':')],
            port=int(cls.mongo_host[cls.mongo_host.rfind(':')+1:]),
        )
        return cls.conn[cls.mongo_db]
