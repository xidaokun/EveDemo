import hashlib
import random

import requests
from flask import request

from main.settings import ACCOUNT_SID, ACCOUNT_TOKEN, APPID, TEMPLAYE_ID
from main.src.info_cache import *
from main.src.utils.auth import create_token, verify_request
from main.src.utils.redis_utils import RedisUtils
from main.src.utils.server_response import ServerResponse
from main.src.utils.sms import RongYun


class LoginModule:
    def __init__(self, app=None):
        self.app = app
        self.response = ServerResponse("Login")
        self._redis_utils = RedisUtils()

    def init_app(self, app):
        self.app = app

    def register(self):
        content = request.get_json(force=True, silent=True)
        if content is None:
            return self.response.response_err(400, "parameter is not application/json")

        name = content.get('name', None)
        info = get_info(name)
        if info:
            return self.response.response_err(400, "user is exist")

        password = content.get('password', None)
        if (name is None) or (password is None):
            return self.response.response_err(400, "name or password is null")

        phone = content.get('phone', None)
        if (name is None) or (password is None):
            return self.response.response_err(400, "name or password is null")
        code = content.get(phone, None)
        cache_code = self._redis_utils.get('code')
        if cache_code is None:
            return self.response.response_err(400, "code has expired")

        if code != cache_code:
            return self.response.response_err(400, "code is invalid")

        try:
            save_info(name, hashlib.sha256(password.encode("utf8")).hexdigest())
        except Exception as e:
            return self.response.response_err(500, e)

        return self.response.response_ok()

    def login(self):
        content = request.get_json(force=True, silent=True)
        if content is None:
            return self.response.response_err(400, "parameter should be application/json")
        name = content.get('name', None)
        password = content.get('password', None)

        info = get_info(name)
        if info is None:
            return self.response.response_err(401, "can not find user")

        # verify password
        pw = info[REGISTER_PASSWORD_KEY]
        password = hashlib.sha256(password.encode("utf8")).hexdigest()
        if password != pw:
            return self.response.response_err(401, "password is error")

        user_id = str(info[REGISTER_ID_KEY])
        data = create_token(user_id, name)
        return self.response.response_ok(data)

    def verification_code(self):
        content = request.get_json(force=True, silent=True)
        if content is None:
            return self.response.response_err(400, "parameter should be application/json")
        phone = content.get('phone', None)
        code = random.randint(1000, 9999)

        config = {
            "accountSid": ACCOUNT_SID,
            "accountToken": ACCOUNT_TOKEN,
            "appId": APPID,
            "templateId": TEMPLAYE_ID
        }

        yun = RongYun(**config)
        data = yun.run(phone, code)
        # TODO Different situations need to be verified
        self._redis_utils.set(phone, code, 3000)
        return self.response.response_ok()

    def oauth(self):
        code = request.args.get('code')
        auth_type = request.args.get('type')
        redirect_uri = request.args.get('redirect_uri')
        state = request.args.get('state')
        if (code is None) or (auth_type is None):
            return self.response.response_err(400, "parameter is null")

        url, auth_params = oauth_settings(auth_type, code, redirect_uri, state)
        ret = requests.get(url, headers={'accept': 'application/json'}, params=auth_params).text
        # TODO Need to get user information
        data = create_token()
        return self.response.response_ok(data)

    def modify_pwd(self):
        isvalid, payload = verify_request()
        if isvalid:
            return self.response.response_err(401, "token is invalid")

        content = request.get_json(force=True, silent=True)
        if content is None:
            return self.response.response_err(400, "parameter is not application/json")

        password = content.get('password', None)
        if password is None:
            return self.response.response_err(400, "name or password is null")

        try:
            update_pwd(payload['name'], hashlib.sha256(password).hexdigest())
        except Exception as e:
            print("Exception in register::", e)

        return self.response.response_ok()