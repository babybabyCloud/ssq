# encoding: utf-8

import unittest
from . import DBHandler
from . import new_session
import datetime
from ..dbmodels import *

class DBHandlerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = new_session('sqlite:///:memory:')

    def test_insert_base(self):
        record_base = RecordBase(id=-2, red1=1, red2=2, red3=3, red4=4, red5=5, red6=6, blue=7, date_=datetime.datetime.now())
        DBHandler.insert_base(record_base, self.session)
        self.session.commit()
        record = self.session.query(RecordBase).filter(RecordBase.id == -2).one()
        self.assertEqual(2, record.red2)

if __name__ == '__main__':
    unittest.main()
