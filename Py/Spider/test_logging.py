# encoding: utf-8

import logging

import unittest
from .logging import LoggerFactory


class LoggerFactoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        LoggerFactory.init_log_config()


    def test_init_log_config(self) -> None:
        logger = logging.getLogger()

        self.assertEqual(logger.level, logging.INFO)


    def test_get_root_logger(self) -> None:
        root_logger = LoggerFactory.get_logger()

        self.assertTrue(isinstance(root_logger.handlers[0], logging.StreamHandler))