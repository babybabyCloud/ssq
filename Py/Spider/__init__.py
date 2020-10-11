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


with open(str(get_file_name(__file__, 'logging.json'))) as f:
    config = json.load(f)
    dictConfig(config)

logger = logging.getLogger('default')

class SubCommandType(Enum):
    DOWNLOAD = 'download'
    EXPORT = 'export'