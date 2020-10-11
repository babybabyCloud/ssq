# -*- encoding:utf-8 -*-

from abc import ABC
from dataclasses import dataclass
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

    @classmethod
    def name_to_value(cls, name) -> int:
        '''
            Get the value from this enum according to the name
        '''
        value_member = cls.__members__.get(name)
        if value_member is None:
            raise ValueError('No entry for %s' %name)
        return value_member.value


@dataclass(repr=True)
class ProcessContext:
    request: Dict[str, Any]
    response: Dict[str, Any]


class BaseProcessor(ABC):
    '''
        An abstract Processor.
        All processes need to implement this Base abstract class.
        All parameters and return value would be instored in the context.
        Many processors would be put in an iterable object as a chain.
    '''
    def __init__(self):
            self.context_data = ProcessContext(request=None, response=None)

    def execute(self) -> None:
        '''
            Main process
        '''
        pass

    @property
    def context_data(self) -> ProcessContext:
        return self._context

    @context_data.setter
    def context_data(self, context_data: ProcessContext) -> None:
        self._context = context_data
