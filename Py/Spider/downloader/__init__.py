# -*- encoding:utf-8 -*-

from enum import Enum

class QueryCountEnum(Enum):
    LOW = '30'
    MEDIUM = '50'
    HIGHT = '100'

def get_file_name(file_path, target_name):
        import os.path
        from pathlib import PurePath
        directory = os.path.dirname(os.path.abspath(file_path))
        return PurePath(directory, target_name)