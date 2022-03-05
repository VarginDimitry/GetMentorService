from flask import request
import json

from app import app


@app.route('/api/<api_version>/dict/base_skills', methods=['GET'])
def dict_base_skills(api_version: str):
    base_skills = [
        {
            'id': 0,
            'name': 'python',
            'category': 'programming',
        },
        {
            'id': 1,
            'name': 'java',
            'category': 'programming',
        },
        {
            'id': 2,
            'name': 'Project management',
            'category': 'management',
        },
    ]
    return json.dumps(base_skills)
