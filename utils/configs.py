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
    a = DB_NAME
    DATABASE_URI = SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}://{DB_USER_NAME}:{DB_USER_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


class LocalConfig(Config):
    DB_SERVER = 'localhost'


class ProductionConfig(Config):
    """Uses production database server."""
    DB_SERVER = '192.168.19.32'
