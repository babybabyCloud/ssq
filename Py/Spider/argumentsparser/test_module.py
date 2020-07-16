# encoding: utf-8

import unittest
from Spider.argumentsparser import DownloadSubCommand, ExportSubCommand


class DownloadTest(unittest.TestCase):
    def test_extract(self):
        dsc = DownloadSubCommand()
        result = dsc.extract('--db-file abcd --query-count 50'.split())
        self.assertEqual('50', result.query_count)


class ExportTest(unittest.TestCase):
    def test_extract(self):
        esc = ExportSubCommand()
        before = '2020-01-04'
        after = '2019-10-28'
        limit = 10
        table = 'record_base'
        result = esc.extract('--db-file {4} --before {0} --after {1} --limit {2} {3}'.format(
            *(before,
            after,
            limit,
            table,
            'abc')
        ).split())
        self.assertEqual(before, str(result.before))
        self.assertEqual(after, str(result.after))
        self.assertEqual(limit, result.limit)
        self.assertEqual(table, result.table)
        self.assertEqual('.', result.out)


if __name__ == '__main__':
    unittest.main()
