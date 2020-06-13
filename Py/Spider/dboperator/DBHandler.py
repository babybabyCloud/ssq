# coding:utf-8

import sqlite3
import Spider
import os.path
from Spider.downloader.decrator import error_handler


class DbHandler():
    @error_handler
    def insert_base(self, identify, reds, blue, date):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO record_base(ID, RED_1, RED_2, RED_3, RED_4, RED_5, RED_6, BLUE, "DATE") VALUES(
            ?, ?, ?, ?, ?, ?, ?, ?, ?);''', (identify, *reds, *blue, date)
        )
        self.conn.commit()

    @error_handler
    def insert_detail(self, identify, week, sales, money, link):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO record_detail(ID, WEEK, SALES, POOL_MONEY, DETAIL_LINK) VALUES(
            ?, ?, ?, ?, ?);''', (identify, week, sales, money, link))
        self.conn.commit()

    @error_handler
    def insert_details(self, identify, tp, type_num, money):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM record_details WHERE ID = ? AND TYPE = ? AND TYPE_NUM = ? AND 
            TYPE_MONEY = ?''', (identify, tp, type_num, money))
        if cur.fetchone():
            return
        cur.execute('''INSERT INTO record_details(ID, TYPE, TYPE_NUM, TYPE_MONEY) VALUES(
            ?, ?, ?, ?);''', (identify, tp, type_num, money))
        self.conn.commit()

    def init_db(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM SQLITE_MASTER WHERE tbl_name = ?;''', ('record_base',))
        if not cur.fetchone():
            for sql_file in pop_file_with_pattern(os.path.join(Spider.__path__[0], 'SQLite/SQL'), '*.sql')():
                with open(sql_file) as sql_f:
                    cur.executescript(sql_f.read())


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
