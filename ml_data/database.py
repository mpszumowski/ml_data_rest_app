from flask import g
from werkzeug.local import LocalProxy
from pymongo import MongoClient


class MongoCfg:
    client = dict(host='mongo', port=27017)
    db_name = 'ml_data'


def _get_flask_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = MongoClient(
            **MongoCfg.client)[MongoCfg.db_name]
    return db


db = LocalProxy(_get_flask_db)
