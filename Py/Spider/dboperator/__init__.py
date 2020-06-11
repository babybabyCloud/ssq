# encoding: utf-8

import sqlite3


class Base:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)

    def __del__(self):
        if self.conn:
            self.conn.close()

