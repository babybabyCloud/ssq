# encoding: utf-8

from ..dboperator import Base
from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm.attributes import InstrumentedAttribute


__all__ = ["tablemapping", "RecordBase", "RecordDetail", "RecordDetails"]

class TableFuncMixIn:
    def columns(self):
        return tuple((getattr(self, attr) for attr in dir(self.__class__) if type(getattr(self.__class__, attr)) == InstrumentedAttribute))


class RecordBase(Base, TableFuncMixIn):
    __tablename__ = 'record_base'

    id = Column(Integer, primary_key=True)
    red1 = Column('red_1', Integer, nullable=False)
    red2 = Column('red_2', Integer, nullable=False)
    red3 = Column('red_3', Integer, nullable=False)
    red4 = Column('red_4', Integer, nullable=False)
    red5 = Column('red_5', Integer, nullable=False)
    red6 = Column('red_6', Integer, nullable=False)
    blue = Column(Integer, nullable=False)
    date_ = Column('date', Date, nullable=False)
    headers = ['ID', 'RED1', 'RED2', 'RED3', 'RED4', 'RED5', 'RED6', 'BLUE', 'DATE']

    def __repr__(self):
        return "<record_base(id=%s, red=[%s, %s, %s, %s, %s, %s], blue=%s, date=%s)>" % (self.id, self.red1, self.red2,
                self.red3, self.red4, self.red5, self.red6, self.blue, self.date_)


class RecordDetail(Base, TableFuncMixIn):
    __tablename__ = 'record_detail'

    id = Column(Integer, ForeignKey('record_base.id'), primary_key=True)
    week = Column(String(8))
    sales = Column(Integer)
    pool_money = Column(Integer)
    detail_link = Column(String(255))

    def __repr__(self):
        return "<record_detail(id=%s, week=%s, sales=%s, pool_money=%s, detail_link=%s)>" % (self.id, self.week, self.sales,
                self.pool_money, self.detail_link)


class RecordDetails(Base, TableFuncMixIn):
    __tablename__ = 'record_details'

    id = Column(Integer, ForeignKey('record_detail.id'), primary_key=True)
    type = Column(Integer, primary_key=True)
    type_num = Column(Integer)
    type_money = Column(Integer)

    def __repr__(self):
        return "<record_details(id=%s, type=%s, type_num=%s, type_money=%s)>" % (self.id, self.type, self.type_num, self.type_money)

tablemapping = {RecordBase.__tablename__: RecordBase, 
        RecordDetail.__tablename__: RecordDetail,
        RecordDetails.__tablename__: RecordDetails}
