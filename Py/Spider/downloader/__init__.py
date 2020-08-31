# -*- encoding:utf-8 -*-

from abc import ABC
from enum import Enum
from typing import Any, Dict

class QueryCountEnum(Enum):
    LOW = '30'
    MEDIUM = '50'
    HIGHT = '100'


class AwardLevel(Enum):
    一等奖 = 1
    二等奖 = 2
    三等奖 = 3
    四等奖 = 4
    五等奖 = 5
    六等奖 = 6


class ProcessRequest:
    pass

class BaseProcessor(ABC):
    def execute(self) -> Any:
        '''
            Main process
        '''
        pass

    @property
    def context_data(self) -> Dict:
        return self._data

    @context_data.setter
    def context_data(self, context_data) -> None:
        self._data = context_data
