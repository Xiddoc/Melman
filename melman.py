import os
import pathlib

from lib import arg_handling

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_FOLDER = pathlib.Path(os.getcwd()).name

if __name__ == '__main__':
    arg_handling.handle_args()
