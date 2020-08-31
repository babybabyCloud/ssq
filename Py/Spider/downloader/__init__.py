# -*- encoding:utf-8 -*-

from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict

from sqlalchemy.orm.session import Session


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


@dataclass(repr=True)
class ProcessContext:
    response: Dict[str, Any]
    session: Session
    request: Dict[str, Any] = dict()



class BaseProcessor(ABC):
    '''
        An abstract Processor.
        All processes need to implement this Base abstract class.
        All parameters and return value would be instored in the context.
        Many processors would be put in an iterable object as a chain.
    '''
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
