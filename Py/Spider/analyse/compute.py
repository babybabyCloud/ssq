# encoding: utf-8

from .. import logger
from ..dboperator import *
from ..dbmodels.model import RecordBase
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session
from typing import Iterable


__DEFAULT_LIMIT = 30


def compute_means(engine: Engine, limit: int = __DEFAULT_LIMIT):
    session = new_session_with_engine(engine)
    needed_computed_ids = read_needed_compute_data(limit, session)
    logger.debug('The ids: %s will be computed, the mean for type %d' %(needed_computed_ids, limit))
    df = pd.read_sql_query('select * from record_base order by id', engine).rename(str.upper, axis='columns')
    means = list()
    for item in needed_computed_ids:
        data = df.loc[df['ID'] <= item].reset_index().tail(limit).loc[:, 'ID']
        if all((diff_data := data.diff().fillna(1.0).isin([1.0]))) == False:
            for index in diff_data[diff_data == False].index.values:
                if not str(df.at[index, 'ID']).endswith('001'):
                    raise ValueError('Missing continuous ID at %s' %index)
        mean = df.loc[df['ID'] <= item].reset_index().tail(limit).loc[:, 'RED_1':'BLUE'].mean()
        means.append(RecordsMean(id=item, mean1=mean['RED_1'], mean2=mean['RED_2'], mean3=mean['RED_3'], 
                                 mean4=mean['RED_4'], mean5=mean['RED_5'], mean6=mean['RED_6'], mean_blue=mean['BLUE'],
                                 type=limit))
    session.add_all(means)
    session.commit()
    logger.info('Mean compute complete!')


def read_needed_compute_data(limit: int, session: Session) -> Iterable[int]:
    rb = session.query(RecordBase.id).order_by(RecordBase.id).offset(limit-1).limit(1).one()
    logger.info('Start from id %s' %rb)
    ids = session.query(RecordBase.id) \
            .outerjoin(RecordsMean) \
            .filter(RecordsMean.id == None) \
            .filter(RecordBase.id >= rb[0]) \
            .order_by(RecordBase.id) \
            .all()
    return [inner for outer in ids for inner in outer]
