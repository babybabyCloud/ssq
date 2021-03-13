# encoding: utf-8

from datetime import date, datetime
from enum import Enum
from typing import Coroutine, List

import asyncio


_DATE_FORMAT = '%Y-%m-%d'


def get_file_name(file_path, target_name):
    import os.path
    from pathlib import PurePath
    directory = os.path.dirname(os.path.abspath(file_path))
    return PurePath(directory, target_name)


def strptime(date_string, format=_DATE_FORMAT) -> date:
    """
    Covert a date string to date according to the format string.
    :param date_string: The string to be converted.
    :param format: The date format.
    """
    return datetime.strptime(date_string, format).date()


class SubCommandType(Enum):
    DOWNLOAD = 'download'
    EXPORT = 'export'


async def run_async(aws: List[Coroutine]):
    """
    A wrapper for asyncio.gather

    :param aws: A list of coroutine
    """
    await asyncio.gather(*aws)