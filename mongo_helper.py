# -*- coding: utf-8 -*-
import json
from flask import request

from server_response import response_err, response_ok


class MongoHelper:
    def create_collection(self):
        content = request.get_json(force=True, silent=True)
        if content is None:
            return response_err(400, "parameter is not application/json")
        collection = content.get('collection', None)
        schema = content.get('schema', None)
        if (collection is None) or (schema is None):
            return response_err(400, "parameter is null")
        settings = {"schema": schema}
        with self.app.app_context():
            self.app.register_resource(collection, settings)
        data = {"collection": collection}
        return response_ok(data)
