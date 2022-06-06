from flask import request, jsonify
from pymongo.collection import Collection

from app import app
from utils.MongoConnector import MongoConnector


@app.route('/api/<api_version>/dict/base_skills', methods=['GET'])
def base_skills(api_version: str):
    category = request.args.get('category')
    coll: Collection = MongoConnector().base_skill
    res = list(coll.find({'category': category} if category else {}, {'_id': 0}))
    return jsonify(res)
