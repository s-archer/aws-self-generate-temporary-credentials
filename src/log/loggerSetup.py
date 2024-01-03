#!/usr/bin/env python

# Setup logging module for use

import os
import sys
import logging
import logging.config
import yaml

home = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logger_config = home + "/config/logger-config.yaml"

def configure(default_path=logger_config, default_level=logging.DEBUG, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
