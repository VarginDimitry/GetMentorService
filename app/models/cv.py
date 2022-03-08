from datetime import datetime

import flask_sqlalchemy
from sqlalchemy.orm import relationship

from app import db
from utils.enums import TimeTypeEnum


class CVModel(db.Model):
    query: flask_sqlalchemy.BaseQuery
    __tablename__ = 'cv'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)

    cv_skills = db.relationship("CVSkillModel", cascade="all, delete", backref="cv")
    cv_times = db.relationship("CVTimeModel", cascade="all, delete", backref="cv")

    dateTimeAdd = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)


class CVSkillModel(db.Model):
    query: flask_sqlalchemy.BaseQuery
    __tablename__ = 'cv_skill'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.id', ondelete='cascade'), nullable=False)

    name = db.Column(db.String(), unique=True, nullable=False)
    category = db.Column(db.String(), nullable=False)
    grade = db.Column(db.Integer(), nullable=False)

    dateTimeAdd = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)


class CVTimeModel(db.Model):
    __tablename__ = 'cv_time'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.id', ondelete='cascade'), nullable=False)

    type = db.Column(db.Enum(TimeTypeEnum))

    dateTimeAdd = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
