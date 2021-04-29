from pymongo import MongoClient

from main.src.utils.constants import *


def save_info(name, password):
    connection = MongoClient()
    db = connection[DB_NAME]
    col = db[COL_NAME]
    info_doc = {REGISTER_NAME_KEY: name, REGISTER_PASSWORD_KEY: password}
    return col.insert_one(info_doc)


def get_info(name):
    connection = MongoClient()
    db = connection[DB_NAME]
    col = db[COL_NAME]
    query = {REGISTER_NAME_KEY: name}
    return col.find_one(query)


def update_pwd(name, password):
    connection = MongoClient()
    db = connection[DB_NAME]
    col = db[COL_NAME]
    query = {REGISTER_PASSWORD_KEY: password}
    value = {"$set": {REGISTER_NAME_KEY: name, REGISTER_PASSWORD_KEY: password}}
    return col.update_one(query, value)
