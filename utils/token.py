from datetime import datetime, timedelta

import jwt

from utils.enums import TokenType
from app import app
from utils.models import UserModel


def encode_token(token_type: TokenType, user: UserModel):
    """
    Generates the Auth Token
    :return: string
    """
    if token_type == TokenType.ACCESS:
        life_time: int = app.config.get('ACCESS_TOKEN_LIFE')
    elif token_type == TokenType.REFRESH:
        life_time: int = app.config.get('REFRESH_TOKEN_LIFE')
    else:
        raise ValueError("You has used some invalid token type. Use utils.enums.TokenType enum")
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=life_time),
        'iat': datetime.utcnow(),

        'id': user.id_,
        'email': user.email,
    }
    return jwt.encode(
        payload=payload,
        key=app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )


def decode_token(token) -> dict:
    try:
        return jwt.decode(
            jwt=token,
            key=app.config.get('SECRET_KEY'),
            algorithms=['HS256'],
        )
    except jwt.ExpiredSignatureError:
        return {'error': 'Signature expired. Please log in again.'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token. Please log in again.'}