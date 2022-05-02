from datetime import datetime, timedelta
import hashlib
from typing import Union

import jwt
from pymongo.collection import Collection
from pymongo.database import Database

from app import app
from uuid import uuid4

from utils.MongoConnector import MongoConnector
from utils.enums import GenderEnum, TokenType
from utils.models import BaseModel, CVModel


class UserModel(BaseModel):
    coll_name = 'user'
    coll: Collection = BaseModel.conn.user

    def __init__(self,
                 email: str,
                 first_name: str,
                 last_name: str,
                 password: str,
                 gender: Union[GenderEnum, str] = GenderEnum.MALE,
                 middle_name: str = None,
                 phone: str = None,
                 telegram_profile: str = None,
                 is_admin=False,
                 date_time_add=None,
                 id_: str = None,
                 **kwargs):
        self.id_: str = id_

        self.first_name: str = first_name
        self.middle_name: str = middle_name
        self.last_name: str = last_name
        self.gender: GenderEnum = gender if isinstance(gender, GenderEnum) else GenderEnum(gender)
        self.email: str = email
        self.password: str = password

        self.phone: str = phone
        self.telegram_profile: str = telegram_profile
        self.is_admin: bool = is_admin

        self.date_time_add: int = date_time_add

    @staticmethod
    def get_from_db(id_: str = None,
                    email: str = None,
                    phone: str = None):
        db_res = UserModel.coll.find_one(
            {
                '$or': [
                    {'id_': id_},
                    {'email': email},
                ]
            },
            {'_id': 0},
        )
        return UserModel(**db_res) if db_res else None

    @staticmethod
    def get_from_dict(data: dict):
        return UserModel(**data)

    def save(self):
        if UserModel.coll.count_documents({
            '$or': [
                {'id_': self.id_},
                {'email': self.email},
            ]
        }) > 0:
            return {'error': 'User with this data already exists'}
        else:
            self.id_ = str(uuid4())
            self.date_time_add = datetime.now().timestamp().__int__()
            self.password = hashlib.sha256(self.password.encode()).hexdigest()
            UserModel.coll.insert_one(self.to_dict())
            return self.to_dict()

    def to_dict(self, with_cvs=False) -> dict:
        res = {
            'id_': self.id_,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'gender': self.gender.value,
            'email': self.email,
            'password': self.password,
            'phone': self.phone,
            'telegram_profile': self.telegram_profile,
            'date_time_add': self.date_time_add,
            'is_admin': self.is_admin
        }
        if with_cvs:
            from utils.models import CVModel
            res['cvs'] = CVModel.get_many_from_db(self.id_, as_dict=True)
        return res

    def assert_password(self, password: str) -> bool:
        return (self.password == hashlib.sha256(
            password.encode()
        ).hexdigest()) if password else False

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

            'id': self.id_,
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