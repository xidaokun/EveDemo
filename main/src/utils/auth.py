import time

import jwt
from jwt import ExpiredSignatureError

from main.src.utils.constants import JWT_SECRET, JWT_ISS, JWT_AUD, JWT_ALGORITHMS, JWT_SCOPES


def create_token(user_id, user_name):
    payload = {
        "iss": JWT_ISS,
        "iat": int(time.time()),
        "exp": int(time.time()) + 60 * 5,
        "aud": JWT_AUD,
        "sub": user_id,
        "name": user_name,
        "scopes": [JWT_SCOPES]
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHMS)
    return {'access_token': token,
                  'user_name': user_name,
                  'user_id': user_id}


def verify_request(request):
    token = get_authorization(request)

    return verify_jwt_token(token)


def get_authorization(request):
    authorization = request.headers.get('Authorization')
    if not authorization:
        return False, None
    try:
        authorization_type, token = authorization.split(' ')
        return token
    except ValueError:
        return None


def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET,
                             audience=[JWT_AUD],
                             algorithms=[JWT_ALGORITHMS])
    except ExpiredSignatureError:
        return False, token
    if payload:
        return True, payload
    return False, None
