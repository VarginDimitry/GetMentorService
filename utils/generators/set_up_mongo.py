import json
import pathlib
from typing import Dict, List

from pymongo import UpdateOne
from pymongo.collection import Collection

from app import app
from utils.MongoConnector import MongoConnector


conn = MongoConnector()
res_dir = pathlib.Path(__file__).parent.parent.parent / 'res'


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
    gen_base_skills()
