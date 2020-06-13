# encoding: utf-8

from Spider.dboperator import Base
from sqlalchemy import Column, Integer, Date


__all__ = ["tablemapping", "RecordBase"]


class RecordBase(Base):
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

    def columns(self):
        return (self.id, self.red1, self.red2, self.red3, self.red4, self.red5, self.red6, self.blue, self.date_)

tablemapping = {RecordBase.__tablename__: RecordBase}