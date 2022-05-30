class LocalConfig:
    TESTING = False
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BCRYPT_LOG_ROUNDS = 8
    SECRET_KEY = 'thingsboardDefaultSigningKey'

    ACCESS_TOKEN_LIFE = 100000  # minutes
    REFRESH_TOKEN_LIFE = 200000  # minutes

    RES_DIR = './res'

    MONGO_HOST = 'localhost:27017'
    MONGO_DB = 'gms'
    MONGO_CONFIG = {
        "host": "localhost",
        "port": 27017,
        "db": "gms",
    }


class DockerConfig(LocalConfig):
    MONGO_HOST = 'mongodb://mongodb:27017'
    MONGO_CONFIG = {
        "host": "mongodb://mongodb",
        "port": 27017,
        "db": "gms",
    }


class TestLocalConfig(LocalConfig):
    TESTING = True
    MONGO_HOST = 'mongodb://localhost:27017'
    MONGO_CONFIG = {
        "host": "mongodb://localhost",
        "port": 27017,
        "db": "gms_test",
    }
