# encoding: utf-8

import logging

import unittest
from .logging import LoggerFactory


class LoggerFactoryTest(unittest.TestCase):
    def test_init_log_config(self):
        LoggerFactory.init_log_config()
        logger = logging.getLogger()

        self.assertEqual(logger.level, logging.INFO)