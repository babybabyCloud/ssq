# coding:utf-8
from __init__ import error_handler
import sqlite3


class DbHandler:
    def __init__(self, conf):
        self.conn = sqlite3.connect(conf['db']['location'])

    @error_handler
    def insert_base(self, identify, r1, r2, r3, r4, r5, r6, blue, date):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO record_base(ID, RED_1, RED_2, RED_3, RED_4, RED_5, RED_6, BLUE, "DATE") VALUES(
                    ?, ?, ?, ?, ?, ?, ?, ?, ?);''', (identify, r1, r2, r3, r4, r5, r6, blue, date)
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
            return None
        cur.execute('''INSERT INTO record_details(ID, TYPE, TYPE_NUM, TYPE_MONEY) VALUES(
            ?, ?, ?, ?);''', (identify, tp, type_num, money))
        self.conn.commit()

