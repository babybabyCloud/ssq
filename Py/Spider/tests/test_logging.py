# encoding: utf-8

import logging

import unittest
from ..logging import LoggerFactory


class LoggerFactoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        LoggerFactory.init_log_config()


    def test_get_root_logger(self) -> None:
        root_logger = LoggerFactory.get_logger('default')

        self.assertTrue(isinstance(root_logger.handlers[0], logging.StreamHandler))

    
    def test_get_logger(self) -> None:
        logger = LoggerFactory.get_logger(__name__)

        self.assertEqual(2, len(logger.parent.handlers))