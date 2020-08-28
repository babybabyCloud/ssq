# encoding: utf-8

from ..dboperator import Base
from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import InstrumentedAttribute


__all__ = ['tablemapping', 'RecordBase', 'RecordDetail', 'RecordDetails', 'RecordsMean']

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
    record_detail = relationship('RecordDetail', uselist=False, back_populates='record_base')
    records_mean = relationship('RecordsMean', back_populates='record_base')

    # headers for exporting as CSV headers
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
    record_base = relationship('RecordBase', uselist=False, back_populates='record_detail')
    record_details = relationship('RecordDetails', back_populates='record_detail')

    def __repr__(self):
        return "<record_detail(id=%s, week=%s, sales=%s, pool_money=%s, detail_link=%s)>" % (self.id, self.week, self.sales,
                self.pool_money, self.detail_link)


class RecordDetails(Base, TableFuncMixIn):
    __tablename__ = 'record_details'

    id = Column(Integer, ForeignKey('record_detail.id'), primary_key=True)
    type = Column(Integer, primary_key=True)
    type_num = Column(Integer)
    type_money = Column(Integer)
    record_detail = relationship('RecordDetail', uselist=False, back_populates='record_details')

    def __repr__(self):
        return "<record_details(id=%s, type=%s, type_num=%s, type_money=%s)>" % (self.id, self.type, self.type_num, self.type_money)


class RecordsMean(Base, TableFuncMixIn):
    __tablename__ = 'records_mean'

    id = Column(Integer, ForeignKey('record_base.id'), primary_key=True)
    mean1 = Column('mean_1', Float)
    mean2 = Column('mean_2', Float)
    mean3 = Column('mean_3', Float)
    mean4 = Column('mean_4', Float)
    mean5 = Column('mean_5', Float)
    mean6 = Column('mean_6', Float)
    mean_blue = Column(Float)
    type = Column(Integer, primary_key=True)
    record_base = relationship('RecordBase', uselist=False, back_populates='records_mean')

    def __repr__(self):
        return "<records_mean(id=%s, means=[%s, %s, %s, %s, %s, %s], mean_blue=%s, type=%s)>" % (self.id, self.mean1, 
                self.mean2, self.mean3, self.mean4, self.mean5, self.mean6, self.mean_blue, self.type)

tablemapping = {RecordBase.__tablename__: RecordBase, 
        RecordDetail.__tablename__: RecordDetail,
        RecordDetails.__tablename__: RecordDetails,
        RecordsMean.__tablename__: RecordsMean}
