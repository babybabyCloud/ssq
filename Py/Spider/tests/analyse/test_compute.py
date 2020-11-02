# encoding: utf-8

import csv
import unittest
from Spider.logging import LoggerFactory
# Init logger for UT.
LoggerFactory.init_log_config()

from Spider import get_file_name, strptime
from Spider.analyse.compute import *


_MEMORY_URL = 'sqlite:///:memory:'


class ComputeMeanTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rbs = list()
        with open(get_file_name(__file__, 'record_base.csv')) as f:
            data = csv.reader(f)
            # skip the header
            next(data)
            for item in data:
                rbs.append(RecordBase(id=item[0], red1=item[1], red2=item[2], red3=item[3], red4=item[4], red5=item[5],
                                red6=item[6], blue=item[7], date_=strptime(item[8])))
        cls.session = new_session(_MEMORY_URL)
        cls.session.add_all(rbs)
        cls._default_limit = 30
        cls.session.commit()
        cls.mean = ComputeMean(get_engine(), cls._default_limit)
        # cls.session.delete(cls.session.query(RecordBase).filter(RecordBase.id == -2).one())

    # unittest will run the test case by method name with ASCII order, this method need run after 
    # test_1_read_needed_compute_data, so add a '2' in the method name
    def test_compute_means(self):
        csv_data = list()
        with open(get_file_name(__file__, 'record_base.csv')) as f:
            data = csv.reader(f)
            # skip the header
            next(data)
            for item in data:
                csv_data.append(item)
        self.mean.compute_means()
        # calculate the data from csv
        for item in self.session.query(RecordsMean.id, RecordsMean.mean1).all():
            sum = 0
            hit = 0 
            for csv_row in reversed(csv_data):
                if int(csv_row[0]) == item[0] or sum != 0:
                    sum += int(csv_row[1])
                    hit += 1
                if hit == self._default_limit:
                    break
            # Compare the mean calculated by above to read from table
            self.assertEqual(sum / self._default_limit, item[1])
            # Won't test for error scenario

    def test_read_needed_compute_data(self):
        self.assertEqual([2018098, 2018099, 2019001], self.mean.read_needed_compute_data(self.session))


class ComputeBaseInfoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._engine = get_engine()
        cls.cbi = ComputeBaseInfo(cls._engine)

    def test_record_data(self):
        self.cbi.compute()
        rd = new_session_with_engine(self._engine).query(RecordData).filter(RecordData.id == 2018097).one()
        self.assertEqual(2, rd.red_part_low)