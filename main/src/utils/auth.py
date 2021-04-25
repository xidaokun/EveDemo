from flask import request

from main.src.info_cache import *


def get_id_by_token():
    auth = request.headers.get("Authorization")
    if auth is None:
        return None

    if auth.strip().lower().startswith(("token", "bearer")):
        token = auth.split(" ")[1]
        info = get_info_by_token(token)
        if info is not None:
            return info["_id"]
        else:
            return None
    else:
        return None


