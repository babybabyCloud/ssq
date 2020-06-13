# encoding: utf-8

from Spider.dboperator import new_session
from Spider .dboperator.model import RecordBase


def main(db_file):
    session = new_session()
    session.query(RecordBase)