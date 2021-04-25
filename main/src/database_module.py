import json
from datetime import datetime

from bson import json_util
from flask import request

from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

from main.src.utils.auth import get_id_by_token
from main.src.utils.common import md5_encode
from main.src.utils.constants import MONGO_HOST, MONGO_PORT
from main.src.utils.server_response import ServerResponse


class DatabaseModule:
    def __init__(self, app=None):
        self.app = app
        self.response = ServerResponse("Database")

    def init_app(self, app):
        self.app = app

    def create_collection(self):
        name = get_id_by_token()
        if name is None:
            return self.response.response_err(401, "token is invalid")

        collection_name = request.get_json(force=True, silent=True).get('collection')

        connection = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        db_name = md5_encode(name)
        db = connection[db_name]
        try:
            db.create_collection(collection_name)
        except CollectionInvalid:
            pass
        except Exception as e:
            return self.response.response_err(500, "Exception:" + str(e))
        return self.response.response_ok()

    def delete_collection(self):
        name = get_id_by_token()
        if name is None:
            return self.response.response_err(401, "token is invalid")

        collection_name = request.get_json(force=True, silent=True).get('collection', None)
        if collection_name is None:
            return self.response.response_err(400, "parameter is null")

        connection = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        db_name = md5_encode(name)
        db = connection[db_name]
        try:
            db.drop_collection(collection_name)
        except CollectionInvalid:
            pass
        except Exception as e:
            return self.response.response_err(500, "Exception:" + str(e))
        return self.response.response_ok()

    def insert_one(self):
        name = get_id_by_token()
        if name is None:
            return self.response.response_err(401, "token is invalid")

        options = populate_options_insert_one(content)

        col = get_collection(did, app_id, content["collection"])
        if not col:
            return self.response.response_err(404, "collection not exist")

        data, err_message = query_insert_one(col, content, options)
        if err_message:
            return self.response.response_err(500, err_message)

        db_size = get_mongo_database_size(did, app_id)
        update_db_use_storage_byte(did, db_size)
        return self.response.response_ok(data)

    def insert_many(self):
        name = get_id_by_token()
        if name is None:
            return self.response.response_err(401, "token is invalid")

        col = get_collection(did, app_id, content["collection"])
        if not col:
            return self.response.response_err(404, "collection not exist")

        options = options_filter(content, ("bypass_document_validation", "ordered"))

        try:
            new_document = []
            for document in content["document"]:
                document["created"] = datetime.utcnow()
                document["modified"] = datetime.utcnow()
                new_document.append(convert_oid(document))

            ret = col.insert_many(new_document, **options)
            db_size = get_mongo_database_size(did, app_id)
            update_db_use_storage_byte(did, db_size)
            data = {
                "acknowledged": ret.acknowledged,
                "inserted_ids": [str(_id) for _id in ret.inserted_ids]
            }
            return self.response.response_ok(data)
        except Exception as e:
            return self.response.response_err(500, "Exception:" + str(e))

    def update_one(self):
        name = get_id_by_token()
        if name is None:
            return self.response.response_err(401, "token is invalid")

        options = populate_options_update_one(content)

        col = get_collection(did, app_id, content["collection"])
        if not col:
            return self.response.response_err(404, "collection not exist")

        data, err_message = query_update_one(col, content, options)
        if err_message:
            return self.response.response_err(500, err_message)

        db_size = get_mongo_database_size(did, app_id)
        update_db_use_storage_byte(did, db_size)
        return self.response.response_ok(data)

    def update_many(self):
        name = get_id_by_token()
        if name is None:
            return self.response.response_err(401, "token is invalid")

        col = get_collection(did, app_id, content["collection"])
        if not col:
            return self.response.response_err(404, "collection not exist")

        options = options_filter(content, ("upsert", "bypass_document_validation"))

        try:
            update_set_on_insert = content.get('update').get('$setOnInsert', None)
            if update_set_on_insert:
                content["update"]["$setOnInsert"]['created'] = datetime.utcnow()
            else:
                content["update"]["$setOnInsert"] = {
                    "created": datetime.utcnow()
                }
            if "$set" in content["update"]:
                content["update"]["$set"]["modified"] = datetime.utcnow()
            ret = col.update_many(convert_oid(content["filter"]), convert_oid(content["update"], update=True),
                                  **options)
            data = {
                "acknowledged": ret.acknowledged,
                "matched_count": ret.matched_count,
                "modified_count": ret.modified_count,
                "upserted_id": str(ret.upserted_id)
            }
            db_size = get_mongo_database_size(did, app_id)
            update_db_use_storage_byte(did, db_size)
            return self.response.response_ok(data)
        except Exception as e:
            return self.response.response_err(500, "Exception:" + str(e))

    def delete_one(self):
        name = get_id_by_token()
        if name is None:
            return self.response.response_err(401, "token is invalid")

        col = get_collection(did, app_id, content["collection"])
        if not col:
            return self.response.response_err(404, "collection not exist")

        data, err_message = query_delete_one(col, content)
        if err_message:
            return self.response.response_err(500, err_message)

        db_size = get_mongo_database_size(did, app_id)
        update_db_use_storage_byte(did, db_size)
        return self.response.response_ok(data)

    def delete_many(self):
        name = get_id_by_token()
        if name is None:
            return self.response.response_err(401, "token is invalid")

        col = get_collection(did, app_id, content["collection"])
        if not col:
            return self.response.response_err(404, "collection not exist")

        try:
            ret = col.delete_many(convert_oid(content["filter"]))
            data = {
                "acknowledged": ret.acknowledged,
                "deleted_count": ret.deleted_count,
            }
            db_size = get_mongo_database_size(did, app_id)
            update_db_use_storage_byte(did, db_size)
            return self.response.response_ok(data)
        except Exception as e:
            return self.response.response_err(500, "Exception:" + str(e))

    def count_documents(self):
        name = get_id_by_token()
        if name is None:
            return self.response.response_err(401, "token is invalid")

        options = populate_options_count_documents(content)

        col = get_collection(did, app_id, content["collection"])
        if not col:
            return self.response.response_err(404, "collection not exist")

        data, err_message = query_count_documents(col, content, options)
        if err_message:
            return self.response.response_err(500, err_message)

        return self.response.response_ok(data)

    def find_one(self):
        name = get_id_by_token()
        if name is None:
            return self.response.response_err(401, "token is invalid")

        col = get_collection(did, app_id, content["collection"])
        if not col:
            return self.response.response_err(404, "collection not exist")

        options = options_filter(content, ("projection",
                                           "skip",
                                           "sort",
                                           "allow_partial_results",
                                           "return_key",
                                           "show_record_id",
                                           "batch_size"))
        if "sort" in options:
            sorts = gene_sort(options["sort"])
            options["sort"] = sorts

        try:
            if "filter" in content:
                result = col.find_one(convert_oid(content["filter"]), **options)
            else:
                result = col.find_one(**options)

            data = {"items": json.loads(json_util.dumps(result))}
            return self.response.response_ok(data)
        except Exception as e:
            return self.response.response_err(500, "Exception:" + str(e))

    def find_many(self):
        name = get_id_by_token()
        if name is None:
            return self.response.response_err(401, "token is invalid")

        options = populate_options_find_many(content)

        col = get_collection(did, app_id, content.get('collection'))
        if not col:
            return self.response.response_err(404, "collection not exist")

        data, err_message = query_find_many(col, content, options)
        if err_message:
            return self.response.response_err(500, err_message)

        return self.response.response_ok(data)