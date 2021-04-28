from pymongo import MongoClient

from main.src.utils.constants import *


def save_info(name, password):
    connection = MongoClient()
    db = connection[ID_INFO_DB_NAME]
    col = db[ID_INFO_REGISTER_COL]
    info_doc = {ID_INFO_REGISTER_NAME: name, ID_INFO_REGISTER_PASSWORD: password}
    return col.insert_one(info_doc)


def get_info(name):
    connection = MongoClient()
    db = connection[ID_INFO_DB_NAME]
    col = db[ID_INFO_REGISTER_COL]
    query = {ID_INFO_REGISTER_NAME: name}
    return col.find_one(query)


def update_pwd(name, password):
    connection = MongoClient()
    db = connection[ID_INFO_DB_NAME]
    col = db[ID_INFO_REGISTER_COL]
    query = {ID_INFO_REGISTER_PASSWORD: password}
    value = {"$set": {ID_INFO_REGISTER_NAME: name, ID_INFO_REGISTER_PASSWORD: password}}
    return col.update_one(query, value)
