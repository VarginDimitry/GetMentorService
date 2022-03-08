from pprint import pprint
from typing import List

from flask import request, make_response, jsonify
import json

from app import app, db
from app.models.dict import BaseSkillModel, BaseCategoryModel


@app.route('/api/<api_version>/dict/base_skills', methods=['GET', 'POST'])
def dict_base_skills(api_version: str):
    if request.method == 'GET':
        skills: List[BaseSkillModel] = BaseSkillModel.query.all()
        print('\n!!!!!!!!!!\n', type(skills), '\n!!!!!!!!!!!!!!!')
        pprint(skills)
        return jsonify([s.to_dict for s in skills])
    else:
        new_skill_json = request.json
        new_skill = BaseSkillModel(
            name=new_skill_json['name'],
            category=new_skill_json['category'],
        )
        db.session.add(new_skill)
        db.session.commit()
        return jsonify({'msg': 'ok'})
