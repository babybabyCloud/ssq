# encoding: utf-8

from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from threading import Lock

Base = declarative_base()
from Spider.dbmodels import * 

__engine = None
__lock = Lock()

def new_session(url):
    global __engine
    with __lock:
        if __engine is None:
            __engine = create_engine(url, echo=False)
            Base.metadata.create_all(__engine)
    return sessionmaker(bind=__engine)()


def get_engine():
    if __engine is None:
        raise NotInitializationError('Not initialize engine, please call new_session to initialize an enginre first')
    return __engine


class NotInitializationError(Exception):
    def __init__(self, message):
        self.message = message
