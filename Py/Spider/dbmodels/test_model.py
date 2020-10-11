# encoding: utf-8

import unittest
from datetime import datetime
from ..dboperator import new_session
from ..dbmodels import model

_MOMORY_SQL_URL = 'sqlite:///:memory:'


class TestTableFuncMixIn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = new_session(_MOMORY_SQL_URL)

    def test_columns(self):
        record_details = model.RecordDetails(id=1, type=2, type_num=3, type_money=10)
        self.assertEqual((1,None,2,10,3), record_details.columns())


class RecordBaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = new_session(_MOMORY_SQL_URL)

    def test_record_base(self):
        rb = model.RecordBase(id=-1, red1=1, red2=3, red3=10, red4=15, red5=16, red6=22, blue=8, 
                              date_=datetime.now().date())
        self.session.add(rb)
        self.session.commit()

        record = self.session.query(model.RecordBase).filter(model.RecordBase.id == -1).one()
        self.assertEqual(rb.red1, record.red1)


class RecordDetailTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = new_session(_MOMORY_SQL_URL)

    def test_record_detail(self):
        rd = model.RecordDetail(id=2019014, week='日', sales=327526362, pool_money=1364355844, detail_link='/c/2019-01-31/448988.shtml')
        self.session.add(rd)
        self.session.commit()

        for record in self.session.query(model.RecordDetail):
            self.assertEqual(rd.week, record.week)


class RecordDetailsTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.session = new_session(_MOMORY_SQL_URL)

    def test_record_details(self):
        rds = model.RecordDetails(id=2019014, type=1, type_num=12, type_money=6477986)
        self.session.add(rds)
        self.session.commit()

        for record in self.session.query(model.RecordDetails):
            self.assertEqual(rds.type_money, record.type_money)


class RecordsMeanTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.session = new_session(_MOMORY_SQL_URL)

    def test_records_mean(self):
        rb = model.RecordBase(id = -3, red1=1, red2=3, red3=10, red4=15, red5=16, red6=22, blue=8, date_=datetime.now().date())
        rm = model.RecordsMean(id=-3, mean1=1, mean2=2, mean3=3, mean4=4, mean5=5, mean6=6, mean_blue=8, type=30, 
                               record_base=rb)
        self.session.add(rm)
        self.session.commit()

        record = self.session.query(model.RecordsMean).filter(model.RecordsMean.id == -3).one()
        self.assertEqual(rm.type, record.type)
        self.assertEqual(rb.red3, record.record_base.red3)


