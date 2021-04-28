import time

import jwt
from jwt import ExpiredSignatureError


def create_token(user_id, user_name):
    payload = {
        "iss": "backend",
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400 * 7,
        "aud": "client",
        "sub": user_id,
        "name": user_name,
        "scopes": ['open']
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
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
        token = authorization.split(' ')
        return token
    except ValueError:
        return None


def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, 'secret',
                             audience="client",
                             algorithms=['HS256'])
    except ExpiredSignatureError:
        return False, None
    if payload:
        return True, payload
    return False, None
