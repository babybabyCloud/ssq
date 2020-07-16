# encoding: utf-8

from datetime import datetime
import unittest
from Spider.dboperator import Base, new_session
from Spider.dboperator.model import RecordBase


class RecordBaseTest(unittest.TestCase):
    def test_record_base(self):
        session = new_session('sqlite:///:memory:')
        rb = RecordBase(red1=1, red2=3, red3=10, red4=15, red5=16, red6=22, blue=8, date_=datetime.now().date())
        session.add(rb)
        session.commit()

        for record in session.query(RecordBase):
            self.assertEquals(rb.red1, record.red1)


if __name__ == '__main__':
    unittest.main()
