import time

import jwt
from flask import request
from jwt import ExpiredSignatureError

from main.settings import JWT_ISS, JWT_AUD, JWT_SCOPES, JWT_SECRET, JWT_ALGORITHMS
from main.src.utils.server_response import ServerResponse


def create_token(user_id, user_name):
    payload = {
        "iss": JWT_ISS,
        "iat": int(time.time()),
        "exp": int(time.time()) + 60 * 60,
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


class LoginCheck:
    def __init__(self, func):
        self._func = func
        self.response = ServerResponse("Auth")

    def __call__(self, *args, **kwargs):
        isvalid, payload = verify_request(request)
        if isvalid is False:
            response = ServerResponse("Auth")
            return response.response_err(401, "token is invalid")
        if args:
            return self._func(self, args[0])
        return self._func(self)


class LoginCheckWithPayload:
    def __init__(self, func):
        self._func = func
        self.response = ServerResponse("Auth")

    def __call__(self, *args, **kwargs):
        isvalid, payload = verify_request(request)
        if isvalid is False:
            response = ServerResponse("Auth")
            return response.response_err(401, "token is invalid")
        return self._func(self, payload)