import flask_sqlalchemy

from app import db


class BaseSkillModel(db.Model):
    query: flask_sqlalchemy.BaseQuery
    __tablename__ = 'base_skill'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)

    def __init__(self, name: str, category: str, id=None):
        self.id = id

        self.name = name
        self.category = category

    def __repr__(self):
        return f"<base_skill {self.id} | {self.name}>"

    @property
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
        }


class BaseCategoryModel(db.Model):
    query: flask_sqlalchemy.BaseQuery
    __tablename__ = 'base_category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)

    def __init__(self, name: str, id=None):
        self.id = id

        self.name = name

    def __repr__(self):
        return f"<base_skill {self.id} | {self.name}>"

    @property
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
