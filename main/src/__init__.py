import logging

from . import view
from .utils.constants import MODE_TEST

logging.getLogger().level = logging.INFO


def init_app(app, mode):
    logging.getLogger("Backend").info("##############################")
    logging.getLogger("Backend").info("Backend start")
    logging.getLogger("Backend").info("##############################")
    view.init_app(app)
