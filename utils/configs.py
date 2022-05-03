class Config:
    TESTING = True
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BCRYPT_LOG_ROUNDS = 8
    SECRET_KEY = 'thingsboardDefaultSigningKey'

    DB_ENGINE = 'postgresql'

    DB_USER_NAME = 'postgres'
    DB_USER_PASSWORD = 'qwe321'

    DB_SERVER = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'gms'
    DATABASE_URI = SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}://{DB_USER_NAME}:{DB_USER_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

    ACCESS_TOKEN_LIFE  = 100000  # minutes
    REFRESH_TOKEN_LIFE = 200000  # minutes

    RES_DIR = './res'

    MONGO_CONFIG = {
        "host": "localhost",
        "port": 27017,
        "db": "gms",
    }


class DockerConfig(Config):
    MONGO_CONFIG = {
        "host": "mongodb://mongodb",
        "port": 27017,
        "db": "gms",
    }


class ProductionConfig(Config):
    pass
