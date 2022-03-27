import json
import os
from pprint import pprint
from typing import Dict, List

from flask import Response

from utils.enums import ErrorEnum


class ErrorManager:

    errors: Dict[ErrorEnum, dict]

    @staticmethod
    def init_class() -> None:
        from app import app
        with open(os.path.join(app.config.get('RES_DIR'), 'errors.json')) as f:
            ErrorManager.errors = {
                ErrorEnum(int(k)): v
                for k, v in
                json.loads(f.read()).items()
            }

    @staticmethod
    def get(err_type: ErrorEnum, msg: str = None) -> Dict:
        res = ErrorManager.errors.get(err_type, ErrorManager.errors.get(ErrorEnum.UNKNOWN))
        res['msg'] = res if msg is None else msg
        return res

    @staticmethod
    def get_res(err_type: ErrorEnum, msg: str = None) -> Response:
        return Response(
            json.dumps(ErrorManager.get(err_type, msg)),
            status=err_type.value,
            mimetype="application/json"
        )
