import base64
from datetime import datetime, timedelta
import flask_sqlalchemy
import jwt
from sqlalchemy.orm import relationship

from app import db, bcrypt, app

from utils.enums import GenderEnum


class UserModel(db.Model):
    query: flask_sqlalchemy.BaseQuery
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateTimeAdd = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    first_name = db.Column(db.String(), nullable=False)
    middle_name = db.Column(db.String(), nullable=True)
    last_name = db.Column(db.String(), nullable=False)

    gender = db.Column(db.Enum(GenderEnum), nullable=False)

    phone = db.Column(db.String(), nullable=True, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    telegram_profile = db.Column(db.String, nullable=True)

    cvs = relationship("CVModel", cascade="all, delete", backref="user")

    password = db.Column(db.String(), nullable=False)

    def __init__(self, first_name: str, last_name: str, gender: GenderEnum,
                 email: str, password: str,
                 phone: str = None, telegram_profile: str = None,
                 middle_name: str = None, id=None):
        self.id = id

        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

        self.phone = phone
        self.telegram_profile = telegram_profile
        self.middle_name = middle_name

        self.dateTimeAdd = datetime.utcnow()

    def encode_auth_token(self, user_id, email):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=2),
                'iat': datetime.utcnow(),

                'sub': user_id,
                'email': email,
            }
            return jwt.encode(
                payload=payload,
                key=app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        # try:
        t_sp = auth_token.split('.')
        t_sp[-1] = base64.b64encode(t_sp[-1].encode('ascii')).decode()
        tt = '.'.join(t_sp)
        print(f"token={tt}")
        secret: str = app.config.get('SECRET_KEY')
        payload = jwt.decode(
            jwt=auth_token,
            key=secret,
            algorithms=['HS256'],
        )
        return payload
        # except jwt.ExpiredSignatureError:
        #     return 'Signature expired. Please log in again.'
        # except jwt.InvalidTokenError:
        #     return 'Invalid token. Please log in again.'

    def __repr__(self):
        return f"<user {self.id} | {self.first_name}>"

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
        }

    @property
    def to_json_res(self) -> dict:
        res = self.to_dict
        res['dateTimeAdd'] = int(self.dateTimeAdd.timestamp())
        res.pop('password')
        return res
