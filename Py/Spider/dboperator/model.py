# encoding: utf-8

from Spider.dboperator import Base
from sqlalchemy import Column, Integer, Date

class RecordBase(Base):
    __tablename__ = 'record_base'

    id = Column(Integer, primary_key=True)
    red1 = Column(Integer)
    red2 = Column(Integer)
    red3 = Column(Integer)
    red4 = Column(Integer)
    red5 = Column(Integer)
    red6 = Column(Integer)
    blue = Column(Integer)
    date_ = Column(Date)

    def __repr__(self):
        return "<record_base(id=%s, red=[%s, %s, %s, %s, %s, %s], blue=%s, date=%s)>" % (self.id, self.red1, self.red2,
                self.red3, self.red4, self.red5, self.red6, self.blue, self.date_)
