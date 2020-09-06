# coding:utf-8

from ..dbmodels import *
from sqlalchemy.orm.session import Session


def insert_base(record_base: RecordBase, session: Session):
    if session.query(RecordBase).filter(RecordBase.id == record_base.id).count() <= 0 :
        session.add(record_base)

def insert_detail(record_detail: RecordDetail, session: Session):
    if session.query(RecordDetail).filter(RecordDetail.id == record_detail.id).count() <= 0 :
        session.add(record_detail)

def insert_details(record_details: RecordDetails, session: Session):
    if session.query(RecordDetails) \
            .filter(RecordDetails.id == record_details.id) \
            .filter(RecordDetails.type == record_details.type) \
            .filter(RecordDetails.type_num == record_details.type_num) \
            .filter(RecordDetails.type_money == record_details.type_money) \
            .count() > 0:
        return
    session.add(record_details)

def select_base_all(session: Session):
    return session.query(RecordBase).order_by(RecordBase.id).all()