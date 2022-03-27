import base64
from datetime import datetime, timedelta
import flask_sqlalchemy
import hashlib
import jwt
from sqlalchemy.orm import relationship

from app import db, bcrypt, app

from utils.enums import GenderEnum, TokenType


class UserModel(db.Model):
    query: flask_sqlalchemy.BaseQuery
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateTimeAdd = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    first_name = db.Column(db.String(), nullable=False)
    middle_name = db.Column(db.String(), nullable=True)
    last_name = db.Column(db.String(), nullable=False)

    gender = db.Column(db.Enum(GenderEnum), nullable=False)

    phone = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    telegram_profile = db.Column(db.String, nullable=True)

    cvs = relationship("CVModel", cascade="all, delete", backref="user")

    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    password = db.Column(db.String(), nullable=False)

    def __init__(self, first_name: str, last_name: str, gender: GenderEnum,
                 email: str, password: str,
                 phone: str = None, telegram_profile: str = None,
                 middle_name: str = None, id=None, is_admin=False):
        self.id = id

        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.email = email
        self.password = hashlib.sha256(password.encode()).hexdigest()
        # self.password = bcrypt.generate_password_hash(
        #     password, app.config.get('BCRYPT_LOG_ROUNDS')
        # ).decode()

        self.phone = phone
        self.telegram_profile = telegram_profile
        self.middle_name = middle_name
        self.is_admin = is_admin

        self.dateTimeAdd = datetime.utcnow()

    def encode_token(self, token_type: TokenType):
        """
        Generates the Auth Token
        :return: string
        """
        if token_type == TokenType.ACCESS:
            life_time: int = app.config.get('ACCESS_TOKEN_LIFE')
        elif token_type == TokenType.REFRESH:
            life_time: int = app.config.get('REFRESH_TOKEN_LIFE')
        else:
            raise ValueError("You has used some invalid token type. Use utils.enums.TokenType enum")
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=life_time),
            'iat': datetime.utcnow(),

            'id': self.id,
            'email': self.email,
        }
        return jwt.encode(
            payload=payload,
            key=app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )

    @staticmethod
    def decode_token(token) -> dict:
        try:
            return jwt.decode(
                jwt=token,
                key=app.config.get('SECRET_KEY'),
                algorithms=['HS256'],
            )
        except jwt.ExpiredSignatureError:
            return {'error': 'Signature expired. Please log in again.'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token. Please log in again.'}

    def __repr__(self):
        return f"<user {self.id} | {self.first_name}>"

    def __str__(self):
        return self.__repr__()

    @property
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender.value,
            'email': self.email,
            'password': self.password,
            'phone': self.phone,
            'telegram_profile': self.telegram_profile,
            'middle_name': self.middle_name,
            'dateTimeAdd': self.dateTimeAdd,
            'cvs': [cv.to_dict for cv in self.cvs],
            'isAdmin': self.is_admin
        }

    @property
    def to_json_res(self) -> dict:
        res = self.to_dict
        res['dateTimeAdd'] = int(self.dateTimeAdd.timestamp())
        res.pop('password', None)
        res.pop('isAdmin', None)
        return res

    @staticmethod
    def assert_user_hash_with_password(user, password: str) -> bool:
        if password:
            return user.password == hashlib.sha256(password.encode()).hexdigest()
        else:
            return False

    def assert_password(self, password: str) -> bool:
        # old_pass = self.password
        # new_pass = hashlib.sha256(password.encode()).hexdigest()
        # print(f"\n{str(type(old_pass)).ljust(4)} {old_pass=}\n{str(type(new_pass)).ljust(4)} {new_pass=}\n")
        if password:
            return self.password == hashlib.sha256(password.encode()).hexdigest()
        else:
            return False
