from flask import Blueprint, request, jsonify

import mongo_helper

main = Blueprint('main', __name__)


def init_app(app):
    app.register_blueprint(main)


@main.route('/api/v1/echo', methods=['POST'])
def echo():
    content = request.get_json()
    return jsonify(content)


@main.route('/api/v1/create_collection', methods=['POST'])
def create_collection_view():
    return mongo_helper.create_collection()
