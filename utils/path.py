import os,sys
import click
from utils.logging_setup import get_logger

logger = get_logger("frogfetch")
def get_project_root(self):
    # Always resolves to the directory containing frogfetch.py
    return os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))