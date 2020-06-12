# encoding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from threading import Lock

Base = declarative_base()
__Session = None
__lock = Lock()


def new_session(url):
    global __Session
    with __lock:
        if __Session is None:
            engine = create_engine(url, echo=False)
            __Session = sessionmaker(engine)
            Base.metadata.create_all(engine)
        return __Session()
