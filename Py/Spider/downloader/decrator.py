# coding:utf-8
import functools
import sqlite3
import logging


logger = logging.getLogger('default')


def error_handler(func):
    @functools.wraps(func)
    def handle(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except sqlite3.IntegrityError as e:
            logger.debug('In {},'.format(func.__name__) + str(args) + ' has been in database')
        return result
    return handle
