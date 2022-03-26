import json
import os
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
    def get(err_type: ErrorEnum, msg: str) -> Dict:
        return ErrorManager.errors.get(err_type, ErrorEnum.UNKNOWN) | {
            'msg': msg,
        }

    @staticmethod
    def get_res(err_type: ErrorEnum, msg: str) -> Response:
        return Response(
            json.dumps(ErrorManager.get(err_type, msg)),
            status=err_type.value,
            mimetype="application/json"
        )
