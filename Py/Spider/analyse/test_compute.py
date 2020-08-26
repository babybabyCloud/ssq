# encoding: utf-8

import csv
import unittest
from .compute import *
from .. import get_file_name
from ..argumentsparser import strptime


_MEMORY_URL = 'sqlite:///:memory:'


class ComputeTest(unittest.TestCase):
    def setUp(self):
        rbs = list()
        with open(get_file_name(__file__, 'record_base.csv')) as f:
            data = csv.reader(f)
            # skip the header
            next(data)
            for item in data:
                rbs.append(RecordBase(id=item[0], red1=item[1], red2=item[2], red3=item[3], red4=item[4], red5=item[5], 
                                red6=item[6], blue=item[7], date_=strptime(item[8])))
        self.session = new_session(_MEMORY_URL)
        self.session.add_all(rbs)
        self._default_limit = 30

    def test_compute_means(self):
        engine = get_engine()
        compute_means(engine, self._default_limit)
        print(self.session.querr(RecordsMean.mean1).all())

    def test_read_needed_compute_data(self):
        self.assertEquals([2018098], read_needed_compute_data(self._default_limit, self.session))
        

if __name__ == '__main__':
    unittest.main()
