# encoding: utf-8

from . import BaseProcessor
from .PageParser import SSQDetails
from .. import logger
from ..dbmodels import RecordBase, RecordDetail
from ..dboperator.DBHandler import insert_base, insert_detail
from datetime import datetime
from typing import List
from sqlalchemy.orm.session import Session


class DataStore(BaseProcessor):
    def __init__(self, session: Session):
        super().__init__()
        self._session = session

    def execute(self) -> None:
        logger.debug('Preparing insert record %s' %self.context_data.request.get('data'))
        self.store_record(**self.context_data.request)

    def store_record(self, **kwargs) -> None:
        pass


class BasePageDataStore(DataStore):
    def store_record(self, data: List[RecordBase]) -> None:
        self.context_data.response = dict()
        self.context_data.response.setdefault('details', list())
        for row in data:
            record_base = RecordBase(id=row.id, blue=row.blue[0], date_=datetime.strptime(row.date[:-3], '%Y-%m-%d'))
            record_base.red1, record_base.red2, record_base.red3, record_base.red4, record_base.red5, \
                    record_base.red6 = row.reds
            insert_base(record_base, self._session)
            record_detail = RecordDetail(id=row.id, week=row.date[-2:-1], sales=row.total, pool_money=row.pool, \
                    detail_link=row.detail_link)
            insert_detail(record_detail, self._session)
            logger.debug('Insert record_base %s and record_details %s' %(record_base, record_detail))
            details = SSQDetails(id=record_detail.id, link=record_detail.detail_link, type=None, type_num=None, \
                    type_money=None)
            self.context_data.response.get('details').append(details)
        self.context_data.response['element_cls'] = 'zjqk'
