# -*- encoding:utf-8 -*-

from enum import Enum

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
