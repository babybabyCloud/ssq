# encoding: utf-8

from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from threading import Lock

Base = declarative_base()
__Session = None
__engine = None
__lock = Lock()


def init_database(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        Base.metadata.create_all(__engine)
        return result
    return wrapper

@init_database
def new_session(url):
    global __Session
    global __engine
    with __lock:
        if __Session is None:
            __engine = create_engine(url, echo=False)
            __Session = sessionmaker(__engine)
        return __Session()
