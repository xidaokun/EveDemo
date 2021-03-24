from eve import Eve

from main import src
from main.src.utils.auth import BackendAuth

DEFAULT_APP_NAME = 'backend services'

configs = {
    'development': "settings_dev.py",
    'production': "settings.py",
}


def create_service(config='development'):
    app = Eve(auth=BackendAuth, settings=configs[config])
    src.init_app(app)
    return app


