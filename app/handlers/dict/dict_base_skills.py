from flask import request, jsonify
from pymongo.collection import Collection

from app import app
from utils.MongoConnector import MongoConnector


@app.route('/api/<api_version>/dict/base_skills', methods=['GET', 'POST'])
def dict_base_skills(api_version: str):
    coll: Collection = MongoConnector().base_skills
    if request.method == 'GET':
        res = list(coll.find())
        for skill in res:
            skill.pop('_id', None)
        return jsonify(res)
    else:
        req_body: dict = request.json
        skill = {
            'name': req_body.get('name'),
            'categories': req_body.get('categories'),
        }
        res = coll.update_one(
            filter=skill,
            update={
                '$set': skill
            },
            upsert=True,
        )
        return jsonify({'msg': 'ok' if res.upserted_id else 'not_ok'})
