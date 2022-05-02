from datetime import datetime
from typing import List, Dict

import flask_sqlalchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from utils.enums import TimeTypeEnum
from .dict import BaseSkillModel


class CVModel(db.Model):
    query: flask_sqlalchemy.BaseQuery
    __tablename__ = 'cv'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)

    cv_skills = db.relationship("CVSkillModel", cascade="all, delete", backref="cv")
    cv_times = db.relationship("CVTimeModel", cascade="all, delete", backref="cv")

    click_count = db.Column(db.Integer, nullable=False, default=0)
    is_hidden = db.Column(db.Boolean, nullable=False, default=False)

    dateTimeAdd = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, user_id: int, is_hidden=False):
        self.id = None
        self.user_id = user_id
        self.is_hidden = is_hidden

    def get_updated(self):
        return self.query.get(self.id)

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'cv_skills': [s.to_dict for s in self.cv_skills],
            'cv_times': [t.to_dict for t in self.cv_times],
            'isHidden': self.is_hidden,
            'dateTimeAdd': self.dateTimeAdd,
        }


class CVSkillModel(db.Model):
    query: flask_sqlalchemy.BaseQuery
    __tablename__ = 'cv_skill'

    __table_args__ = (
        db.UniqueConstraint(
            'name',
            'categories',
            'cv_id',
            name='unique_cv_skill'
        ),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.id', ondelete='cascade'), nullable=False)

    name = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    grade = db.Column(db.Integer(), nullable=False)

    dateTimeAdd = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, cv_id: int, grade: int, base_skill: BaseSkillModel = None,
                 name: str = None, category: str = None, is_hidden=False):

        self.id = None
        self.cv_id = cv_id
        self.grade = grade
        self.is_hidden = is_hidden

        second_way = name and category
        if base_skill and not second_way:
            self.name = base_skill.name
            self.category = base_skill.category
        elif not base_skill and second_way:
            self.name = name
            self.category = category
        else:
            raise ValueError("You must use one of these constructors: by BaseSkills and by name and categories")

    def update(self, cv_id: int = None, name: str = None, category: str = None, grade: int = None,
               is_hidden: bool = None):
        self.cv_id = self.cv_id if cv_id is None else cv_id
        self.name = self.name if name is None else name
        self.category = self.category if category is None else category
        self.grade = self.grade if grade is None else grade
        self.is_hidden = self.is_hidden if is_hidden is None else is_hidden
        return self

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'cv_id': self.cv_id,
            'name': self.name,
            'categories': self.category,
            'grade': self.grade,
            'dateTimeAdd': self.dateTimeAdd.timestamp().__int__(),
        }


class CVTimeModel(db.Model):
    __tablename__ = 'cv_time'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.id', ondelete='cascade'), nullable=False)

    type = db.Column(db.Enum(TimeTypeEnum))

    dateTimeAdd = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, cv_id: int, time_type: TimeTypeEnum):
        self.id = None
        self.cv_id = cv_id
        self.type = time_type

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'cv_id': self.cv_id,
            'type': self.type,
            'dateTimeAdd': self.dateTimeAdd.timestamp().__int__()
        }
