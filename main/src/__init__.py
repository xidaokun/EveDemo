import logging

from . import view
from .utils.constants import MODE_TEST

logging.getLogger().level = logging.INFO


def init_app(app, mode):
    logging.getLogger("Hive").info("##############################")
    logging.getLogger("Hive").info("HIVE BACK-END IS STARTING")
    logging.getLogger("Hive").info("##############################")
    view.init_app(app)
