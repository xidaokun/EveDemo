MONGO_HOST = "localhost"
MONGO_PORT = 27017

GITHUB_GRANT_TYPE = "authorization_code"

DB_NAME = "register"
COL_NAME = "users"

REGISTER_ID_KEY = "_id"
REGISTER_NAME_KEY = "name"
REGISTER_PASSWORD_KEY = "password"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def oauth_settings(auth_type, code, redirect_uri, state):
    url = {
        'github': "https://github.com/login/oauth/access_token",
        'wechat': "https://api.weixin.qq.com/sns/oauth2/access_token",
        'qq': "https://graph.qq.com/oauth2.0/token"
    }

    client_id = {
        'github': "a0f35ac949b0e8ba3e33",
        'wechat': "wxd7c9f7b628e20d7f",
        'qq': "1111706401"
    }

    client_secret = {
        'github': "6badc447e2ebe6f926b916ae637be96e0df99c14",
        'wechat': "9c7b80e6ce82c5ccfed0a95ce37a1ba1",
        'qq': "KXvh5uRrPOQJEPLW"
    }

    client_id_key = {
        'github': "client_id",
        'wechat': "appid",
        'qq': "client_id"
    }

    client_secret_key = {
        'github': "client_secret",
        'wechat': "secret",
        'qq': "client_secret"
    }

    auth_params = {client_id_key(auth_type, None): client_id,
                   "grant_type": GITHUB_GRANT_TYPE,
                   client_secret_key(auth_type, None): client_secret,
                   "code": code,
                   "redirect_uri": redirect_uri,
                   "state": state}

    return url.get(auth_type, None), auth_params
