# encoding: utf-8

from ..dboperator import *
from ..dbmodels.model import RecordBase, RecordsMean
import pandas as pd
from Spider.logging import LoggerFactory
from sqlalchemy import outerjoin, and_
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session
from typing import Iterable


_DEFAULT_LIMIT = 30
logger = LoggerFactory.get_logger(__name__)


class Compute:
    """
    Base class for computing.
    This aims to provide a common constructor
    """
    def __init__(self, engine: Engine, limit: int = _DEFAULT_LIMIT, /):
        """
        :param engine: The DB engine object
        :param limit: The type of the limit to be computed
        """
        self._engine = engine
        self._limit = limit


class ComputeMean(Compute):
    def compute_means(self):
        """
        Compute the mean
        """
        logger.info('Start to compute mean')
        session = new_session_with_engine(self._engine)
        needed_computed_ids = self.read_needed_compute_data(session)
        logger.debug('The ids: %s will be computed, the mean for type %d' %(needed_computed_ids, self._limit))
        df = pd.read_sql_query('select * from record_base order by id', self._engine).rename(str.upper, axis='columns')
        means = list()
        for item in needed_computed_ids:
            data = df.loc[df['ID'] <= item].reset_index().tail(self._limit).loc[:, 'ID']
            # Get all ids' difference, fill the first with 1
            diff = data.diff().fillna(1)
            data = pd.DataFrame({'ID': data.astype(str).values, 'DIFF': diff.values})
            # Get the difference are not 1, we think they aren't continuous'
            tmp = data[data.loc[:, 'DIFF'] != 1]
            # If the records aren't continuous and the id don't end with '001', they aren't truely continuous.
            error = False if tmp.empty else not tmp.loc[:, 'ID'].str.endswith('001').all()
            if error:
                raise ValueError(f"Missing continuous ID at {tmp.loc[:, 'ID'].values}")
            mean = df.loc[df['ID'] <= item].reset_index().tail(self._limit).loc[:, 'RED_1':'BLUE'].mean()
            means.append(RecordsMean(id=item, mean1=mean['RED_1'], mean2=mean['RED_2'], mean3=mean['RED_3'], 
                                    mean4=mean['RED_4'], mean5=mean['RED_5'], mean6=mean['RED_6'], mean_blue=mean['BLUE'],
                                    type=self._limit))
        session.add_all(means)
        session.commit()
        logger.info('Mean compute complete!')


    def read_needed_compute_data(self, session: Session, /) -> Iterable[int]:
        """
        Query those needs calculated id of the recoreds
        :param session: The DB session object
        :return: The ids.
        """
        rb_limit_cte = session.query(RecordBase).order_by(RecordBase.id).limit(-1).offset(self._limit).cte()
        ids = session.query(rb_limit_cte.c.id)\
            .select_from(outerjoin(rb_limit_cte, \
                                    RecordsMean, \
                                    and_(rb_limit_cte.c.id == RecordsMean.id, RecordsMean.type == self._limit)))\
            .filter(RecordsMean.id == None)\
            .order_by(rb_limit_cte.c.id)\
            .all()
        return [inner for outer in ids for inner in outer]


class ComputeBaseInfo(Compute):
    """
    Compute the information in record_data table
    """
    def compute(self):
        logger.info("Start computing base information in recore_data table")
        data = self._prepare_data()


    def _prepare_data(self) -> pd.DataFrame:
        """
        Prepare the data according to record_data table
        """
        df = pd.read_sql_query('select rb.* from record_base rb left join record_data rd on rb.ID = rd.id \
                where rd.id ISNULL order by rb.ID;', self._engine).rename(str.upper, axis='columns')
        
        reds = df.loc[:, 'RED_1':'RED_6']
        blues = df.loc[:, 'BLUE']
        roe = reds.transform(lambda x: x%2).aggregate(pd.Series.value_counts, axis=1).fillna(0).astype(int)\
                .rename(columns={0:'RED_ODD', 1:'RED_EVEN'})
        data = reds.transform(lambda x: (x-1)//11).aggregate(pd.Series.value_counts, axis=1).fillna(0).astype(int)\
                .rename(columns={0:'RED_PART_LOW', 1:'RED_PART_MID', 2:'RED_PART_HIGH'})\
                .assign(BLUE=blues.transform(lambda x: (x-1)//8), 
                        RED_ODD=roe.loc[:, 'RED_ODD'],
                        RED_EVEN=roe.loc[:, 'RED_EVEN'],
                        BLUE_ODD_EVEN=blues.transform(lambda x: x%2))
        logger.debug('Computed data %s', data)
        return data