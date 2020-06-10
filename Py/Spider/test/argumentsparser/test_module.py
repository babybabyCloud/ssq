# encoding: utf-8

import unittest
from Spider.argumentsparser import DownloadSubCommand


class DownloadTest(unittest.TestCase):
    def test_extract(self):
        dsc = DownloadSubCommand()
        result = dsc.extract('--db-file abcd --query-count 50'.split())
        self.assertEqual('50', result.query_count)



if __name__ == '__main__':
    unitest.main()
