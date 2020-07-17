# coding:utf-8

import Spider
import os.path
from Spider.downloader.decrator import error_handler
from Spider.dbmodels import *


class DbHandler:
    @error_handler
    def insert_base(self, identify, reds, blue, date, session):
        record = RecordBase(id=identify, red1=reds[0], red2=reds[1], red3=reds[2], red4=reds[3], red5=reds[4], red6=reds[5],
            blue=blue, date_=date)
        session.add(record)

    @error_handler
    def insert_detail(self, identify, week, sales, money, link, session):
        record = RecordDetail(id=identify, week=week, sales=sales, pool_money=money, detail_link=link)
        session.add(record)

    @error_handler
    def insert_details(self, identify, tp, type_num, money, session):
        if session.query(RecordDetails) \
                .filter(RecordDetails.id == identify) \
                .filter(RecordDetails.type == tp) \
                .filter(RecordDetails.type_num == type_num) \
                .filter(RecordDetails.type_money == money) \
                .count() > 0:
            return
        record = RecordDetails(id=identify, type=tp, type_num=type_num, type_money=money)
        session.add(record)


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
