# encoding: utf-8

import unittest
from datetime import datetime
from Spider.dboperator import new_session
from Spider.dbmodels import model

class TestTableFuncMixIn(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.session = new_session('sqlite:///:memory:')

    def test_columns(self):
        record_details = model.RecordDetails(id=1, type=2, type_num=3, type_money=10)
        self.assertEqual((1,2,10, 3), record_details.columns())


class RecordBaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.session = new_session('sqlite:///:memory:')

    def test_record_base(self):
        rb = model.RecordBase(red1=1, red2=3, red3=10, red4=15, red5=16, red6=22, blue=8, date_=datetime.now().date())
        self.session.add(rb)
        self.session.commit()

        for record in self.session.query(model.RecordBase):
            self.assertEquals(rb.red1, record.red1)


