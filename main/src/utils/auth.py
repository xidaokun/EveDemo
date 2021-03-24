from eve.auth import TokenAuth
from flask import request

from main.src.info_cache import *


class BackendAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        info = get_info_by_token(token)
        if info is not None:
            return True
        else:
            return False


def get_auth_token():
    auth = request.headers.get("Authorization").strip()
    if auth.lower().startswith("token", "bearer"):
        token = auth.split(" ")[1]
        info = get_info_by_token(token)
        if info is not None:
            return info["_id"]
        else:
            return None
    else:
        return None


