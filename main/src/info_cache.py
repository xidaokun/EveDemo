import uuid

from pymongo import MongoClient

from main.src.utils.constants import *


def save_info_to_db(name, password):
    connection = MongoClient()
    db = connection[ID_INFO_DB_NAME]
    col = db[ID_INFO_REGISTER_COL]
    info_doc = {"_id": name, ID_INFO_REGISTER_PASSWORD: password, ID_INFO_REGISTER_TOKEN: None}
    return col.insert_one(info_doc)


def get_info_by_name(name):
    connection = MongoClient()
    db = connection[ID_INFO_DB_NAME]
    col = db[ID_INFO_REGISTER_COL]
    query = {"_id": name}
    return col.find_one(query)


def save_token_to_db(name, token):
    connection = MongoClient()
    db = connection[ID_INFO_DB_NAME]
    col = db[ID_INFO_REGISTER_COL]
    query = {"_id": name}
    value = {"$set": {ID_INFO_REGISTER_TOKEN: token}}
    return col.update_one(query, value)


def get_info_by_token(token):
    connection = MongoClient()
    db = connection[ID_INFO_DB_NAME]
    col = db[ID_INFO_REGISTER_COL]
    query = {ID_INFO_REGISTER_TOKEN: token}
    return col.find_one(query)


def create_token():
    token = uuid.uuid1()
    return str(token)

