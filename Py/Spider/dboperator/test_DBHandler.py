# encoding: utf-8

import unittest
from .DBHandler import DbHandler
from . import new_session
import datetime
from ..dbmodels import *

class DBHandlerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = new_session('sqlite:///:memory:')
        cls.dbh = DbHandler()

    def test_insert_base(self):
        record_base = RecordBase(id=2, red1=1, red2=2, red3=3, red4=4, red5=5, red6=6, blue=7, date_=datetime.datetime.now())
        self.dbh.insert_base(record_base, self.session)
        self.session.commit()
        record = self.session.query(RecordBase).first()
        self.assertEqual(1, record.id)

if __name__ == '__main__':
    unittest.main()
