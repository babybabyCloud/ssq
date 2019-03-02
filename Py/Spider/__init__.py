# coding:utf-8
import functools
import sqlite3
import logging


logger = logging.getLogger('log_default')

def error_handler(func):
    @functools.wraps(func)
    def handle(*args):
        result = None
        try:
            result = func(*args)
        except sqlite3.IntegrityError as e:
            logger.info('In {},'.format(func.__name__) + str(args) + ' has been in database')
        return result
    return handle
