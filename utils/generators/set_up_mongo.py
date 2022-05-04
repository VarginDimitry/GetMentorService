import json
import pathlib
from pprint import pprint
from typing import Dict, List

import requests
from pymongo import UpdateOne
from pymongo.collection import Collection
from pymongo.database import Database

from app import app
from utils.MongoConnector import MongoConnector
from utils.models import UserModel

conn: Database = MongoConnector()
res_dir = pathlib.Path(__file__).parent.parent.parent / 'res'


def clear_db():
    collections = conn.list_collection_names()
    delete_count = {}
    for collection in collections:
        delete_count[collection] = conn[collection].delete_many({}).deleted_count
    print('Delete count:')
    pprint(delete_count)


def gen_base_skills():
    file_path = res_dir / 'base_skills.json'
    with file_path.open('r') as f:
        skills: List[Dict] = json.loads(f.read())
    print(f"Read {len(skills)} skills: \n{skills[:10]}...")
    bs_coll: Collection = conn.base_skill
    upd_list = []
    for skill in skills:
        upd_list.append(UpdateOne(skill, {"$set": skill}, upsert=True))
    bs_coll.bulk_write(upd_list, ordered=True)


if __name__ == '__main__':
    clear_db()
    gen_base_skills()
