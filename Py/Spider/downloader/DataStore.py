# encoding: utf-8

from . import BaseProcessor
from ..dbmodels import RecordBase, RecordDetail
from ..dboperator.DBHandler import insert_base, insert_detail
from datetime import datetime

class BasePageDataStore(BaseProcessor):
    def execute(self):
        self.context_data.response = list()
        for row in self.context_data.request.data:
            record_base = RecordBase(id=row.id, red1=row.reds[0], red2=row.reds[1], red3=row.reds[2], red4=row.reds[3],
                    red5=row.reds[4], red6=row.reds[5], blue=row.blue[0], \
                    date_=datetime.strptime(row.date[:-3], '%Y-%m-%d'))
            insert_base(record_base, self.context_data.session)
            insert_detail(RecordDetail(id=row.id, week=row.date[-2:-1], sales=row.total, pool_money=row.pool))
            self.context_data.response.append(record_base)