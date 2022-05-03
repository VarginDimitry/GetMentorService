from collections import Counter

from flask import request, jsonify

from app import app
from utils.models import CVModel
from utils.validation import validation_request

schema = {
    'type': {
        'type': 'string',
        'allowed': ['popular', 'all', 'base'],
        'required': False
    }
}


@app.route('/api/<api_version>/categories/get_categories', methods=['GET'])
@validation_request(with_token=True)
def get_categories(api_version: str):
    categories_type: str = request.args.get('type')
    base_categories = ['backend', 'frontend', 'android', 'ios', 'devops', 'design']

    if categories_type == 'popular':
        categories = [
            x[0] for x in
            Counter([
                x.get('category')
                for x in CVModel.coll.find({}, {'category': 1})
            ]).most_common(10)
        ]
    elif categories_type == 'all':
        categories = CVModel.coll.distinct('category', {})
    else:
        categories = base_categories

    return jsonify({'categories': categories})
