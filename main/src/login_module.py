from flask import request

from main.src.info_cache import *
from main.src.utils.server_response import *


class LoginModule:
    def __init__(self, app=None):
        self.app = app

    def init_app(self, app):
        self.app = app

    def register(self):
        content = request.get_json(force=True, silent=True)
        if content is None:
            return response_err(400, "parameter is not application/json")
        name = content.get('name', None)
        password = content.get('password', None)
        if (name is None) or (password is None):
            return response_err(400, "parameter is null")

        try:
            save_info_to_db(name, password)
        except Exception as e:
            print("Exception in did_register::", e)

        return response_ok()

    def login(self):
        content = request.get_json(force=True, silent=True)
        if content is None:
            return response_err(400, "parameter is not application/json")
        name = content.get('name', None)
        password = content.get('password', None)
        if (name is None) or (password is None):
            return response_err(400, "parameter is null")

        info = get_info_by_name(name)
        if info is None:
            return response_err(401, "User error")

        # verify password
        pw = info[ID_INFO_REGISTER_PASSWORD]
        if password != pw:
            return response_err(401, "Password error")

        token = create_token()
        save_token_to_db(name, token)

        data = {"token": token}
        return response_ok(data)


