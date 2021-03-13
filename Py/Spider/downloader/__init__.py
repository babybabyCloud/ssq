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
    派奖一等奖特别奖 = 7
    派奖一等奖普惠奖 = 8
    派奖六等奖翻番奖 = 9

    @classmethod
    def name_to_value(cls, name) -> int:
        '''
            Get the value from this enum according to the name
        '''
        value_member = cls.__members__.get(name.replace(':', ''))
        if value_member is None:
            raise ValueError('No entry for %s' %name)
        return value_member.value
