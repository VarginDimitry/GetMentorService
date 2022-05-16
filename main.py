import argparse
import logging
import sys
from pprint import pprint

from flask import Flask, render_template
from app import app
from utils import ErrorManager, configs
from utils.MongoConnector import MongoConnector


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
        '--config_name',
        type=str,
        default='Config',
        help='See a file ./utils/configs.py and choose a suitable config class\nExamples:\nConfig\nDockerConfig\n'
    )

    argv = parser.parse_args()
    # app.logger.info(f"__name__ ={getattr(configs, argv.config_name).__name__}")
    # app.logger.info(f"__name__ = {getattr(configs, argv.config_name).MONGO_CONFIG}")
    # print(f"Config name: {argv.config_name}")
    app.config.from_object(getattr(configs, argv.config_name))
    pprint(app.config)
    ErrorManager.init_class()


if __name__ == '__main__':
    main()
    from app.handlers import *
    app.run(host="0.0.0.0", debug=True)
