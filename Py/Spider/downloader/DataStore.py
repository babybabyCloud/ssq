# encoding: utf-8

from Spider.logging import LoggerFactory
from . import BaseProcessor
from .PageParser import SSQData, SSQDetails
from ..dbmodels import RecordBase, RecordDetail, RecordDetails
from ..dboperator.DBHandler import insert_base, insert_detail, insert_details
from datetime import datetime
from typing import List
from sqlalchemy.orm.session import Session


logger = LoggerFactory.get_logger(__name__)


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
    def store_record(self, data: List[SSQData]) -> None:
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


class DetailsPageDataStore(DataStore):
    def store_record(self, data: List[SSQDetails]) -> None:
        for item in data:
            record_details = RecordDetails(id=item.id, type=item.type, type_num=item.type_num, 
                    type_money=item.type_money)
            insert_details(record_details, self._session)
            logger.debug('Insert record_details %s' %record_details)