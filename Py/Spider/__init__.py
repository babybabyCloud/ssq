# encoding: utf-8

from enum import Enum
import json
import logging
from logging.config import dictConfig


def get_file_name(file_path, target_name):
        import os.path
        from pathlib import PurePath
        directory = os.path.dirname(os.path.abspath(file_path))
        return PurePath(directory, target_name)


logger = logging.getLogger('default')

class SubCommandType(Enum):
    DOWNLOAD = 'download'
    EXPORT = 'export'