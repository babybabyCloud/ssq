# encoding: utf-8

import json
import logging
import re
from logging.config import dictConfig
from threading import Lock
from typing import Mapping, List

from . import get_file_name


class LoggerFactory:
    config: Mapping[str, Mapping] = None
    logger_register = set()
    _lock =  Lock()
    __DEFAULT_CONFIG_FILE = 'logging.json'
    __LOGGERS_KEY = 'loggers'

    @classmethod
    def init_log_config(cls, config_path: str = __DEFAULT_CONFIG_FILE, /) -> None:
        """
        Init the log config
        :param config_path: The full path of config file.
        """
        path = config_path
        if config_path == cls.__DEFAULT_CONFIG_FILE:
            path = str(get_file_name(__file__, config_path))
        with open(path) as f:
            cls.config = json.load(f)
            dictConfig(cls.config)

    
    @classmethod
    def get_logger(cls, name: str, /, **kwargs) -> logging.Logger:
        """
        Get the logger
        :param name: The name of logger
        """
        assert cls.config != None, '"LoggerFactory.init_log_config" must be called first'

        logger_names: List[str] = list(
            sorted(
                filter(
                    lambda logger_name: name.startswith(logger_name), 
                    cls.config.get(cls.__LOGGERS_KEY).keys()
                ), 
            key=len)
        )

        # Get the correct logger
        logger = None
        if len(logger_names) == 0:
            logger = logging.getLogger()
        else:
            parent_logger_name = logger_names.pop()
            match_name = f"{parent_logger_name}.".repalce('.', '\.')
            prefix_regexp = re.compile(match_name)
            child_logger_name_suffix = prefix_regexp.sub('', name, 1)
            parent_logger = logging.getLogger(parent_logger_name)
            logger = parent_logger.getChild(child_logger_name_suffix)
            cls.configure_parent_logger(logger, **kwargs)
            cls.configure_logger(parent_logger, logger)
        return logger
        

    @classmethod
    def configure_parent_logger(cls, logger: logging.Logger, **kwargs) -> None:
        """
        Configure the logger.
        :param logger: The logger to be configured
        :param log_level: The log level is configured to the logger
        :param log_path: The log path is configured to the logger is the logger is a logging.FileHandler
        """
        with cls._lock:
            if logger not in cls.logger_register:
                log_level = kwargs.get('log_level')
                if log_level != None:
                    logger.setLevel(log_level)
                if log_des := kwargs.get('log_des') != None:
                    for handler in filter(lambda h: isinstance(h, logging.FileHandler), logger.handlers):
                        handler.stream = open(log_des, 'a+')
                        handler.setLevel(log_level)
                cls.logger_register.add(logger)
    

    @staticmethod
    def configure_logger(parent: logging.Logger, child: logging.Logger) -> None:
        """
        Copy the attributes from parent to child
        :param parent: The parent
        :param child: The child
        """
        for attr in ["level", "propagate", "filters", "handlers"]:
            setattr(child, attr, getattr(parent, attr))
        # child.setLevel(parent.level)
        # child.propagate = parent.propagate
        # child.filters = parent.filters
        # child.handlers = parent.handlers