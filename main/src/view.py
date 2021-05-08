

from flask import Blueprint, request, jsonify

from main.src.db_module import DbModule
from main.src.files_module import FilesModule
from main.src.login_module import LoginModule

login_module = LoginModule()
files_module = FilesModule()
database_module = DbModule()
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


@main.route('/api/v1/user/register', methods=['POST'])
def register():
    return login_module.register()


@main.route('/api/v1/user/login', methods=['POST'])
def login():
    return login_module.login()


@main.route('/api/v1/user/verification_code', methods=['POST'])
def verification_code():
    return login_module.verification_code()


@main.route('/api/v1/user/change_pwd', methods=['POST'])
def modify_pwd():
    return login_module.modify_pwd()


@main.route('/api/v1/user/oauth', methods=['GET'])
def oauth():
    return login_module.oauth()


@main.route('/api/v1/file/upload/<path:file_name>', methods=['POST'])
def upload_file(file_name):
    return files_module.upload_file(file_name)


@main.route('/api/v1/file/download', methods=['GET'])
def download_file():
    return files_module.download_file()


@main.route('/api/v1/file/list', methods=['GET'])
def list_files():
    return files_module.list_files()


@main.route('/api/v1/file/information', methods=['GET'])
def get_file_information():
    return files_module.get_file_info()


@main.route('/api/v1/file/delete', methods=['POST'])
def delete_file():
    return files_module.delete_file()


@main.route('/api/v1/db/create_col', methods=['POST'])
def create_collection():
    return database_module.create_collection()


@main.route('/api/v1/db/delete_col', methods=['POST'])
def delete_collection():
    return database_module.delete_collection()


@main.route('/api/v1/db/insert_one', methods=['POST'])
def insert_one():
    return database_module.insert_one()


@main.route('/api/v1/db/insert_many', methods=['POST'])
def insert_many():
    return database_module.insert_many()


@main.route('/api/v1/db/update_one', methods=['POST'])
def update_one():
    return database_module.update_one()


@main.route('/api/v1/db/update_many', methods=['POST'])
def update_many():
    return database_module.update_many()


@main.route('/api/v1/db/find_one', methods=['POST'])
def find_one():
    return database_module.find_one()


@main.route('/api/v1/db/find_many', methods=['POST'])
def find_many():
    return database_module.find_many()


@main.route('/api/v1/db/count_documents', methods=['POST'])
def count_documents():
    return database_module.count_documents()


@main.route('/api/v1/db/delete_one', methods=['POST'])
def delete_one():
    return database_module.delete_one()


@main.route('/api/v1/db/delete_many', methods=['POST'])
def delete_many():
    return database_module.delete_many()
