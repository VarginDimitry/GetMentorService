import argparse
import sys
from pprint import pprint

from flask import Flask, render_template
from app import app
from app.handlers import *
from utils import ErrorManager

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
    '--config_name',
    type=str,
    default='Config',
    help='See a file ./utils/configs.py and choose a suitable config class\nExamples:\nConfig\nDockerConfig\n'
)


def main():
    argv = parser.parse_args()
    app.config.from_object(f'utils.configs.{argv.config_name}')
    ErrorManager.init_class()


if __name__ == '__main__':
    main()
    app.run(host="0.0.0.0", debug=True)
