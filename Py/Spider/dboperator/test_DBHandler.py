# encoding: utf-8

import unittest
from ..dboperator.DBHandler import DbHandler
import Spider.dboperator as dbop
import datetime
from ..dbmodels import *

class DBHandlerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = dbop.new_session('sqlite:///:memory:')
        cls.dbh = DbHandler()

    def test_insert_base(self):
        self.dbh.insert_base(2, [1,2,3,4,5,6], 10, datetime.datetime.now(), self.session)
        self.session.commit()
        record = self.session.query(RecordBase).first()
        self.assertEqual(1, record.id)

if __name__ == '__main__':
    unittest.main()