from datetime import datetime

import flask_sqlalchemy
from sqlalchemy.orm import relationship

from app import db

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

    def __init__(self, first_name: str, last_name: str, gender: str,
                 email: str, password: str,
                 phone: str = None, telegram_profile: str = None,
                 middle_name: str = None):
        self.id = None

        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.email = email
        self.password = password

        self.phone = phone
        self.telegram_profile = telegram_profile
        self.middle_name = middle_name

    def __repr__(self):
        return f"<user {self.id} | {self.first_name}>"
