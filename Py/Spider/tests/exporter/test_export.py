# encoding: utf-8

import unittest
from Spider.exporter import Export

class ExportTest(unittest.TestCase):
    def test_extension_with(self):
        input = '/home/vagrant/helloworld.py'
        output = Export.extension(input)
        self.assertEqual('.py', output)

    def test_extension_without(self):
        input = '/home/vagrant/helloworld'
        output = Export.extension(input)
        self.assertEqual('', output)

    def test_outpath_with_ext(self):
        input = '/home/vagrant/helloworld.html'
        output = Export.outpath(input, '')
        self.assertEqual(input, output)

    def test_outpath_without_ext(self):
        input = '/home/vagrant/helloworld'
        output = Export.outpath(input, 'temp')
        self.assertEqual('%s/temp.csv' % input, output)
