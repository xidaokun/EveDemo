#!/usr/bin/env python
# coding=utf-8
import logging.config

import yaml
from flask_script import Manager, Server

from main import create_service

logging.config.dictConfig(yaml.load(open('logging.conf'), Loader=yaml.FullLoader))
logfile = logging.getLogger('file')
log_console = logging.getLogger('console')
logfile.debug("Debug FILE")
log_console.debug("Debug CONSOLE")

app = create_service()
manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))
manager.add_option('-c', '--config', dest='mode', required=False)

if __name__ == "__main__":
    manager.run()

