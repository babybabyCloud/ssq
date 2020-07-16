# encoding: utf-8

import unittest
from Spider.dboperator import new_session
from Spider.dbmodels import model

class TestTableFuncMixIn(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.session = new_session('sqlite:///:memory:')

    def test_columns(self):
        record_details = model.RecordDetails(id=1, type=2, type_num=3, type_money=10)
        self.assertEqual((1,2,10, 3), record_details.columns())
