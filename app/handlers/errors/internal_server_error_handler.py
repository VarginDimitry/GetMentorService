import traceback
from pprint import pprint

from app import app
from utils import ErrorManager, ErrorEnum


@app.errorhandler(Exception)
def internal_server_error_handler(e: Exception):
    print(traceback.format_exc())
    return ErrorManager.get_res(
        ErrorEnum.INTERNAL_SERVER_ERROR,
        e.args[0] if e.args else ""
    )
