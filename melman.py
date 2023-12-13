import os

from lib import arg_handling

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# TODO Better README
# TODO move files to commons
if __name__ == '__main__':
    arg_handling.handle_args()
