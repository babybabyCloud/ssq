# encoding: utf-8

import unittest
from unittest.mock import MagicMock
from .compute import *


_MEMORY_URL = 'sqlite:///:memory:'


class ComputeTest(unittest.TestCase):
    def test_compute_means(self):
        session = new_session(_MEMORY_URL)
        engine = get_engine()
        read_needed_compute_data = MagicMock(return_value=[1])
        df = pd.DataFrame(
            data={'ID': 1, 'RED_1': 2, 'RED_1': 1, 'RED_2': 2, 'RED_3': 3, 'RED_4': 4, 'RED_5': 5, 'RED_6': 6}    
        )
        pd.read_sql_table = MagicMock(return_value=)
        compute_means(engine)
        mean1 = session.query(RecordsMean.mean1).one()
        self.assertEquals(df['RED_1'], mean1.mean1)

    def test_read_needed_compute_data(self):
        session = new_session(_MEMORY_URL)
        rb = RecordBase(red1=1, red2=3, red3=10, red4=15, red5=16, red6=22, blue=8, date_=datetime.now().date())
        session.add(rb)
        ids = read_needed_compute_data(30, session)
        self.assertEquals(rb.red1, ids[0])

if __name__ == '__main__':
    unittest.main()
