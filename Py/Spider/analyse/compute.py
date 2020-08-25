# encoding: utf-8

from ..dboperator import *
from ..dbmodels.model import RecordBase
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session
from typing import Iterable, Tuple


__DEFAULT_LIMIT = 30


def compute_means(engine: Engine, limit: int = __DEFAULT_LIMIT)
    session = new_session_with_engine(engine)
    needed_computed_ids = read_neened_compute_data(limit, session)
    df = pd.read_sql_table(RecordBase.__table__.name, engine)
    means = list()
    for item in needed_computed_ids:
        mean = df.loc[df['ID'] < item].reset_index().loc[:__DEFAULT_LIMIT-1, 'RED_1':'BLUE'].mean()
        means.append(RecordsMean(id=item, mean1=mean['RED_1'r]), mean2=mean['RED_2'], mean3=mean['RED_3'], 
                                 mean4=mean['RED_4'], mean5=mean['RED_5'], mean6=mean['RED_6'], mean_blue=mean['BLUE'],
                                 type=limit)
    session.add_all(means)


def read_needed_compute_data(limit: int, session: Session) -> Iterable[int]:
    rb = session.query(RecordBase).order_by(RecordBase.id).offset(limit).limit(1).all()
    ids = session.query(RecordBase.id)
            .outerjoin(RecordsMean)
            .filter(RecordsMean.id == None)
            .order_by(RecordBase.id)
    return [inner for outer in ids for inner in outer]
