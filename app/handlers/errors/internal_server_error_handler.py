from pprint import pprint

from app import app
from utils import ErrorManager, ErrorEnum


@app.errorhandler(Exception)
def internal_server_error_handler(e: Exception):
    pprint(e)
    return ErrorManager.get_res(
        ErrorEnum.INTERNAL_SERVER_ERROR,
        e.args[0]
    )
