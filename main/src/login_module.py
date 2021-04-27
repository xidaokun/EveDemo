import requests
from flask import request

from main.src.info_cache import *
from main.src.utils.server_response import ServerResponse


class LoginModule:
    def __init__(self, app=None):
        self.app = app
        self.response = ServerResponse("Login")

    def init_app(self, app):
        self.app = app

    def register(self):
        content = request.get_json(force=True, silent=True)
        if content is None:
            return self.response.response_err(400, "parameter is not application/json")
        name = content.get('name', None)
        password = content.get('password', None)
        if (name is None) or (password is None):
            return self.response.response_err(400, "parameter is null")

        try:
            save_info_to_db(name, password)
        except Exception as e:
            print("Exception in register::", e)

        return self.response.response_ok()

    def login(self):
        content = request.get_json(force=True, silent=True)
        if content is None:
            return self.response.response_err(400, "parameter is not application/json")
        name = content.get('name', None)
        password = content.get('password', None)
        if (name is None) or (password is None):
            return self.response.response_err(400, "parameter is null")

        info = get_info_by_name(name)
        if info is None:
            return self.response.response_err(401, "User error")

        # verify password
        pw = info[ID_INFO_REGISTER_PASSWORD]
        if password != pw:
            return self.response.response_err(401, "Password error")

        token = create_token()
        save_token_to_db(name, token)

        data = {"token": token}
        return self.response.response_ok(data)

    def oauth(self):
        code = request.args.get('code')
        auth_type = request.args.get('type')
        redirect_uri = request.args.get('redirect_uri')
        state = request.args.get('state')
        if (code is None) or (auth_type is None):
            return self.response.response_err(400, "parameter is null")

        url, auth_params = oauth_settings(auth_type, code, redirect_uri, state)
        ret = requests.get(url, headers={'accept': 'application/json'}, params=auth_params).text

        return self.response.response_ok(ret)
