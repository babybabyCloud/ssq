# coding:utf-8

from ..dbmodels import *
from sqlalchemy.orm.session import Session


class DbHandler:
    def insert_base(self, record_base: RecordBase, session):
        if session.query(RecordBase).filter(RecordBase.id == record_base.id).count() <= 0 :
            session.add(record_base)

    def insert_detail(self, record_detail: RecordDetail, session):
        if session.query(RecordDetail).filter(RecordDetail.id == record_detail.id).count() <= 0 :
            session.add(record_detail)

    def insert_details(self, record_details: RecordDetails, session):
        if session.query(RecordDetails) \
                .filter(RecordDetails.id == record_details.id) \
                .filter(RecordDetails.type == record_details.type) \
                .filter(RecordDetails.type_num == record_details.type_num) \
                .filter(RecordDetails.type_money == record_details.type_money) \
                .count() > 0:
            return
        session.add(record_details)

    def select_base_all(self, session: Session):
        return session.query(RecordBase).order_by(RecordBase.id).all()

def pop_file_with_pattern(path, pattern):
    import os
    import fnmatch
    import heapq
    sql_files = []
    for _, _, files in os.walk(path):
        for file in fnmatch.filter(files, pattern):
            heapq.heappush(sql_files, file)

    def get():
        for index in range(len(sql_files)):
            yield heapq.heappop(sql_files)

    return get
