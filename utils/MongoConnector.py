from utils.configs import Config
from pymongo import MongoClient
from pymongo.database import Database
from app import app


class MongoConnector:
    __mongo_config: dict = app.config.get('MONGO_CONFIG', {})
    __mongo_host: str = None
    __mongo_port: int = None
    __mongo_db: str = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            setattr(cls, 'instance', cls.create_connection())
        return getattr(cls, 'instance')

    @classmethod
    def create_connection(cls) -> Database:
        cls.__mongo_host = cls.__mongo_config.get('host', 'localhost')
        cls.__mongo_port = cls.__mongo_config.get('port', 27017)
        cls.__mongo_db = cls.__mongo_config.get('db', 'gms')
        return MongoClient(
            host=cls.__mongo_host,
            port=cls.__mongo_port,
        )[cls.__mongo_db]
