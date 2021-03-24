from flask import Blueprint, request, jsonify

from main.src.database_module import DatabaseModule
from main.src.files_module import FilesModule
from main.src.login_module import LoginModule

login_module = LoginModule()
files_module = FilesModule()
database_module = DatabaseModule()
main = Blueprint('main', __name__)


def init_app(app):
    login_module.init_app(app)
    files_module.init_app(app)
    database_module.init_app(app)
    app.register_blueprint(main)


@main.route('/api/v1/echo', methods=['POST'])
def echo():
    content = request.get_json()
    return jsonify(content)


@main.route('/api/v1/register', methods=['POST'])
def register():
    return login_module.register()


@main.route('/api/v1/login', methods=['POST'])
def login():
    return login_module.login()


