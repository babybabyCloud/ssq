# encoding: utf-8

import logging
from dataclasses import dataclass
from logging.config import dictConfig
from io import FileIO
from threading import Lock
from typing import Dict, List

from . import get_file_name


LOG_LEVEL_STR = 'log_level'
LOG_DEST_STR = 'log_dest'
LOG_CONFIG_PATH_STR = 'config_path'


@dataclass
class LogConfig:
    log_level: str = None
    log_path: str = None


class LoggerFactory:
    """
    The factory class to get Logger instance.
    """
    _config: Dict[str, Dict] = None
    __DEFAULT_CONFIG_FILE = 'logging.json'
    __LOGGERS_KEY = 'loggers'
    __LOCK = Lock()
    __init = False

    @classmethod
    def _init_log_config(cls, *, config_path: str = __DEFAULT_CONFIG_FILE, **kwargs) -> None:
        """
        Init the log config
        :param config_path: The full path of config file.
        """
        with cls.__LOCK:
            if cls.__init:
                return
            path = config_path
            if config_path == cls.__DEFAULT_CONFIG_FILE:
                path = str(get_file_name(__file__, config_path))
            with open(path) as f:
                cls._config = cls._read_config(f)
                dictConfig(cls._config)
            
            cls.log_config = LogConfig(**kwargs)
            cls._reconfig_logger()
            cls.__init == False

    
    @classmethod
    def get_logger(cls, name: str = "", /, **kwargs) -> logging.Logger:
        """
        Get the logger
        :param name: The name of logger
        """
        cls._init_log_config(**kwargs)

        logger_names: List[str] = list(
            sorted(
                filter(
                    lambda logger_name: name.startswith(logger_name), 
                    cls._config.get(cls.__LOGGERS_KEY).keys()
                ), 
            key=len)
        )

        # Get the correct logger
        logger = None
        if len(logger_names) == 0:
            logger = logging.getLogger('default')
        else:
            logger = logging.getLogger(name)
        return logger


    @classmethod
    def _reconfig_logger(cls) -> None:
        """
        The config could be overridden by CLI arguments or Environment variables.
        This will reset those values.
        """
        loggers = cls._config.get(cls.__LOGGERS_KEY)
        for logger_name in loggers.keys():
            logger = logging.getLogger(logger_name)
            log_level = cls.log_config.log_level
            if  log_level != None:
                logger.setLevel(log_level)
            for handler in logger.handlers:
                if log_level != None:
                    handler.setLevel(cls.log_config.log_level)
                if isinstance(handler, logging.StreamHandler):
                    if log_path := cls.log_config.log_path != None:
                        handler.setStream(open(log_path, 'a+'))
        

    @staticmethod
    def _read_config(config_file: FileIO) -> Dict[str, Dict]:
        """
        Read the config. This now only supports json format.
        :param config_file: The fd of the config file.
        :return: dict-like object
        """
        if config_file.name.endswith('json'):
            import json
            return json.load(config_file)
        return dict()