MONGO_HOST = "localhost"
MONGO_PORT = 27017

GITHUB_GRANT_TYPE = "authorization_code"

ID_PREFIX = "_id_prefix"
ID_DB_PREFIX = "id_of_"
ID_INFO_DB_NAME = "register"
ID_INFO_REGISTER_COL = "users"

ID_INFO_REGISTER_PASSWORD = "password"
ID_INFO_REGISTER_TOKEN = "token"

MODE_DEV = "dev"
MODE_PROD = "prod"
MODE_TEST = "test"


def oauth_settings(auth_type, code, redirect_uri, state):
    url = {
        'github': "https://github.com/login/oauth/access_token",
        'wechat': "https://api.weixin.qq.com/sns/oauth2/access_token",
        'qq': "https://graph.qq.com/oauth2.0/token"
    }

    client_id = {
        'github': "YOUR",
        'wechat': "YOUR",
        'qq': "YOUR"
    }

    client_secret = {
        'github': "YOUR",
        'wechat': "YOUR",
        'qq': "YOUR"
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
