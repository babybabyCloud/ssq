# encoding: utf-8

import unittest
from .compute import compute_means


class ComputeTest(unittest.TestCase):
    def test_compute_means(self):
        compute_means()


if __name__ == '__main__':
    unittest.main()
