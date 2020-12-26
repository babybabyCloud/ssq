# encodig: utf-8

import unittest

from Spider.tests.test_logging import LoggerFactoryTest
from Spider.tests.analyse.test_compute import Compute1MeanTest, Compute2BaseInfoTest
from Spider.tests.dbmodels.test_model import TestTableFuncMixIn, RecordBaseTest, RecordDetailTest, RecordDetailsTest, RecordsMeanTest, \
    RecordDataTest
from Spider.tests.dboperator.test_DBHandler import DBHandlerTest
from Spider.tests.exporter.test_export import ExportTest


if __name__ == '__main__':
    suite = unittest.TestSuite()
    test_cases = [LoggerFactoryTest('test_get_root_logger'),
                  LoggerFactoryTest('test_get_logger'),
                  Compute2BaseInfoTest('test_compute_data'),
                  Compute1MeanTest('test_2_compute_means'),
                  Compute1MeanTest('test_1_read_needed_compute_data'),
                  TestTableFuncMixIn('test_columns'), 
                  RecordBaseTest('test_record_base'), 
                  RecordDetailTest('test_record_detail'), 
                  RecordDetailsTest('test_record_details'), 
                  RecordsMeanTest('test_records_mean'),
                  RecordDataTest('test_record_data'),
                  DBHandlerTest('test_insert_base'), 
                  ExportTest('test_extension_with'),
                  ExportTest('test_extension_without'), 
                  ExportTest('test_outpath_with_ext'), 
                  ExportTest('test_outpath_without_ext')]

    suite.addTests(test_cases)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
