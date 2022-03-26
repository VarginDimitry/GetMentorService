import json
from typing import List, Dict

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os

from sqlalchemy.orm import Query

db: SQLAlchemy = None
folder_path = ''


def create_skills():
    delete_count = db.session.query(BaseSkillModel).delete()
    with open(os.path.join(folder_path, 'base_skills.json'), 'r') as f:
        rows: List[Dict] = json.loads(f.read())
    for skill in rows:
        db.session.add(BaseSkillModel(**skill))
    print(f'{create_skills.__name__}:\n\tdeleted: {delete_count}\n\tinserted: {len(rows)}')
    db.session.commit()


def main():
    create_skills()


if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:qwe321@localhost:5432/gms"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db = SQLAlchemy(app)
    app.config.from_object('utils.configs.LocalConfig')
    folder_path = app.config.get('RES_DIR')
    from app.models import *

    migrate = Migrate(app, db)
    main()
